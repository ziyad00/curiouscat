from django.contrib import admin
from .models import QA

@admin.register(QA)
class QAAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'created']
    list_filter = ['created']