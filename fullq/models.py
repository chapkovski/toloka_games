from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from django.db.models import DateTimeField
from fullq import choices

author = 'Philipp Chapkovski, HSE-Moscow'

doc = """
Large-sample survey for toloka participants
"""


class Constants(BaseConstants):
    name_in_url = 'fullq'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # toloka block
    toloka_hours_per_week = models.IntegerField(label='Сколько в среднем часов в неделю вы работаете в Толоке?')
    toloka_main_job = models.BooleanField(label='Является ли Толока основным местом вашей работы?',
                                          choices=((False, 'Нет'), (True, 'Да')))
    toloka_income_share = models.IntegerField(
        label='Какую часть вашего общего заработка составляет ваш доход на Толоке',
        widget=widgets.RadioSelect,
        choices=[
            (0, "несущественную"),
            (1, "немного меньше половины общего дохода"),
            (2, "немного больше половины общего дохода"),
            (3, "очень существенную"),
            (4, "Толока обеспечивает весь мой доход")

        ])
    toloka_num_surveys = models.IntegerField(
        label='В течение месяца в среднем в скольких социологических исследованиях (опросах и тому подобное) вы'
              ' принимаете участие?',
        widget=widgets.RadioSelect,
        choices=((0, 'Вообще не принимаю участие в социологических исследованиях'),
                 (1, '1-2 в месяц'),
                 (2, '3-5 в месяц'),
                 (3, 'Больше 5 в месяц'),
                 (4, 'Другое'),
                 choices.HARD_TO_SAY_CHOICE))
    toloka_wage_per_hour = models.IntegerField(
        label='Сколько в среднем вы зарабатываете в час, выполняя задания на Толоке (в долларах США)?',
    )
    # toloka block END
    # COVID BLOCK

    covid_sick_ego = models.IntegerField(label="Вы сами болели коронавирусом?",
                                         choices=choices.COVID_SICK_EGO_CHOICES,
                                         widget=widgets.RadioSelect)


    covid_sick_nearby = models.IntegerField(
        label="В вашем ближайшем кругу (семья, друзья) болел или болеет ли кто-то коронавирусом?",
        choices=choices.COVID_SICK_NEARBY_CHOICES,
        widget=widgets.RadioSelect)

    covid_vaccine_must = models.IntegerField(label="Насклько вы согласны или не согласны со следующим утверждением: "
                                                   "<br> <i>Чтобы остановить эпидемию коронавируса, прививка от COVID-19 должна быть обязательной.</i>",
                                          choices=choices.AgreementChoices,
                                          widget=widgets.RadioSelect)

    covid_vaccine = models.IntegerField(label='Вы уже привились или планируете привиться от коронавируса?',
                                        choices=choices.COVID_VACCINE,
                                        widget=widgets.RadioSelect
                                        )
    # COVID BLOCK END
    # politics
    politics_party = models.PositiveIntegerField(
        label="""Сторонником какой политической партии вы являетесь, или по крайней мере,симпатизируете ей?""",
        choices=choices.PARTY_CHOICES,
        widget=widgets.RadioSelect
    )
    politics_duma_vote = models.IntegerField(label='Головали ли вы на выборах в Государственную Думу в этом году?',
                                             choices=[
                                                 (0, 'Нет'),
                                                 (1, 'Да'),
                                                 (333, 'Я не гражданин РФ'),
                                                 choices.HARD_TO_SAY_CHOICE
                                             ],
                                             widget=widgets.RadioSelect
                                             )
    politics_president_vote = models.IntegerField(
        label='Если бы выборы Президента РФ прошли в ближайшее воскресенье, за кого бы вы проголосовали?',
        choices=[
            (0, 'Владимир Путин'),
            (1, 'Геннадий Зюганов'),
            (2, 'Владимир Жириновский'),
            (3, 'Сергей Шойгу'),
            (4, 'Алексей Навальный'),
            (5, 'Другой кандидат'),
            (111, 'Не пошел бы голосовать'),
            (333, 'Я не гражданин РФ'),
            choices.HARD_TO_SAY_CHOICE
        ],
        widget=widgets.RadioSelect
    )
    # politics END

    # user agent block
    useragent_is_mobile = models.BooleanField()
    useragent_is_bot = models.BooleanField()
    useragent_browser_family = models.StringField()
    useragent_os_family = models.StringField()
    useragent_device_family = models.StringField()
    # user agent block END
    global_start_time = DateTimeField(null=True)

    age = models.IntegerField(label='Укажите ваш возраст:', choices=choices.AGE_CHOICES, widget=widgets.RadioSelect)
    general_trust = models.IntegerField(label="""
        Если говорить в целом, Вы считаете, что большинству людей можно доверять или нужно быть очень
        осторожными в отношениях с людьми?""", choices=choices.TRUST_CHOICES)
    education = models.IntegerField(
        label="Какой самый высокий уровень школы вы закончили или какую высшую степень вы получили?",
        choices=choices.EDUCATION_CHOICES, widget=widgets.RadioSelect)
    gender = models.IntegerField(label='Укажите ваш пол:',
                                 choices=choices.GENDER_CHOICES, widget=widgets.RadioSelect)
    marital = models.IntegerField(label='В настоящий момент вы:',
                                  choices=choices.MARITAL_CHOICES, widget=widgets.RadioSelect)
    employment = models.IntegerField(label='В настоящий момент вы:',
                                     choices=choices.EMPLOYMENT_CHOICES, widget=widgets.RadioSelect)
    income = models.IntegerField(
        label="Какое высказывание наиболее точно описывает финансовое положение вашей семьи?",
        choices=choices.INCOME_CHOICES,
        widget=widgets.RadioSelect()
    )
    nationality = models.IntegerField(label='Укажите вашу национальность',
                                      widget=widgets.RadioSelect(),
                                      choices=(
                                          (0, 'Россия'),
                                          (1, 'Украина'),
                                          (2, 'Казахстан'),
                                          (3, 'Молдова'),
                                          (4, 'Беларусь'),
                                          (5, 'Другая страна бывшего СССР'),
                                          (6, 'Другая'),
                                          (9999, 'Предпочитаю не отвечать')
                                      ))
    country = models.IntegerField(label='В какой стране вы на данные момент проживаете?',
                                  widget=widgets.RadioSelect(),
                                  choices=(
                                      (0, 'Россия'),
                                      (1, 'Украина'),
                                      (2, 'Казахстан'),
                                      (3, 'Молдова'),
                                      (4, 'Беларусь'),
                                      (5, 'Другая страна бывшего СССР'),
                                      (6, 'Другая'),
                                      (9999, 'Предпочитаю не отвечать')
                                  ))

    # general risk, trust, political, religion
    general_risk = models.IntegerField(label='Укажите, пожалуйста, насколько Вы в целом любите рисковать', )
    general_trust = models.IntegerField(label="""
        Если говорить в целом, Вы считаете, что большинству людей можно доверять или нужно быть очень
        осторожными в отношениях с людьми?""", choices=choices.TRUST_CHOICES)
    religion = models.IntegerField(label="""
              Насколько сильно вы верите в существование Бога? (укажите свой ответ в диапазоне от 1 = совсем нет до 5 = очень сильно)
              """, choices=range(1, 6), widget=widgets.RadioSelectHorizontal)
    political = models.IntegerField(label="""
              Ниже представлена 7-балльная шкала, на которой политические взгляды, которых могут придерживаться люди, расположены от крайне либеральных (слева) до крайне консервативных (справа). Куда бы вы поставили себя на этой шкале?
              """, choices=range(0, 8), widget=widgets.RadioSelectHorizontal)

    # happyness
    happy = models.BooleanField(
        label="""В целом я могу сказать, что я""",
        choices=choices.HAPPY_CHOICES,
        widget=widgets.RadioSelectHorizontal()
    )

    happy_relative = models.PositiveIntegerField(
        label="""По сравнению с большинством окружающих вас людей, вы""",
        choices=choices.RELATIVE_HAPPY_CHOICES,
        widget=widgets.RadioSelect()
    )
