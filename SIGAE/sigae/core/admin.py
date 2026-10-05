from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Equipamento, Reserva, Turma, User


@admin.register(User)
class SigaeUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("SIGAE", {"fields": ("turma", "turno")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("SIGAE", {"fields": ("email", "first_name", "last_name", "turma", "turno")}),)
    list_display = ("username", "get_full_name", "email", "turma", "turno")


admin.site.register(Turma)
admin.site.register(Equipamento, list_display=("numero", "status"), list_filter=("status",))
admin.site.register(Reserva, list_display=("id", "solicitante", "data", "turno", "equipamento", "status"),
                    list_filter=("status", "turno", "data"))
