from django.contrib import admin
from .models import Recharge

@admin.register(Recharge)
class RechargeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'recharge_type', 'date_submitted')
    list_filter = ('recharge_type', 'date_submitted')
    search_fields = ('first_name', 'last_name', 'email', 'recharge_code')
