from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from django.http import HttpResponseForbidden

from django.contrib.auth.models import Group

from .models import Artigo, Comentario

from .forms import ArtigoForm, ComentarioForm


def is_autor(user):
    return user.groups.filter(name='autores').exists()


def lista_artigos(request):

    artigos = Artigo.objects.all().order_by("-data_criacao")

    return render(
        request,
        "artigos/lista_artigos.html",
        {"artigos": artigos}
    )


def detalhe_artigo(request, id):

    artigo = get_object_or_404(Artigo, id=id)

    comentarios = artigo.comentarios.all()

    if request.method == "POST":

        if request.user.is_authenticated:

            form = ComentarioForm(request.POST)

            if form.is_valid():

                comentario = form.save(commit=False)

                comentario.artigo = artigo

                comentario.utilizador = request.user

                comentario.save()

                return redirect("detalhe_artigo", id=id)

    else:
        form = ComentarioForm()

    return render(
        request,
        "artigos/detalhe_artigo.html",
        {
            "artigo": artigo,
            "comentarios": comentarios,
            "form": form
        }
    )


@login_required
def criar_artigo(request):

    if not is_autor(request.user):
        return HttpResponseForbidden("Sem permissão")

    if request.method == "POST":

        form = ArtigoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            artigo = form.save(commit=False)

            artigo.autor = request.user

            artigo.save()

            return redirect("lista_artigos")

    else:
        form = ArtigoForm()

    return render(
        request,
        "artigos/form_artigo.html",
        {"form": form}
    )


@login_required
def editar_artigo(request, id):

    artigo = get_object_or_404(Artigo, id=id)

    if artigo.autor != request.user:
        return HttpResponseForbidden("Sem permissão")

    if request.method == "POST":

        form = ArtigoForm(
            request.POST,
            request.FILES,
            instance=artigo
        )

        if form.is_valid():
            form.save()
            return redirect("detalhe_artigo", id=id)

    else:
        form = ArtigoForm(instance=artigo)

    return render(
        request,
        "artigos/form_artigo.html",
        {"form": form}
    )


def like_artigo(request, id):

    artigo = get_object_or_404(Artigo, id=id)

    if request.user.is_authenticated:

        if request.user in artigo.likes.all():

            artigo.likes.remove(request.user)

        else:
            artigo.likes.add(request.user)

    return redirect("detalhe_artigo", id=id)