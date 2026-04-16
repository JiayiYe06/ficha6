from django.contrib import admin

# Register your models here.

from .models import Licenciatura
admin.site.register(Licenciatura)

from .models import Docente
admin.site.register(Docente)

from .models import UnidadeCurricular
admin.site.register(UnidadeCurricular)

from .models import Tecnologia
admin.site.register(Tecnologia)

from .models import Competencia
admin.site.register(Competencia)

from .models import Projeto
admin.site.register(Projeto)

from .models import TFC
admin.site.register(TFC)

from .models import Classificacao
admin.site.register(Classificacao)

from .models import MakingOf
admin.site.register(MakingOf)

from .models import Formacao
admin.site.register(Formacao)

