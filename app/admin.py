from django.contrib import admin
from .models import MainTask, SubTask


class MainTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'active', 'slug',)
    prepopulated_fields = {'slug': ('title',)}


class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'maintask', 'title', 'active', 'slug',)
    prepopulated_fields = {'slug': ('maintask', 'title',)}


admin.site.register(MainTask, MainTaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)