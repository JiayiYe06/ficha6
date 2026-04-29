from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjetoForm
from .forms import TecnologiaForm
from django.shortcuts import get_object_or_404, redirect
from .models import Projeto, Tecnologia, Competencia, Formacao
from .models import Competencia, Formacao
from .forms import CompetenciaForm, FormacaoForm
from django.shortcuts import get_object_or_404, redirect


def criar_projeto(request):
    if request.method == "POST":
        form = ProjetoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("lista_projetos")
    else:
        form = ProjetoForm()

    return render(request, "portfolio/form_projeto.html", {"form": form})

def editar_projeto(request, id):
    projeto = get_object_or_404(Projeto, id=id)

    if request.method == "POST":
        form = ProjetoForm(request.POST, request.FILES, instance=projeto)
        if form.is_valid():
            form.save()
            return redirect("lista_projetos")
    else:
        form = ProjetoForm(instance=projeto)

    return render(request, "portfolio/form_projeto.html", {"form": form})

def apagar_projeto(request, id):
    projeto = get_object_or_404(Projeto, id=id)

    if request.method == "POST":
        projeto.delete()
        return redirect("lista_projetos")

    return render(request, "portfolio/confirmar_delete.html", {"projeto": projeto})


def portfolio_view(request):
    return render(request, "portfolio/portfolio.html")


def criar_tecnologia(request):
    if request.method == "POST":
        form = TecnologiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("lista_tecnologias")
    else:
        form = TecnologiaForm()

    return render(request, "portfolio/form_tecnologia.html", {"form": form})

def editar_tecnologia(request, id):
    tecnologia = get_object_or_404(Tecnologia, id=id)

    if request.method == "POST":
        form = TecnologiaForm(request.POST, request.FILES, instance=tecnologia)
        if form.is_valid():
            form.save()
            return redirect("lista_tecnologias")
    else:
        form = TecnologiaForm(instance=tecnologia)

    return render(request, "portfolio/form_tecnologia.html", {"form": form})

def apagar_tecnologia(request, id):
    tecnologia = get_object_or_404(Tecnologia, id=id)

    if request.method == "POST":
        tecnologia.delete()
        return redirect("lista_tecnologias")

    return render(request, "portfolio/confirmar_delete_tecnologia.html", {"tecnologia": tecnologia})

def lista_projetos(request):
    projetos = Projeto.objects.all()
    return render(request, "portfolio/projetos.html", {"projetos": projetos})

def lista_tecnologias(request):
    tecnologias = Tecnologia.objects.all()
    return render(request, "portfolio/tecnologias.html", {"tecnologias": tecnologias})


def lista_competencias(request):
    competencias = Competencia.objects.all()
    return render(request, "portfolio/competencias.html", {"competencias": competencias})


def lista_formacoes(request):
    formacoes = Formacao.objects.all()
    return render(request, "portfolio/formacoes.html", {"formacoes": formacoes})

def criar_competencia(request):
    if request.method == "POST":
        form = CompetenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_competencias")
    else:
        form = CompetenciaForm()

    return render(request, "portfolio/form_competencia.html", {"form": form})


def editar_competencia(request, id):
    competencia = get_object_or_404(Competencia, id=id)

    if request.method == "POST":
        form = CompetenciaForm(request.POST, instance=competencia)
        if form.is_valid():
            form.save()
            return redirect("lista_competencias")
    else:
        form = CompetenciaForm(instance=competencia)

    return render(request, "portfolio/form_competencia.html", {"form": form})


def apagar_competencia(request, id):
    competencia = get_object_or_404(Competencia, id=id)

    if request.method == "POST":
        competencia.delete()
        return redirect("lista_competencias")

    return render(request, "portfolio/confirmar_delete_competencia.html", {"competencia": competencia})

def criar_formacao(request):
    if request.method == "POST":
        form = FormacaoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("lista_formacoes")
    else:
        form = FormacaoForm()

    return render(request, "portfolio/form_formacao.html", {"form": form})


def editar_formacao(request, id):
    formacao = get_object_or_404(Formacao, id=id)

    if request.method == "POST":
        form = FormacaoForm(request.POST, request.FILES, instance=formacao)
        if form.is_valid():
            form.save()
            return redirect("lista_formacoes")
    else:
        form = FormacaoForm(instance=formacao)

    return render(request, "portfolio/form_formacao.html", {"form": form})


def apagar_formacao(request, id):
    formacao = get_object_or_404(Formacao, id=id)

    if request.method == "POST":
        formacao.delete()
        return redirect("lista_formacoes")

    return render(request, "portfolio/confirmar_delete_formacao.html", {"formacao": formacao})

def sobre(request):
    return render(request, "portfolio/sobre.html")

def sobre(request):
    texto = """
# Sobre esta aplicação

## 1. Arquitetura MVT
A aplicação segue o padrão MVT:
- Model: estrutura da base de dados
- View: lógica da aplicação
- Template: interface com o utilizador

<img src="/media/makingof/foto4.png" width="400">

---

## 2. Modelação
O sistema é composto por várias entidades:
- Projeto
- Tecnologia
- Competência
- Formação
- Licenciatura
- Docente
- Unidade Curricular
- TFC
- Classificação
- Making Of


<img src="/media/makingof/foto3.png" width="400">

---

## 3. Tecnologias
Foram utilizadas:
- Django 
- HTML 
- GitHub (controlo de versões)

---

## 4. Estrutura das páginas
A aplicação está organizada em:
- Página inicial (menu)
- Projetos
- Tecnologias
- Competências
- Formações

---

## 5. GitHub
O projeto está disponível em:
https://github.com/JiayiYe06/ficha6


---

## 6. Making Of
Durante o desenvolvimento foram feitos vários registos:
- criação de models
- implementação de CRUD
- organização das páginas

"""

    return render(request, "portfolio/sobre.html", {"texto": texto})