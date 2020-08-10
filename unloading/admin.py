from unloading.models import TrackModel, Track, Storage

from django.contrib import admin
from django.forms.widgets import Textarea
from django.contrib.gis.db import models as gis_models


@admin.register(TrackModel)
class TrackModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'max_load_capacity']


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'getMaxLoadCapacity', 'getContentsWeight', 'getOverloading']


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ['name', 'getContentsWeight', 'polygon', 'getComposition']
    formfield_overrides = {
        gis_models.PolygonField: {'widget': Textarea}
    }
