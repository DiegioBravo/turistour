from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

#app_name = 'turismo'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # LOGIN / LOGOUT
    path('login/', auth_views.LoginView.as_view(template_name='index_landing.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),


    # ADMIN
    path('index/', views.admin_index, name='index'),

    path('registrar/', views.registrar_sitio, name='registrar_sitio'),
    path('listar/', views.lista_sitios, name='lista_sitios'),
    path('editar/<int:pk>/', views.editar_sitio, name='editar_sitio'),
    path("index/editar/<int:pk>/", views.admin_index, name="editar_sitio"),

    path("cargar_excel/", views.cargar_excel, name="cargar_excel"),
    path('sitios_json/', views.sitios_turisticos_json, name='sitios_json'),
]