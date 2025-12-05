from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Empresa
from .forms import EmpresaForm
from .models import DataPoint
from django.core import serializers
import json
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SitioTuristicoForm
from .models import SitioTuristico
from django.db.models import Count
from django.db.models import Q
import pandas as pd
from django.http import JsonResponse
import requests



def sitios_turisticos_json(request):
    datos = []
    sitios = SitioTuristico.objects.all()

    for sitio in sitios:
        datos.append({
            "lat": float(sitio.latitud),
            "lng": float(sitio.longitud),
            "ciudad": sitio.ciudad,
            "departamento": sitio.departamento,
            "pais": sitio.pais,
        })

    return JsonResponse(datos, safe=False)




def admin_index(request,pk=None):
    empresas = SitioTuristico.objects.all()
    view = request.GET.get("view", "dashboard")

    q = request.GET.get('q', '').strip()
    categoria_filtro = request.GET.get('categoria', '').strip()

    empresas = SitioTuristico.objects.all()

    if q:
        empresas = empresas.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(categoria__icontains=q) |
            Q(ciudad__icontains=q) |
            Q(region__icontains=q) |
            Q(pais__icontains=q) |
            Q(servicios_ofrecidos__icontains=q)
        )
    
    if categoria_filtro:
        empresas = empresas.filter(categoria__iexact=categoria_filtro)

    empresas_json = json.dumps([
        {
            "nombre": e.nombre,
            "lat": float(e.latitud) if e.latitud else None,
            "lng": float(e.longitud) if e.longitud else None,
        }
        for e in empresas
    ])

    categorias = (
        SitioTuristico.objects
        .values('categoria')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    ICONOS_CATEGORIA = {
            'religioso': 'fas fa-church',
            'turistico': 'fas fa-map-marked-alt',
            'otro': 'fas fa-star',
            'gastronomico': 'fas fa-utensils',
            'cultural': 'fas fa-archway',
            'historia': 'fas fa-archway',
            'playa': 'fas fa-umbrella-beach',
            'montaña': 'fas fa-mountain',
        }

    # Convertir queryset de categorías en lista con iconos
    categorias_final = []

    for c in categorias:
        key = (c["categoria"] or "").strip().lower()
        icono = ICONOS_CATEGORIA.get(key, 'fas fa-star')

        categorias_final.append({
            "categoria": c["categoria"],
            "total": c["total"],
            "icono": icono
        })

    context = {
        "empresas": empresas,
        "empresas_json": empresas_json,
        "categorias": categorias_final,
        "q": q,
        "view": view,
        "categoria_filtro": categoria_filtro,
    }

    if view == "listar":
        context["sitios"] = SitioTuristico.objects.all()

    if view == "registrar":
        if request.method == 'POST':
            form = SitioTuristicoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = SitioTuristicoForm()
        context["form"] = SitioTuristicoForm()

    if view == "editar":
        sitio = get_object_or_404(SitioTuristico, pk=pk)

        if request.method == 'POST':
            form = SitioTuristicoForm(request.POST, instance=sitio)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = SitioTuristicoForm(instance=sitio)

        context["form"] = form
        context["sitio"] = sitio

    return render(request, "index.html", context)


def cargar_excel(request):

    if request.method == 'POST':

        archivo = request.FILES.get("archivo")

        if not archivo:
            return render(request, "lista_sitios.html", {
                "error": "Debes seleccionar un archivo Excel."
            })

        df = pd.read_excel(archivo)

        for i, row in df.iterrows():
            print(f"Insertando fila {i}: {row.get('nombre')}")

            SitioTuristico.objects.create(
                nombre=row.get("nombre"),
                categoria=row.get("categoria"),
                ciudad=row.get("ciudad"),
                descripcion=row.get("descripcion"),
                region=row.get("region"),
                pais=row.get("pais"),
                direccion=row.get("direccion"),
                capaciad=row.get("capaciad"),
                servicios_ofrecidos=row.get("servicios_ofrecidos"),
                url_imagen_principal=row.get("url_imagen_principal"),
                nit_sitio=row.get("nit_sitio"),
                etiquetas=row.get("etiquetas"),
                galeria_imagenes=row.get("galeria_imagenes"),
                estado_publicacion=row.get("estado_publicacion"),
                registrado_por=row.get("registrado_por"),
                latitud=float(row.get("latitud")) if not pd.isna(row.get("latitud")) else None,
                longitud=float(row.get("longitud")) if not pd.isna(row.get("longitud")) else None,
            )

        return redirect('/index/?view=listar')

    return render(request, "lista_sitios.html")


def landing(request):
    # formulario que espera tu template
    form = AuthenticationForm() 
     
    return render(request, 'index_landing.html', {'form': form})


@login_required(login_url='login')
def dashboard_view(request):
    # Obtener datos desde SQLite
    data = DataPoint.objects.order_by('created_at')[:50]
    labels = [d.label for d in data]
    values = [d.value for d in data]
    # pasar como JSON al template para Chart.js
    context = {
    'labels_json': json.dumps(labels),
    'values_json': json.dumps(values),
    }
    return render(request, 'dashboard.html', context)


# Crear un sitio turístico
def registrar_sitio(request):
    if request.method == 'POST':
        form = SitioTuristicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_sitios')
    else:
        form = SitioTuristicoForm()

    return render(request, 'registrar_sitio.html', {'form': form})


# Listar todos los sitios turísticos
def lista_sitios(request):
    sitios = SitioTuristico.objects.all().order_by('-fecha_registro')
    return render(request, 'lista_sitios.html', {'sitios': sitios})


# Editar un sitio existente
def editar_sitio(request, pk):
    sitio = get_object_or_404(SitioTuristico, pk=pk)

    if request.method == 'POST':
        form = SitioTuristicoForm(request.POST, instance=sitio)
        if form.is_valid():
            form.save()
            return redirect('lista_sitios')
    else:
        form = SitioTuristicoForm(instance=sitio)

    return render(request, 'editar_sitio.html', {
        'form': form,
        'sitio': sitio
    })





