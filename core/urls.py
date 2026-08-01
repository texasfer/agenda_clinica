from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("admin/", admin.site.urls),

    path("", include("usuarios.urls")),
    path("agenda/", include("agenda.urls")),

    path("clientes/", include("clientes.urls")),

    path("atendimento/", include("atendimento.urls")),

    path("financeiro/", include("financeiro.urls")),
    
    path(
    "configuracoes/",
    include("configuracoes.urls")
),

path(
    "recibos/",
    include("recibos.urls")
),
path('admin/', admin.site.urls),  # <-- Rota padrão do Admin

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)