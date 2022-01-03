from choices import *
def rconv(v):
    template="""
    c(
    {cont}
    )
    """
    cont = [f'"{j}"={i}' for i,j in v]
    cont= ','.join(cont)
    return template.format(cont=cont)

PRES_CHOICES= choices=[
            (0, 'Владимир Путин'),
            (1, 'Геннадий Зюганов'),
            (2, 'Владимир Жириновский'),
            (3, 'Сергей Шойгу'),
            (4, 'Алексей Навальный'),
            (5, 'Другой кандидат'),
            (111, 'Не пошел бы голосовать'),
            (333, 'Я не гражданин РФ'),
            HARD_TO_SAY_CHOICE
        ]
print(rconv(COVID_VACCINE))