from unloading.models import Storage, Track, getDefaultContents
from core.utils import round_

from django.contrib.gis.geos import Point
from django.shortcuts import render
from django.http import HttpResponseNotFound


def index(request):
    return render(request, 'unloading/index.html', {'tracks': Track.objects.all()})


def unload(request):
    if request.method != 'POST':
        return HttpResponseNotFound('<h1>Page not found</h1>')
    storages = {}
    errors = []
    for key in request.POST:
        if 'track-' not in key or not request.POST[key]:
            continue
        coordinates = [int(coord) for coord in request.POST[key].split(' ')]
        if (coord_len := len(coordinates)) and coord_len != 2:
            errors.append(
                f'ОШИБКА! Необходимо указать 2 координаты, разделённых запятой. Получено значение: {request.POST[key]}')
            continue
        storage = Storage.objects.filter(polygon__intersects=Point(*coordinates)).first()
        if not storage:
            continue
        track = Track.objects.get(id=int(key[6]))
        old_weight = storage.contents['weight']
        storage.contents['weight'] += track.contents['weight']
        for item in track.contents['composition']:
            if item not in storage.contents['composition']:
                storage.contents['composition'][item] = track.contents['composition'][item]
            else:
                storage.contents['composition'][item] += track.contents['composition'][item]
        track.contents = getDefaultContents()
        storage.save()
        track.save()
        if storage.id not in storages:
            storages[storage.id] = {
                'name': storage.name,
                'old_weight': round_(old_weight / 1000),
                'new_weight': storage.getContentsWeight(),
                'composition': storage.getComposition()
            }
    return render(request, 'unloading/unload.html', {'storages': storages.values(), 'errors': errors})
