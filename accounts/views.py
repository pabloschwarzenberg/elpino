from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from covid19.models import Usuario

SERVICIOS = (
        (1, 'Servicio 1'),
        (2, 'Servicio 2'),
)

ACTIVIDADES = (
        (1, 'Clínico'),
        (2, 'Administrativo'),
)

class SignUpForm(UserCreationForm):
    username = forms.CharField(label="Rut",max_length=30, required=True, help_text='')
    nombre = forms.CharField(max_length=30, required=True, help_text='')
    apellido_paterno = forms.CharField(max_length=30, required=True, help_text='')
    apellido_materno = forms.CharField(max_length=30, required=True, help_text='')
    fecha_nacimiento = forms.DateField(required=True, help_text='dd/mm/yyyy')
    funcionario = forms.BooleanField(required=False, help_text='')
    servicio = forms.TypedChoiceField(choices=SERVICIOS,required=False, help_text='Sólo si es funcionario',empty_value=None)
    actividad = forms.TypedChoiceField(choices=ACTIVIDADES, required=False, help_text='Sólo si es funcionario',empty_value=None)
    email = forms.EmailField(max_length=254, help_text='')

    class Meta:
        model = Usuario
        fields = ('username', 'nombre', 'apellido_paterno', 'apellido_materno',
        'fecha_nacimiento','funcionario','servicio','actividad','email','password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["password1"].help_text="Debe tener al menos 8 caracteres, con letras y números"
        self.fields["password2"].help_text="Repita su clave por favor"

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
