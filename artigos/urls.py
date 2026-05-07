from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.lista_artigos,
        name="lista_artigos"
    ),

    path(
        "<int:id>/",
        views.detalhe_artigo,
        name="detalhe_artigo"
    ),

    path(
        "criar/",
        views.criar_artigo,
        name="criar_artigo"
    ),

    path(
        "editar/<int:id>/",
        views.editar_artigo,
        name="editar_artigo"
    ),

    path(
        "like/<int:id>/",
        views.like_artigo,
        name="like_artigo"
    ),

]