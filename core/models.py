from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя артиста")
    era = models.CharField(max_length=50, verbose_name="Эпоха / Жанр", help_text="Например: 70s Funk, French House")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

class Track(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название трека")
    listen_link = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на прослушивание")   
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='tracks', verbose_name="Артист")
    release_year = models.IntegerField(verbose_name="Год выпуска")
    listen_link = models.URLField(blank=True, verbose_name="Ссылка на прослушивание")

    def __str__(self):
        return f"{self.artist.name} - {self.title} ({self.release_year})"

class SampleRelation(models.Model):
    SAMPLE_TYPES = [
        ('vocal', 'Вокал'),
        ('drum', 'Ударные (Drum Loop)'),
        ('bass', 'Басовая линия'),
        ('melody', 'Мелодия (Synth/Guitar)'),
        ('full', 'Полный кусок (Full Loop)')
    ]

    source_track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='sampled_in', verbose_name="Оригинальный трек (Источник)")
    target_track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='contains_samples', verbose_name="Новый трек (Куда вставили)")
    sample_type = models.CharField(max_length=20, choices=SAMPLE_TYPES, verbose_name="Тип семпла")
    timestamp = models.CharField(max_length=10, blank=True, verbose_name="Таймкод")

    def __str__(self):
        return f"[{self.sample_type}] {self.target_track.title} samples {self.source_track.title}"