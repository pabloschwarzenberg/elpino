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
from django.conf import settings
from django.shortcuts import redirect
from covid19.models import Usuario

class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if "username" not in request.session:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return super().dispatch(request, *args, **kwargs)

class HomePageView(CustomLoginRequiredMixin,TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'noticias.html', {'noticias': Noticia.noticias.all()})

class AboutView(CustomLoginRequiredMixin,TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'about.html')

class HomeNoticiasView(CustomLoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        return render(request, 'noticias.html', {'noticias': Noticia.noticias.all().order_by("-fecha")})

class HomeEstadisticasNacionalesView(CustomLoginRequiredMixin,TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'estadisticas_nacionales.html')

class HomeEstadisticasView(CustomLoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        try:
            return render(request, 'estadisticas.html', {'estadisticas': Estadistica.estadisticas.latest('fecha')})
        except:
            return render(request, 'estadisticas.html', {'estadisticas':
            {'confirmados_Hospital':0,
            'examenes_Hospital':0,
            'hospital_contagios':0,
            'hospital_recuperados':0
            }})

class HomeEstadisticasListView(CustomLoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        try:
            return render(request, 'estadisticas_list.html', {'estadisticas': Estadistica.estadisticas.order_by('fecha')})
        except:
            return render(request, 'estadisticas_list.html', {'estadisticas': []})   

class HomeAlgoritmosView(CustomLoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        return render(request, 'biblioteca.html',
        {'documentos': Documento.documentos.filter(tipo=1).order_by('-fecha'),'titulo': 'Flujogramas', 'tipo':1})

class HomeBibliotecaView(CustomLoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        return render(request, 'biblioteca.html',
        {'documentos': Documento.documentos.all().order_by('-fecha'), 'titulo': 'Biblioteca','tipo':0})

class HomeVideosView(CustomLoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        return render(request, 'biblioteca.html',
        {'documentos': Documento.documentos.filter(tipo=2).order_by('-fecha'), 'titulo': 'Videos','tipo':2})

class DetalleNoticiaView(CustomLoginRequiredMixin,TemplateView):
    def get(self, request, **kwargs):
        id=kwargs["pk"]
        return render(request, 'noticia.html', {'noticia': Noticia.noticias.get(id=id)})

class NoticiaCreate(CustomLoginRequiredMixin,CreateView):
    model = Noticia
    template_name='./noticia_form.html'
    fields = ['fecha','titulo','imagen','descripcion']
    
    def form_valid(self,form):
        autor=Usuario.objects.get(username=self.request.user)
        form.instance.autor=autor.nombre+" "+autor.apellido_paterno
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super(NoticiaCreate, self).get_form(form_class)
        form.fields['fecha'].input_formats=['%d/%m/%Y %H:%M %p']
        form.fields['fecha'].widget = forms.DateTimeInput(attrs={
            'class': 'datetimepicker-input',
            'data-target': '#datetimepicker1'})
        form.fields['titulo'].widget = forms.Textarea(attrs={'cols': 80, 'rows': 2})
        form.fields['descripcion'].widget = forms.Textarea(attrs={'cols': 80, 'rows': 15})
        return form

class NoticiaUpdate(CustomLoginRequiredMixin,UpdateView):
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

class NoticiaDelete(CustomLoginRequiredMixin,DeleteView):
    model = Noticia
    template_name='./noticia_confirm_delete.html'
    success_url = reverse_lazy('noticias')

class DetalleDocumentoView(CustomLoginRequiredMixin,TemplateView):
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
            if "archivo" in form.cleaned_data and form.cleaned_data["archivo"]:
                form.add_error("link","No puede subir archivos de video, por favor indique el link a youtube")
                return self.form_invalid(form)
        else:
            if not form.cleaned_data["archivo"]:
                form.add_error("archivo","Debe indicar un archivo")
                return self.form_invalid(form)
        
        return super().form_valid(form)

class DocumentoCreate(CustomLoginRequiredMixin,DocumentValidationMixin,CreateView):
    model = Documento
    template_name='./documento_form.html'
    fields = ['tipo','titulo','link','archivo']

    def get_form(self, form_class=None):
        form = super(DocumentoCreate, self).get_form(form_class)

        return form

class DownloadDocumentCreate(DocumentoCreate):
    fields = ['tipo','titulo','archivo']

class VideoCreate(DocumentoCreate):
    fields = ['tipo','titulo','link']

class DocumentoUpdate(DocumentValidationMixin,UpdateView):
    model = Documento
    template_name='./documento_form.html'
    fields = ['tipo','titulo','link','archivo']

    def get_form(self, form_class=None):
        form = super(DocumentoUpdate, self).get_form(form_class)
        form.fields['tipo'].widget.attrs={'disabled':'disabled'}

        return form

class DownloadDocumentUpdate(CustomLoginRequiredMixin,DocumentoUpdate):
    fields = ['tipo','titulo','archivo']

class VideoUpdate(CustomLoginRequiredMixin,DocumentoUpdate):
    fields = ['tipo','titulo','link']

class DocumentoDelete(CustomLoginRequiredMixin,DeleteView):
    model = Documento
    template_name='./documento_confirm_delete.html'
    success_url = reverse_lazy('biblioteca')

class CustomRadioSelect(forms.RadioSelect):
    template_name="./customradio.html"

class ContactoCreate(CustomLoginRequiredMixin,CreateView):
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

class ContactoEvaluationView(CustomLoginRequiredMixin,TemplateView):
    def get(self, request, **kwargs):
        pk=kwargs["pk"]
        return render(request, 'evaluacion.html', {'contacto':Contacto.contactos.get(id=pk)})

class EstadisticaFormatMixin():
    def configurar(self,form):
        form.fields['fecha'].widget = forms.DateInput(format="%d/%m/%Y",attrs={
            'class': 'datepicker',
            'autocomplete': 'off'})
        form.fields['fecha'].input_formats=['%d/%m/%Y']
        form.fields['confirmados_Hospital'].label = "Cantidad de Contagiados"
        form.fields['examenes_Hospital'].label = "Test PCR tomados"
        form.fields['hospital_VMI'].label = "Pacientes hospitalizados en VMI"
        form.fields['hospital_TOTAL'].label = "Total de Hospitalizados COVID-19 hoy"
        form.fields['funcionarios_contagiados'].label = "Funcionarios Contagiados"
        form.fields['funcionarios_PCR'].label = "Test PCR a Funcionarios"

        return form

class EstadisticaCreate(CustomLoginRequiredMixin,EstadisticaFormatMixin,CreateView):
    model = Estadistica
    template_name='./estadistica_form.html'
    fields = ['fecha', 'confirmados_Hospital','examenes_Hospital',
    'hospital_VMI','hospital_TOTAL',
    'funcionarios_contagiados', 'funcionarios_PCR']

    def get_form(self, form_class=None):
        form = super(EstadisticaCreate, self).get_form(form_class)
        return self.configurar(form)

class EstadisticaUpdate(CustomLoginRequiredMixin,EstadisticaFormatMixin,UpdateView):
    model = Estadistica
    template_name='./estadistica_form.html'
    fields = ['fecha', 'confirmados_Hospital','examenes_Hospital',
    'hospital_VMI','hospital_TOTAL',
    'funcionarios_contagiados', 'funcionarios_PCR']

    def get_form(self, form_class=None):
        form = super(EstadisticaUpdate, self).get_form(form_class)
        return self.configurar(form)

class EstadisticaDelete(CustomLoginRequiredMixin,DeleteView):
    model = Estadistica
    template_name='./estadistica_confirm_delete.html'
    success_url = reverse_lazy('estadistica_list')

def casos_hospital_chart(request):
    datasets = []
    datasets_h=[]
    datasets_f=[]

    queryset = Estadistica.estadisticas.order_by('-fecha')[:7]
    labels = []
    data_vmi=[]
    data_total=[]
    data_confirmados_Hospital=[]
    data_examenes_Hospital=[]
    data_funcionarios_contagiados=[]
    data_funcionarios_PCR=[]
    for dato in queryset:
        labels.append(dato.fecha.strftime("%d-%m"))
        data_vmi.append(dato.hospital_VMI)
        data_total.append(dato.hospital_TOTAL)
        data_confirmados_Hospital.append(dato.confirmados_Hospital)
        data_examenes_Hospital.append(dato.examenes_Hospital)
        data_funcionarios_contagiados.append(dato.funcionarios_contagiados)
        data_funcionarios_PCR.append(dato.funcionarios_PCR)
    labels.reverse()
    data_vmi.reverse()
    data_total.reverse()
    data_confirmados_Hospital.reverse()
    data_examenes_Hospital.reverse()
    data_funcionarios_contagiados.reverse()
    data_funcionarios_PCR.reverse()
    datasets.append({
        'label': 'VMI',
        'fill': False,
        'data': data_vmi
    })
    datasets.append({
        'label': 'Total',
        'fill' : False,
        'data': data_total
    })
    datasets_h.append({
        'label': 'Total Casos',
        'fill' : False,
        'data': data_confirmados_Hospital
    })
    datasets_h.append({
        'label': 'Test PCR',
        'fill': False,
        'data': data_examenes_Hospital
    })
    datasets_f.append({
        'label': 'Casos Funcionarios',
        'fill' : False,
        'data': data_funcionarios_contagiados
    })
    datasets_f.append({
        'label': 'Test PCR',
        'fill': False,
        'data': data_funcionarios_PCR
    })
    return JsonResponse(data={
        'labels': labels,
        'datasets': datasets,
        'datasets_h': datasets_h,
        'datasets_f': datasets_f
    })