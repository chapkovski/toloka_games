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

from q import choices
doc = """
 Post-survey Questionnaire 
"""


class Constants(BaseConstants):
    name_in_url = 'questionnaire'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comment = models.LongStringField(
        label='Мы были бы вам признательны за любые комментарии об этом исследовании: было ли все ясно в инструкциях? Долго ли вам приходилось ждать '
              'других участников? Были ли какие-то технические сложности?'
    )
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


