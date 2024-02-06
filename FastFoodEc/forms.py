from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class Local_form(forms.ModelForm):

    nombre = forms.CharField(widget = forms.TextInput(
        attrs={
            "placeholder" :"Ingrese el nombre del Local",
            "class" : "step__input",
            "id":"nombre"
        }
    ))
    imagen = forms.CharField(widget = forms.TextInput(
        attrs={
            "placeholder" :"Ingrese un enlace",
            "class" : "step__input",
            "name":"imagen"

        }
    ))
    puntaje = forms.CharField(widget = forms.TextInput(
        attrs={
            "placeholder" :"Coloque el puntaje del Local",
            "class" : "step__input",
            "id":"puntaje"
        }
    ))
    costoEnvio = forms.CharField(widget = forms.TextInput(
        attrs={
            "placeholder" :"Ingrese el costo del envio",
            "class" : "step__input",
            "id":"costoEnvio"
        }
    ))
    tiempo_entrega = forms.CharField(widget = forms.TextInput(
        attrs={
            "placeholder" :"Ingrese el tiempo de entrega del Local",
            "class" : "step__input",
            "type": "time",
            "id":"tiempoEntrega"
            
        }
    ))
    horario= forms.CharField(widget = forms.Textarea(
        attrs={
            "placeholder" :" Ingrese el horario del Local",
            "class" : "step__area",
            "rows" : "7" ,
            "cols": "40",
            "value": "Lunes: 00:00 am - 00:00 pm",
            "id":"horario"
        }
    ))



    class Meta:
        model = Local
        fields ='__all__'


class categoria_form(forms.ModelForm):

    nombre = forms.CharField(widget = forms.TextInput(
        attrs={
            "placeholder" :"Ingrese el nombre de la materia"
        }
    ))
    class Meta:
        model = Categoria
        fields ='__all__'


class cliente_form(forms.ModelForm):

    imagen = forms.CharField(widget = forms.TextInput(
        attrs={
            "placeholder" :"Foto de Perfil",
            "class":"input-form-c",
            "onchange": "cargarImagen()",
            "id":"url-img-profile"
        }
    ))
     

    nombres = forms.CharField(widget = forms.TextInput(
        attrs={
            "placeholder" :"Nombres",
            "class":"input-form-c"
        }
    ))

    apellidos = forms.CharField(widget = forms.TextInput(
        attrs={
            "placeholder" :"Apellidos",
            "class":"input-form-c"
        }
    ))

    telefono= forms.CharField(widget = forms.TextInput(
        attrs={
            "placeholder" :"Telefono",
            "class":"input-form-c"
        }
    ))

    ciudad= forms.CharField(widget = forms.TextInput(
        attrs={
            "placeholder" :"Ciudad",
            "class":"input-form-c"
        }
    ))
    

    direccion= forms.CharField(widget = forms.TextInput(
        attrs={
            "placeholder" :"Dirección",
            "class":"input-form-c"
        }
    ))



    

    class Meta:
        model = Cliente
        fields =['imagen','nombres','apellidos','telefono','ciudad','direccion']

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for fieldname in ['imagen','nombres','apellidos','telefono','ciudad','direccion']:
            self.fields[fieldname].label= ""


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs= {
            "placeholder": "Nombre de Usuario"
        }
    ))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            "placeholder":"Email"
        }
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder":"Contraseña"
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder":"Confirmar Contraseña"
        }
    ))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username','email','password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label= ""
           


