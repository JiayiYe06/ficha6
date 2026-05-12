import os

from django.core.files import File

from portfolio.models import (
    UnidadeCurricular,
    Tecnologia,
    Projeto,
    MakingOf,
    Formacao,
)


def migrar_media(queryset, campo):

    for obj in queryset:

        ficheiro = getattr(obj, campo)

        if ficheiro and ficheiro.name:

            try:
                local_path = ficheiro.path

            except Exception:
                print(f"Sem path local: {obj}")
                continue

            if os.path.exists(local_path):

                with open(local_path, "rb") as f:

                    ficheiro.save(
                        os.path.basename(local_path),
                        File(f),
                        save=True
                    )

                print(f"Migrado: {obj}")

            else:
                print(f"Ficheiro não existe: {local_path}")


print("\n--- UnidadeCurricular ---")
migrar_media(UnidadeCurricular.objects.all(), "imagem")

print("\n--- Tecnologia ---")
migrar_media(Tecnologia.objects.all(), "logo")

print("\n--- Projeto ---")
migrar_media(Projeto.objects.all(), "imagem")

print("\n--- MakingOf ---")
migrar_media(MakingOf.objects.all(), "foto")

print("\n--- Formacao ---")
migrar_media(Formacao.objects.all(), "certificado")

print("\nMigração concluída.")