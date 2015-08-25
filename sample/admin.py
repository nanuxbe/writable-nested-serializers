from django.contrib import admin

from .models import Human, Pet


class PetInline(admin.StackedInline):

    model = Pet


@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):

    list_display = ['name', ]
    inlines = [PetInline, ]
