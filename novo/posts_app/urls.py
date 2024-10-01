from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('home', views.listaEmpresa, name='home'),
    path('empresa/<int:empresa_id>/projetos', views.listaProjeto, name='listaProjeto'),
    path('empresa/<int:empresa_id>/excluir/', views.excluir_empresa, name='excluir_empresa'),
    path('projeto/<int:projeto_id>/excluir/', views.excluir_projeto, name='excluir_projeto'),
    path('empresa/criar/', views.criar_empresa, name='criar_empresa'),
    path('empresa/<int:empresa_id>/editar/', views.editar_empresa, name='editar_empresa'),
    path('projeto/<int:projeto_id>/editar/', views.editar_projeto, name='editar_projeto'),
    path('empresa/<int:empresa_id>/projeto/criar/', views.criar_projeto, name='criar_projeto'),
    path('usuarios/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/excluir/', views.excluir_usuario, name='excluir_usuario'),
]  