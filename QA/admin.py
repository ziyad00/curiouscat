from django.contrib import admin
from .models import QA, Reply

class ReplyInline(admin.StackedInline):
    model = Reply

@admin.register(QA)
class QAAdmin(admin.ModelAdmin):
    list_display = ['question', 'created', 'published']
    list_filter = ['created']
    inlines = [ReplyInline]