from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'study_plans'

# Router para ViewSets
router = DefaultRouter()
router.register(r'disciplinas', views.DisciplinaViewSet)
router.register(r'planos', views.PlanoEstudoViewSet, basename='planos')
router.register(r'atividades', views.AtividadePlanoViewSet, basename='atividades')
router.register(r'progressos', views.ProgressoUsuarioViewSet, basename='progressos')

urlpatterns = [
    # URLs do router
    path('', include(router.urls)),
    
    # URLs adicionais
    path('dashboard/', views.dashboard_estatisticas, name='dashboard'),
    path('gerar-plano-ia/', views.gerar_plano_ia, name='gerar_plano_ia'),
]