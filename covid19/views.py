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
        return render(request, 'estadisticas.html', {'estadisticas': Estadistica.estadisticas.latest('id')})

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
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'})
        form.fields['titulo'].widget = forms.Textarea(attrs={'cols': 80, 'rows': 2})
        form.fields['imagen'].widget = forms.Textarea(attrs={'cols': 80, 'rows': 3})
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
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'})
        form.fields['titulo'].widget = forms.Textarea(attrs={'cols': 80, 'rows': 2})
        form.fields['imagen'].widget = forms.Textarea(attrs={'cols': 80, 'rows': 3})
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
                print(link)
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
        form.instance.status=0
        return super().form_valid(form)

    def get_form(self, form_class=None):
        CHOICES = [(True,"Sí"),(False,"No")]
        form = super(ContactoCreate, self).get_form(form_class)
        form.fields['contacto_confirmado'].widget = CustomRadioSelect(choices=CHOICES)
        form.fields['contacto_confirmado'].label = "¿Ha tenido Contacto con caso confirmado o sospechoso?"
        form.fields['sintomas'].widget = CustomRadioSelect(choices=CHOICES)
        form.fields['sintomas'].label = "¿Tiene Sintomas?"
        form.fields['contacto_10minutos'].widget = CustomRadioSelect(choices=CHOICES)
        form.fields['contacto_10minutos'].label = "¿Estuvo más de 10 minutos con la persona?"
        form.fields['contacto_2horas'].widget = CustomRadioSelect(choices=CHOICES)
        form.fields['contacto_2horas'].label = "¿Estuvo más de 2 horas con la persona en una habitación?"
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
    fields = ['fecha', 'casos_Chile', 'hospital_T1', 'hospital_T2', 'hospital_T3', 'hospital_T4', 'hospital_contagios',
    'hospital_lm']

    def get_form(self, form_class=None):
        form = super(EstadisticaCreate, self).get_form(form_class)
        form.fields['fecha'].input_formats=['%d/%m/%Y']
        form.fields['fecha'].widget = forms.DateTimeInput(attrs={
            'class': 'datetimepicker-input',
            'data-target': '#datetimepicker1'})
        form.fields['casos_Chile'].label = "Cantidad de casos en Chile"
        form.fields['hospital_contagios'].label = "Cantidad de Contagios en el Hospital"
        form.fields['hospital_lm'].label = "Cantidad de LM en el Hospital"
        form.fields['hospital_T1'].label = "Casos Tipo 1 en el Hospital"
        form.fields['hospital_T2'].label = "Casos Tipo 2 en el Hospital"
        form.fields['hospital_T3'].label = "Casos Tipo 3 en el Hospital"
        form.fields['hospital_T4'].label = "Casos Tipo 4 en el Hospital"
        return form

def casos_chile_chart(request):
    labels = []
    data = []

    meses={}
    queryset = Estadistica.estadisticas.all()
    for dato in queryset:
        mes=dato.fecha.strftime("%m")
        if mes in meses:
            casos=meses[mes]
            if casos<dato.casos_Chile:
                meses[mes]=dato.casos_Chile
        else:
            meses[mes]=dato.casos_Chile
    for mes in meses.keys():
        labels.append(mes)
        data.append(meses[mes])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def casos_hospital_chart(request):
    datasets = []

    queryset = Estadistica.estadisticas.order_by("fecha")[:4]
    labels = [ "Tipo 1", "Tipo 2", "Tipo 3", "Tipo 4" ]
    for dato in queryset:
        data = []
        data.append(dato.hospital_T1)
        data.append(dato.hospital_T2)
        data.append(dato.hospital_T3)
        data.append(dato.hospital_T4)
        datasets.append({
            'label': dato.fecha.strftime("%d-%m"),
            'data': data
        })
    
    return JsonResponse(data={
        'labels': labels,
        'datasets': datasets,
    })