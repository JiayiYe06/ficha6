from django.db import models

from django.contrib.auth.models import User


class Artigo(models.Model):

    titulo = models.CharField(max_length=200)

    texto = models.TextField()

    fotografia = models.ImageField(
        upload_to="artigos/",
        blank=True,
        null=True
    )

    link_externo = models.URLField(
        blank=True
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True
    )

    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="artigos"
    )

    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name="likes_artigos"
    )

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.titulo


class Comentario(models.Model):

    artigo = models.ForeignKey(
        Artigo,
        on_delete=models.CASCADE,
        related_name="comentarios"
    )

    utilizador = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    texto = models.TextField()

    data = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.utilizador} - {self.artigo}"