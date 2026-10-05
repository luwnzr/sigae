from django.contrib.auth import views as auth
from django.urls import path

from . import views

urlpatterns = [
    path("login/", auth.LoginView.as_view(template_name="registration/login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", auth.LogoutView.as_view(), name="logout"),  # Django 5: somente POST
    path("", views.dashboard, name="dashboard"),
    path("reservas/", views.reservas, name="reservas"),
    path("turmas/", views.turmas, name="turmas"),
    path("equipamentos/", views.equipamentos, name="equipamentos"),
    path("emprestimos/", views.emprestimos, name="emprestimos"),
    path("emprestimos/solicitacoes/", views.solicitacoes, name="solicitacoes"),
    path("emprestimos/ativos/", views.ativos, name="ativos"),
    path("perfil/", views.PerfilView.as_view(), name="perfil"),
    path("reservar/", views.reservar, name="reservar"),
    path("resgatar/", views.resgatar_view, name="resgatar"),
    path("reservas/<int:pk>/entregar/", views.entregar_view, name="entregar"),
    path("reservas/<int:pk>/devolver/", views.devolver_view, name="devolver"),
    path("reservas/<int:pk>/cancelar/", views.cancelar_view, name="cancelar"),
]
