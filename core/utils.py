from typing import Tuple, Union


def inPolygon(x: int, y: int, xp: Tuple[int], yp: Tuple[int]) -> int:
    """
    Проверка вхождения точки в полигон, при попадании точки на границу полигона,
    считается что точка НЕ В полигоне.
    Возвращает 0, если точка НЕ В полигоне, 1 - если В полигоне.
    """
    c = 0
    for i in range(len(xp)):
        if (((yp[i] <= y < yp[i-1]) or (yp[i-1] <= y < yp[i])) and
                (x > (xp[i-1] - xp[i]) * (y - yp[i]) / (yp[i-1] - yp[i]) + xp[i])):
            c = 1 - c
    return c


def round_(x: Union[int, float]):
    """ Арифметическое округление, см. https://pythonworld.ru/osnovy/okruglenie.html """
    return int(x + 0.5)
