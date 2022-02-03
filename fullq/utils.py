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

PRES_CHOICES= choices=(
                                      (0, 'Россия'),
                                      (1, 'Украина'),
                                      (2, 'Казахстан'),
                                      (3, 'Молдова'),
                                      (4, 'Беларусь'),
                                      (5, 'Другая страна бывшего СССР'),
                                      (6, 'Другая'),
                                      (9999, 'Предпочитаю не отвечать')
                                  )
print(rconv(AGE_CHOICES))