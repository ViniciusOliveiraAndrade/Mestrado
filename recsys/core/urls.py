from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.projetos, name='projetos'),
    path('projeto/<int:projeto_id>', views.detalhar_projeto, name="detalhe_projeto"),
    path('projeto/cadastro', views.cadastrar_projeto, name="cadastro_projeto"),

    path('desenvolvedores', views.desenvolvedores, name="devs"),
    path('desenvolvedor/<int:desenvolvedor_id>', views.detalhar_desenvolverdor, name="detalhe_dev"),
    path('desenvolvedor/cadastro', views.cadastrar_desenvolverdor, name="cadastro_dev"),

    path('projeto/<int:projeto_id>/recomendacao', views.recomendacao, name="recomendacao"),

    path('projeto/<int:projeto_id>/squads', views.listar_squad, name="squads"),
    path('projeto/<int:projeto_id>/squad/<int:squad_id>', views.detalhar_squad, name="detalhe_squad"),
    path('projeto/<int:projeto_id>/squad/cadastro', views.cadastrar_squad, name="cadastro_squad"),
    path('projeto/<int:projeto_id>/squad/<int:squad_id>/editar', views.editar_squad, name="editar_squad"),
    path('projeto/<int:projeto_id>/squad/<int:squad_id>/deletar', views.deletar_squad, name="deletar_squad"),

    path('projeto/<int:projeto_id>/alocacao/', views.listar_alodos, name="listar_alocacao"),
    path('projeto/<int:projeto_id>/alocacao/alocar', views.alocar_dev, name="alocar_dev"),
    path('projeto/<int:projeto_id>/alocacao/<int:dev_id>/alocar_squad', views.alocar_dev_squad, name="alocar_dev_squad"),
    path('projeto/<int:projeto_id>/alocacao/remover_alocacao/<int:alocacao_id>/', views.remover_alocar_dev, name="remover_alocar_dev"),

]
