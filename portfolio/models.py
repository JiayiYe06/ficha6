from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
# Create your models here.

NIVEL_CHOICES = [
    (1, "Muito baixo"),
    (2, "Baixo"),
    (3, "Médio"),
    (4, "Alto"),
    (5, "Muito alto"),
]

# ─────────────────────────────────────────
# Licenciatura
# ─────────────────────────────────────────
class Licenciatura(models.Model):
    nome         = models.CharField(max_length=200)
    ano_inicio   = models.IntegerField()
    ano_fim      = models.IntegerField(null=True, blank=True)
    universidade = models.CharField(max_length=200)
    descricao    = models.TextField(blank=True)
 
    def __str__(self):
        return self.nome
    
    def clean(self):
        if self.ano_fim and self.ano_fim < self.ano_inicio:
            raise ValidationError("Datas incorretas")
 
    class Meta:
        verbose_name        = "Licenciatura"
        verbose_name_plural = "Licenciaturas"


# ─────────────────────────────────────────
# Docente
# ─────────────────────────────────────────
class Docente(models.Model):
    nome = models.CharField(max_length=200)
    mail = models.EmailField(blank=True)
    link_pagina = models.URLField(blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Docente"
        verbose_name_plural = "Docentes"

# ─────────────────────────────────────────
# Unidade Curricular
# ─────────────────────────────────────────

TIPO_CHOICES = [
    ("Semestral", "Semestral"),
    ("Anual", "Anual"),
]

class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50, unique=True)

    semestre = models.PositiveSmallIntegerField(null=True, blank=True)
    ano = models.PositiveSmallIntegerField()
    ects = models.PositiveSmallIntegerField()

    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, blank=True)
    natureza = models.CharField(max_length=50, blank=True)

    objetivos = models.TextField(blank=True)
    programa = models.TextField(blank=True)

    imagem = models.ImageField(upload_to="uc/imagens/", null=True, blank=True)

    # UC - Licenciatura  →  N:1
    licenciatura = models.ForeignKey(
        Licenciatura,
        on_delete=models.CASCADE,
        related_name="unidades_curriculares",
    )

    # UC - Docente  →  N:N
    docentes = models.ManyToManyField(
        Docente,
        related_name="unidades_curriculares",
        blank=True,
    )

    def __str__(self):
        return f"{self.nome} (S{self.semestre} – Ano {self.ano})"

    class Meta:
        verbose_name        = "Unidade Curricular"
        verbose_name_plural = "Unidades Curriculares"


# ─────────────────────────────────────────
# Tecnologia
# ─────────────────────────────────────────

class Tecnologia(models.Model):
    nome            = models.CharField(max_length=100)
    tipo            = models.CharField(max_length=100)
    descricao       = models.TextField(blank=True)
    logo            = models.ImageField(upload_to="tecnologias/logos/", null=True, blank=True)
    link_oficial    = models.URLField(blank=True)
    nivel_interesse = models.PositiveSmallIntegerField(choices=NIVEL_CHOICES, default=3)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name        = "Tecnologia"
        verbose_name_plural = "Tecnologias"


# ─────────────────────────────────────────
# Competência
# ─────────────────────────────────────────

class Competencia(models.Model):
    nome = models.CharField(max_length=200)
    nivel = models.PositiveSmallIntegerField(choices=NIVEL_CHOICES, default=3)
    descricao = models.TextField(blank=True)

    # Competência - Tecnologia  →  N:N
    tecnologias = models.ManyToManyField(
    Tecnologia,
    related_name="competencias",
    blank=True,
    help_text="Use Ctrl (ou Command) para selecionar várias tecnologias. Os itens destacados estão selecionados."
)

    def __str__(self):
        return f"{self.nome} (Nível {self.nivel})"

    class Meta:
        verbose_name        = "Competência"
        verbose_name_plural = "Competências"


# ─────────────────────────────────────────
# Projeto  (entidade base — TFC é uma especialização)
# ─────────────────────────────────────────
class Projeto(models.Model):
    ESTADO_CHOICES = [
        ("em_curso",  "Em curso"),
        ("concluido", "Concluído"),
    ]

    titulo              = models.CharField(max_length=300)
    ano                 = models.PositiveSmallIntegerField()
    conceitos_aplicados = models.TextField(blank=True)
    imagem = models.ImageField(upload_to="tfcs/", blank=True, null=True)
    video_demo          = models.URLField(blank=True)
    link_repositorio    = models.URLField(blank=True)
    estado              = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="em_curso")
    autor = models.CharField(max_length=200)
    
    # Projeto - UC  →  N:1
    unidade_curricular = models.ForeignKey(
    UnidadeCurricular,
    on_delete=models.CASCADE,
    related_name="projetos",
    )
    
    # Projeto - Competência  →  N:N
    competencias = models.ManyToManyField(
        Competencia,
        related_name="projetos",
        blank=True,
    )

    # Projeto - Tecnologia  →  N:N
    tecnologias = models.ManyToManyField(
        Tecnologia,
        related_name="projetos",
        blank=True,
    )

    def __str__(self):
        return f"{self.titulo} ({self.estado})"

    class Meta:
        ordering = ["-ano"]
        verbose_name        = "Projeto"
        verbose_name_plural = "Projetos"


# ─────────────────────────────────────────
# TFC  (especialização de Projeto — herança multi-tabela)
# ─────────────────────────────────────────
class TFC(Projeto):

    # Docente - TFC  →  N:N
    orientadores = models.ManyToManyField(
        Docente,
        related_name="tfcs",
        blank=True,
    )

    # NOVOS CAMPOS (alinhados com JSON)
    resumo = models.TextField(blank=True)

    palavras_chave = models.CharField(max_length=300, blank=True)

    area = models.CharField(max_length=200, blank=True)

    rating = models.IntegerField(
    validators=[MinValueValidator(0), MaxValueValidator(10)],
    null=True,
    blank=True
)

    def __str__(self):
        return f"TFC: {self.titulo}"


# ─────────────────────────────────────────
# Classificação
# ─────────────────────────────────────────
class Classificacao(models.Model):
    TIPO_CHOICES = [
        ("quizz", "Quizz"),
        ("teste", "Teste"),
        ("projeto", "Projeto"),
        ("defesa", "Defesa"),
        ("exame_recurso", "Exame Recurso"),
        ("nota_final", "Nota Final"),
    ]

    valor = models.DecimalField(
    max_digits=4,
    decimal_places=1,
    validators=[
        MinValueValidator(0),
        MaxValueValidator(20)
        ]
    )
    data      = models.DateField()
    tipo      = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descricao = models.TextField(blank=True)

    # Classificação - Projeto  →  N:1
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="classificacoes",
    )

    # Classificação - UC  →  N:1
    unidade_curricular = models.ForeignKey(
        UnidadeCurricular,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="classificacoes",
    )

    # Classificação - Formação  →  N:1
    # Referência lazy (string) porque Formacao é definida a seguir
    formacao = models.ForeignKey(
        "Formacao",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="classificacoes",
    )

    def clean(self):
        
        ligacoes = [
            self.projeto,
            self.unidade_curricular,
            self.formacao,
        ]
        if sum(1 for l in ligacoes if l) != 1:
            raise ValidationError("Só pode estar ligado a uma entidade.")

    def __str__(self):
        return f"{self.tipo} – {self.valor} ({self.data})"

    class Meta:
        verbose_name        = "Classificação"
        verbose_name_plural = "Classificações"


# ─────────────────────────────────────────
# Making Of
# ─────────────────────────────────────────
class MakingOf(models.Model):
    data = models.DateField()
    etapa = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    foto = models.ImageField(upload_to="makingof/fotos/", null=True, blank=True)
    decisao = models.TextField(blank=True)
    erros = models.TextField(blank=True)
    uso_IA = models.BooleanField(default=False)

    # Making Of - Projeto  →  N:1
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name="making_ofs",
    )

    def __str__(self):
        return f"{self.etapa} ({self.data})"
# ─────────────────────────────────────────
# Formação
# ─────────────────────────────────────────
class Formacao(models.Model):
    nome               = models.CharField(max_length=300)
    data_inicio        = models.DateField()
    data_fim           = models.DateField(null=True, blank=True)
    entidade_formadora = models.CharField(max_length=200)
    certificado        = models.FileField(upload_to="formacoes/certificados/", null=True, blank=True)
    descricao          = models.TextField(blank=True)

    # Formação - Competência  →  N:N
    competencias = models.ManyToManyField(
        Competencia,
        related_name="formacoes",
        blank=True,
    )
    
    def clean(self):
        if self.data_fim and self.data_fim < self.data_inicio:
            raise ValidationError("Datas incorretas")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name        = "Formação"
        verbose_name_plural = "Formações"