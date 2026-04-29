from django.urls import path
from . import views

urlpatterns = [
    path("", views.portfolio_view, name="portfolio"),

    path("criar/", views.criar_projeto, name="criar_projeto"),
    path("editar/<int:id>/", views.editar_projeto, name="editar_projeto"),
    path("apagar/<int:id>/", views.apagar_projeto, name="apagar_projeto"),

    path("tecnologias/criar/", views.criar_tecnologia, name="criar_tecnologia"),
    path("tecnologias/editar/<int:id>/", views.editar_tecnologia, name="editar_tecnologia"),
    path("tecnologias/apagar/<int:id>/", views.apagar_tecnologia, name="apagar_tecnologia"),
    path("projetos/", views.lista_projetos, name="lista_projetos"),
    path("tecnologias/", views.lista_tecnologias, name="lista_tecnologias"),
    path("competencias/", views.lista_competencias, name="lista_competencias"),
    path("formacoes/", views.lista_formacoes, name="lista_formacoes"),
    
    path("competencias/criar/", views.criar_competencia, name="criar_competencia"),
    path("competencias/editar/<int:id>/", views.editar_competencia, name="editar_competencia"),
    path("competencias/apagar/<int:id>/", views.apagar_competencia, name="apagar_competencia"),
    
    path("formacoes/criar/", views.criar_formacao, name="criar_formacao"),
    path("formacoes/editar/<int:id>/", views.editar_formacao, name="editar_formacao"),
    path("formacoes/apagar/<int:id>/", views.apagar_formacao, name="apagar_formacao"),

    path("sobre/", views.sobre, name="sobre"),

]