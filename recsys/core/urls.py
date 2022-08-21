from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.projetos, name='home'),
    path('projeto/<int:projeto_id>', views.projeto_detail, name="project"),
    path('projeto/cadastro', views.projeto_cadastro, name="project_registration"),

    path('desenvolvedores', views.desenvolvedores, name="devs"),
    path('desenvolvedor/<int:desenvolvedor_id>', views.desenvolverdor_detalhe, name="dev_detail"),
    path('desenvolvedor/cadastro', views.desenvolverdor_cadastro, name="dev_registration"),

    path('projeto/<int:projeto_id>/recomendacao', views.recomendacao, name="recommendation"),
]
