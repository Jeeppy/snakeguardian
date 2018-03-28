from django.contrib import admin
from book.models import (Achat, Document, Emplacement, Hivernation, Maintenance, Mesure, Mue, Photo, Repas, Specimen,
                         Terrarium)


@admin.register(Specimen)
class SpecimenAdmin(admin.ModelAdmin):
    pass


@admin.register(Repas)
class RepasAdmin(admin.ModelAdmin):
    pass


@admin.register(Mue)
class MueAdmin(admin.ModelAdmin):
    pass


@admin.register(Mesure)
class MesureAdmin(admin.ModelAdmin):
    pass


@admin.register(Terrarium)
class TerrariumAdmin(admin.ModelAdmin):
    pass


@admin.register(Emplacement)
class EmplacementAdmin(admin.ModelAdmin):
    pass


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    pass


@admin.register(Achat)
class AchatAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass

@admin.register(Hivernation)
class HivernationAdmin(admin.ModelAdmin):
    pass
