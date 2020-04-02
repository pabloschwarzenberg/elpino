from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Noticia, Estadistica, Documento
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms

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

class HomeContactosView(LoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        return render(request, 'contactos.html')

class HomeEstadisticasView(LoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        return render(request, 'estadisticas.html', {'estadisticas': Estadistica.estadisticas.all()[:1]})

class HomeAlgoritmosView(LoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        return render(request, 'algoritmos.html', {'algoritmos': Documento.documentos.filter(tipo=1)})

class HomeBibliotecaView(LoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        return render(request, 'biblioteca.html', {'documentos': Documento.documentos.filter(tipo=0)})

class HomeVideosView(LoginRequiredMixin,TemplateView):
    #permission_required='puede_buscar_cursos'
    def get(self, request, **kwargs):
        return render(request, 'videos.html', {'videos': Documento.documentos.filter(tipo=2)})

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

class DocumentoCreate(CreateView):
    model = Documento
    template_name='./documento_form.html'
    fields = ['tipo','titulo','link','archivo']

class DocumentoUpdate(UpdateView):
    model = Documento
    template_name='./documento_form.html'
    fields = ['tipo','titulo','link','archivo']

class DocumentoDelete(DeleteView):
    model = Documento
    template_name='./documento_confirm_delete.html'
    success_url = reverse_lazy('biblioteca')
