from django import forms
from .models import Empresa
from .models import SitioTuristico



class SitioTuristicoForm(forms.ModelForm):
    class Meta:
        model = SitioTuristico
        exclude = ['fecha_registro', 'fecha_actualizacion']  # Campos automáticos

        widgets = {
            'nit_sitio': forms.TextInput(attrs={
                'placeholder': 'Ej: 900123456-7'
            }),
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Nombre del sitio turístico'
            }),
            'descripcion': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Breve descripción del sitio'
            }),
            'etiquetas': forms.TextInput(attrs={
                'placeholder': 'Ej: historia, arte, cultura'
            }),
            'pais': forms.TextInput(attrs={'placeholder': 'Ej: Colombia'}),
            'region': forms.TextInput(attrs={'placeholder': 'Ej: Boyacá'}),
            'ciudad': forms.TextInput(attrs={'placeholder': 'Ej: Chiquinquirá'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección exacta del sitio'}),
            'latitud': forms.NumberInput(attrs={
                'placeholder': 'Escribir o Señalar en el mapa'
            }),
            'longitud': forms.NumberInput(attrs={
                'placeholder': 'Escribir o Señalar en el mapa'
            }),
            'capaciad': forms.TextInput(attrs={
                'placeholder': 'Ej: 150 personas'
            }),
            'servicios_ofrecidos': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Separe cada servicio con comas o punto y coma. Ej: parqueadero, restaurante; guías'
            }),
            'url_imagen_principal': forms.URLInput(attrs={
                'placeholder': 'https://ejemplo.com/imagen.jpg'
            }),
            'galeria_imagenes': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Ingrese URLs separadas por comas o punto y coma'
            }),
            'registrado_por': forms.TextInput(attrs={
                'placeholder': 'Nombre de quien registra'
            }),
        }

        help_texts = {
            'servicios_ofrecidos': 'Separe cada servicio usando comas (,) o punto y coma (;).',
            'galeria_imagenes': 'Puede incluir varias URLs separadas por comas o punto y coma.',
        }    


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'direccion', 'latitud', 'longitud']   