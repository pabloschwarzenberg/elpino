from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Noticia, Estadistica, Documento, Contacto
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.http import JsonResponse

class PermissionRequiredInGroupMixin(PermissionRequiredMixin):
    def has_permission(self):
        usuario=self.request.user
        permisos=self.get_permission_required()
        privilegios=[]
        for g in usuario.groups.all():
            for p in g.permissions.all():
                privilegios.append(p.codename)
        for r in permisos:
            if r not in privilegios:
                return False
        return True

class HomePageView(LoginRequiredMixin,TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'noticias.html', {'noticias': Noticia.noticias.all()})

class HomeNoticiasView(LoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        return render(request, 'noticias.html', {'noticias': Noticia.noticias.all()})

class HomeEstadisticasView(LoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        try:
            return render(request, 'estadisticas.html', {'estadisticas': Estadistica.estadisticas.latest('id')})
        except:
            return render(request, 'estadisticas.html', {'estadisticas': {'confirmados_Hospital':0,'hospital_contagios':0}})

class HomeAlgoritmosView(LoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        return render(request, 'biblioteca.html', {'documentos': Documento.documentos.filter(tipo=1),'titulo': 'Algoritmos'})

class HomeBibliotecaView(LoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        return render(request, 'biblioteca.html', {'documentos': Documento.documentos.all(), 'titulo': 'Biblioteca'})

class HomeVideosView(LoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        return render(request, 'biblioteca.html', {'documentos': Documento.documentos.filter(tipo=2), 'titulo': 'Videos'})

class DetalleNoticiaView(LoginRequiredMixin,TemplateView):
    def get(self, request, **kwargs):
        id=kwargs["pk"]
        return render(request, 'noticia.html', {'noticia': Noticia.noticias.get(id=id)})

class NoticiaCreate(CreateView):
    model = Noticia
    template_name='./noticia_form.html'
    fields = ['fecha','titulo','imagen','descripcion']
    
    def get_form(self, form_class=None):
        form = super(NoticiaCreate, self).get_form(form_class)
        form.fields['fecha'].input_formats=['%m/%d/%Y %H:%M %p']
        form.fields['fecha'].widget = forms.DateTimeInput(attrs={
            'class': 'datetimepicker-input',
            'data-target': '#datetimepicker1'})
        form.fields['titulo'].widget = forms.Textarea(attrs={'cols': 80, 'rows': 2})
        form.fields['descripcion'].widget = forms.Textarea(attrs={'cols': 80, 'rows': 15})
        return form

class NoticiaUpdate(UpdateView):
    model = Noticia
    template_name='./noticia_form.html'
    fields = ['fecha','titulo','imagen','descripcion']

    def get_form(self, form_class=None):
        form = super(NoticiaUpdate, self).get_form(form_class)
        form.fields['fecha'].input_formats=['%m/%d/%Y %H:%M %p']
        form.fields['fecha'].widget = forms.DateTimeInput(attrs={
            'class': 'datetimepicker-input',
            'data-target': '#datetimepicker1'})
        form.fields['titulo'].widget = forms.Textarea(attrs={'cols': 80, 'rows': 2})
        form.fields['descripcion'].widget = forms.Textarea(attrs={'cols': 80, 'rows': 15})
        return form

class NoticiaDelete(DeleteView):
    model = Noticia
    template_name='./noticia_confirm_delete.html'
    success_url = reverse_lazy('noticias')

class DetalleDocumentoView(LoginRequiredMixin,TemplateView):
    def get(self, request, **kwargs):
        id=kwargs["pk"]
        return render(request, 'documento.html', {'documento': Documento.documentos.get(id=id)})

class DocumentValidationMixin:
    def form_valid(self,form):
        if form.cleaned_data["tipo"] == 2:
            link=form.cleaned_data["link"]
            if not link:
                form.add_error("link","Para videos debe indicar el link a youtube")
                return self.form_invalid(form)
            else:
                p=link.rfind("/")
                link=link[p+1:]
                if(p==-1) or link=="":
                    form.add_error("link","El link ingresado no es válido")
                    return self.form_invalid(form)
                form.instance.link=link
            if form.cleaned_data["archivo"]:
                form.add_error("link","No puede subir archivos de video, por favor indique el link a youtube")
                return self.form_invalid(form)

        if not form.cleaned_data["link"] and not form.cleaned_data["archivo"]:
            form.add_error("archivo","Debe indicar al menos un link o un archivo")
            return self.form_invalid(form)
        
        return super().form_valid(form)

class DocumentoCreate(DocumentValidationMixin,CreateView):
    model = Documento
    template_name='./documento_form.html'
    fields = ['tipo','titulo','link','archivo']
   
class DocumentoUpdate(DocumentValidationMixin,UpdateView):
    model = Documento
    template_name='./documento_form.html'
    fields = ['tipo','titulo','link','archivo']

class DocumentoDelete(DeleteView):
    model = Documento
    template_name='./documento_confirm_delete.html'
    success_url = reverse_lazy('biblioteca')

class CustomRadioSelect(forms.RadioSelect):
    template_name="./customradio.html"

class ContactoCreate(CreateView):
    model=Contacto
    template_name='./contacto_form.html'
    fields=['contacto_confirmado','sintomas','contacto_10minutos','contacto_2horas']

    def form_valid(self,form):
        form.instance.usuario=self.request.user
        if not form.instance.sintomas and not form.instance.contacto_confirmado and not form.instance.contacto_10minutos and not form.instance.contacto_2horas:
            form.instance.status=0
        else:
            form.instance.status=1
        return super().form_valid(form)

    def get_form(self, form_class=None):
        CHOICES = [(True,"Sí"),(False,"No")]
        form = super(ContactoCreate, self).get_form(form_class)
        form.fields['contacto_confirmado'].widget = forms.RadioSelect(choices=CHOICES)
        form.fields['contacto_confirmado'].label = "¿Ha tenido contacto con un caso confirmado o sospechoso?"
        form.fields['sintomas'].widget = forms.RadioSelect(choices=CHOICES)
        form.fields['sintomas'].label = "¿Tiene Sintomas Respiratorios?"
        form.fields['contacto_10minutos'].widget = forms.RadioSelect(choices=CHOICES)
        form.fields['contacto_10minutos'].label = "¿Estuvo 15 minutos cara a cara a menos de 1 metro de una persona contagiada?"
        form.fields['contacto_2horas'].widget = forms.RadioSelect(choices=CHOICES)
        form.fields['contacto_2horas'].label = "¿Estuvo más de 2 horas con una persona contagiada en una habitación?"
        return form

    def get_success_url(self):
        return reverse_lazy('contacto_evaluacion', kwargs={'pk': self.object.pk})

class ContactoEvaluationView(LoginRequiredMixin,TemplateView):
    def get(self, request, **kwargs):
        pk=kwargs["pk"]
        return render(request, 'evaluacion.html', {'contacto':Contacto.contactos.get(id=pk)})

class EstadisticaCreate(CreateView):
    model = Estadistica
    template_name='./estadistica_form.html'
    fields = ['fecha', 'contagios_Chile','confirmados_Hospital','examenes_Hospital','hospital_UPC','hospital_VMI','hospital_BASICA',
    'hospital_TOTAL', 'hospital_contagios', 'hospital_lm']

    def get_form(self, form_class=None):
        form = super(EstadisticaCreate, self).get_form(form_class)
        form.fields['fecha'].input_formats=['%d/%m/%Y']
        form.fields['fecha'].widget = forms.DateTimeInput(attrs={
            'class': 'datetimepicker-input',
            'data-target': '#datetimepicker1'})
        form.fields['contagios_Chile'].label = "Cantidad de contagios en Chile"
        form.fields['confirmados_Hospital'].label = "Cantidad de Casos Confirmados en el Hospital"
        form.fields['examenes_Hospital'].label = "Cantidad de Exámenes tomados a la fecha en el Hospital"
        form.fields['hospital_UPC'].label = "Pacientes hospitalizados en UPC"
        form.fields['hospital_VMI'].label = "Pacientes hospitalizados en VMI"
        form.fields['hospital_BASICA'].label = "Pacientes hospitalizados en Cama Básica"
        form.fields['hospital_TOTAL'].label = "Total de Hospitalizados COVID-19 hoy"
        form.fields['hospital_contagios'].label = "Funcionarios Contagiados"
        form.fields['hospital_lm'].label = "Cantidad de LM en el Hospital"

        return form

def casos_chile_chart(request):
    labels = []
    data = []
    datasets = []
    nombres = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    for mes in range(1,13):
        queryset = Estadistica.estadisticas.filter(fecha__month=mes,fecha__year=2020).order_by('fecha')[:1]
        for dato in queryset:
            labels.append(nombres[mes-1])
            data.append(dato.contagios_Chile)
    datasets.append({
        'label': "Contagios en Chile",
        'data': data
    })
    return JsonResponse(data={
        'labels': labels,
        'datasets': datasets,
    })

def casos_hospital_chart(request):
    datasets = []

    queryset = Estadistica.estadisticas.order_by('fecha')[:4]
    labels = [ "UPC", "VMI", "Cama Básica", "Hospitalizados Hoy" ]
    for dato in queryset:
        data = []
        data.append(dato.hospital_UPC)
        data.append(dato.hospital_VMI)
        data.append(dato.hospital_BASICA)
        data.append(dato.hospital_TOTAL)
        datasets.append({
            'label': dato.fecha.strftime("%d-%m"),
            'data': data
        })
    return JsonResponse(data={
        'labels': labels,
        'datasets': datasets,
    })