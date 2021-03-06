HARD_TO_SAY_CHOICE = [999, 'Затрудняюсь ответить']
COVID_SICK_EGO_CHOICES = [
    (0, 'Не болел/не болею'),
    (1, 'Болел/Болею'),
    (9999, 'Предпочитаю не отвечать'),
    HARD_TO_SAY_CHOICE

]
COVID_SICK_NEARBY_CHOICES = [
    (0, 'Никто не болел/не болеет'),
    (1, 'Болели/Болеют'),
    (9999, 'Предпочитаю не отвечать'),
    HARD_TO_SAY_CHOICE

]


COVID_VACCINE = [
    (0, 'Не привился и не планирую'),
    (1, 'Не привился, но планирую'),
    (2, 'Уже привился'),
    (9999, 'Предпочитаю не отвечать'),
    HARD_TO_SAY_CHOICE

]
SEPARATION_POWER_CHOICES = [
    [1, 'Разделение властей существует, система сдержек и противовесов реально работает'],
    [2, 'Разделение властей существует, несмотря на отдельные попытки нарушить систему сдержек и противовесов'],
    [3, 'Разделение властей существует формально, на практике система сдержек и противовесов работает плохо'],
    [4, 'Разделения властей нет, система сдержек и противовесов не работает'],
    HARD_TO_SAY_CHOICE

]
INDEPENDENT_JUD_CHOICES = [
    [1, 'Суды независимы от других общественных институтов и некоррумпированы'],
    [2,
     'Суды в основном независимы, хотя иногда подвержены воздействию других общественных институтов и бывают случаи коррупции'],
    [3,
     'Независимость судов в значительной степени подорвана: они находятся во влиянием других общественных институтов и коррупции'],
    [4, 'Независимых судов в нашей стране нет'],
    HARD_TO_SAY_CHOICE

]

CORRUPTION_CHOICES = [
    [1, 'Коррупция строго преследуется в соответствии с законом и подвергается публичному осуждению'],
    [2,
     'Коррупция в целом преследуется по закону и осуждается, однако иногда вовлеченным в нее людям удается найти лазейки и уйти от ответственности'],
    [3, 'Коррупция недостаточно преследуется по закону, и иногда подвергается публичному осуждению'],
    [4, 'Коррупция практически безнаказанна, и не осуждается публично'],
    HARD_TO_SAY_CHOICE
]
CIVIL_RIGHTS_CHOICES = [
    [1, 'Гражданские права эффективно защищены законом, а их нарушение карается'],
    [2, 'Гражданские права охраняются законом, но защита недостаточна, и нарушение этих прав не всегда преследуется'],
    [3,
     'Гражданские права обозначены в законе, но на практике нарушаются, и механизмы их защиты, как правило, неэффективны'],
    [4, 'Гражданские права систематически нарушаются, и механизмы их защиты отсутствуют'],
    HARD_TO_SAY_CHOICE
]

HAPPY_CHOICES = [
    [0, 'Несчастливый человек'],
    [1, 'Счастливый человек'],
]
RELATIVE_HAPPY_CHOICES = [
    [1, '1 - Менее счастливы чем они'],
    [2, '2'],
    [3, '3'],
    [4, '4 - В среднем так же счастлив, как и они'],
    [5, '5'],
    [6, '6'],
    [7, '7 - Более счастлив чем они']
]

AgreementChoices = [
    [0, 'Совершенно согласен'],
    [1, 'Скорее согласен'],
    [2, 'Отчасти согласен, отчасти нет'],
    [3, 'Скорее не согласен'],
    [4, 'Совершенно не согласен'],]

PARTY_CHOICES = [
    [1, 'Единая Россия'],
    [2, 'КПРФ'],
    [3, 'ЛДПР'],
    [4, 'Справедливая Россия'],
    [5, 'Яблоко'],
    [6, 'Другая партия'],
    [7, 'В России нет партии, которой  я симпатизирую'],
    [8, 'Я не интересуюсь политикой'],
    [333, 'Я не гражданин РФ'],
    HARD_TO_SAY_CHOICE
]

TRUST_CHOICES = [
    (1, "Большинству можно доверять"),
    (2, "Нужно быть очень осторожными в отношениях с людьми"),
]

EDUCATION_CHOICES = [
    (0, 'Средняя школа'),
    (1, 'Среднее профессиональное образование'),
    (2, 'Незаконченное высшее образование'),
    (3, 'Высшее образование'),
    (4, 'Два и более диплома / Ученая степень')]
AGE_CHOICES = [(0, "Младше 18 лет"),
               (1, "18-24 года"),
               (2, "25-34 года"),
               (3, "35-44 года"),
               (4, "45-54 года"),
               (5, "55-64 года"),
               (6, "65 лет и старше"),
               ]

GENDER_CHOICES = [
    (0, "Мужской"),
    (1, "Женский")

]

INCOME_CHOICES = [
    (0, 'Не хватает денег даже на еду'),
    (1, 'Хватает на еду, но не хватает на покупку одежды и обуви'),
    (2, 'Хватает на одежду и обувь, но не хватает на покупку мелкой бытовой техники'),
    (3,
     'Хватает денег на небольшие покупки, но покупка дорогих вещей (компьютера, стиральной машины, холодильника) требует накоплений или кредита'),

    (4, 'Хватает денег на покупки для дома, но на покупку машины, дачи, квартиры необходимо копить или брать кредит'),
    (5, 'Можем позволить себе любые покупки без ограничений и кредитов')]

RISK_CHOICES = range(0, 11)

MARITAL_CHOICES = [(0, 'Не женаты/не замужем'),
                   (1, 'Женаты/замужем'),
                   (2, 'В отношениях, но официально не состоите в браке'),
                   (3, 'Разведены'),
                   (4, 'Живете отдельно от супруга/и'),
                   (5, 'Вдовец/Вдова')]
EMPLOYMENT_CHOICES = [
    (0, "Трудоустроен (полный рабочий день)"),
    (1, "Трудоустроен (частичная занятость)"),
    (2, "Самозанятый"),
    (3, "Не работаю и ищу работу"),
    (4, "Не работаю (на пенсии)"),
    (5, "Не работаю (по состоянию здоровья)"),
    (6, 'Не работаю (другое)'),
    (7, "Предпочитаю не отвечать"),
]
