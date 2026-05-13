from django.contrib import admin
from .models import ImageLogement, Locataire, LocationContrat, Logement, Profil, Proprietaire


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'telephone', 'adresse')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'telephone')


@admin.register(Proprietaire)
class ProprietaireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'tel', 'email', 'adresse', 'date_creation')
    search_fields = ('nom', 'tel', 'email', 'adresse')


@admin.register(ImageLogement)
class ImageLogementAdmin(admin.ModelAdmin):
    list_display = ('photo', 'legende', 'date_ajout')


@admin.register(Logement)
class LogementAdmin(admin.ModelAdmin):
    list_display = ('adresse', 'type', 'surface', 'loyer', 'caution', 'proprietaire', 'est_disponible')
    list_filter = ('type', 'est_disponible')
    search_fields = ('adresse', 'proprietaire__nom')


@admin.register(Locataire)
class LocataireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'tel', 'email', 'date_creation')
    search_fields = ('nom', 'tel', 'email')


@admin.register(LocationContrat)
class LocationContratAdmin(admin.ModelAdmin):
    list_display = ('locataire', 'logement', 'date_debut', 'date_fin', 'date_creation')
    list_filter = ('date_debut', 'date_fin')
    search_fields = ('locataire__nom', 'logement__adresse')
