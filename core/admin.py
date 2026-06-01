from django.contrib import admin
from .models import Artist, Track, SampleRelation

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'era')
    search_fields = ('name', 'era')

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_year')
    list_filter = ('release_year', 'artist')
    search_fields = ('title', 'artist__name')

@admin.register(SampleRelation)
class SampleRelationAdmin(admin.ModelAdmin):
    list_display = ('source_track', 'target_track', 'sample_type', 'timestamp')
    list_filter = ('sample_type',)