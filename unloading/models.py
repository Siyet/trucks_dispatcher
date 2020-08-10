from core.utils import round_

from django.db import models
from django.contrib.gis.db import models as gis_models


class TrackModel(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=128)
    max_load_capacity = models.PositiveIntegerField(verbose_name='Максимальная грузоподъёмность, кг')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модель самосвалов'
        verbose_name_plural = "Модели самосвалов"


def getDefaultContents():
    return {
        'weight': 0,
        'composition': {
            'SiO2': 0,
            'Fe': 0
        }
    }


class Track(models.Model):
    name = models.CharField(verbose_name='Бортовой номер', max_length=128)
    model = models.ForeignKey(TrackModel, verbose_name="Модель самосвала", on_delete=models.SET_NULL, null=True)
    contents = models.JSONField(verbose_name='Груз, кг', default=getDefaultContents,
                                help_text='Например, {"weight": 100000, "composition": {"SiO2": 32000, "Fe": 67000}}')

    def getMaxLoadCapacity(self):
        return round_(self.model.max_load_capacity / 1000)
    getMaxLoadCapacity.short_description = 'Макс. грузоподъемность, т'

    def _getContentsWeight(self):
        return self.contents['weight'] if 'weight' in self.contents else 0

    def getContentsWeight(self):
        return round_(self._getContentsWeight() / 1000)
    getContentsWeight.short_description = 'Текущий вес, т'

    def getOverloading(self):
        weight = self._getContentsWeight()
        max_weight = self.model.max_load_capacity
        return round_((weight - max_weight) / max_weight * 100) if weight > max_weight else 0
    getOverloading.short_description = 'Перегруз, %'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if 'contents' in self.get_deferred_fields():
            pass  # Анализ изменений и отправка в коллектор статистики
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Самосвал'
        verbose_name_plural = 'Самосвалы'


class Storage(gis_models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=128)
    polygon = gis_models.PolygonField(verbose_name='Территория склада',
                                      help_text='Введите координаты в формате WKT, например, '
                                                'POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))')
    contents = models.JSONField(verbose_name='Содержимое, кг', default=getDefaultContents,
                                help_text='Например, {"weight": 900000, "composition": '
                                          '{"SiO2": 306000, "Fe": 585000}}')

    def __str__(self):
        return self.name

    def _getContentsWeight(self):
        return self.contents['weight'] if 'weight' in self.contents else 0

    def getContentsWeight(self):
        return round_(self._getContentsWeight() / 1000)

    def getComposition(self):
        if not self.contents or 'composition' not in self.contents:
            return 'Нет данных'
        result = []
        total = self._getContentsWeight()
        for key in self.contents['composition']:
            value = self.contents['composition'][key]
            result.append(f"{round_(value / total * 100)}% {key}")

        return ', '.join(result)

    getContentsWeight.short_description = 'Объём, т'

    def save(self, *args, **kwargs):
        if 'contents' in self.get_deferred_fields():
            pass  # Анализ изменений и отправка в коллектор статистики
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'
