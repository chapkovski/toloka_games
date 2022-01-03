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
from django.utils.timezone import now
from django.db.models import DateTimeField
author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'intro_matcher'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # user agent block
    useragent_is_mobile = models.BooleanField()
    useragent_is_bot = models.BooleanField()
    useragent_browser_family = models.StringField()
    useragent_os_family = models.StringField()
    useragent_device_family = models.StringField()
    # user agent block END
    global_start_time = DateTimeField(null=True)
    understand_rules = models.BooleanField(label='Я подтверждаю что понимаю правила игры.',
                                           widget=widgets.CheckboxInput)
    understand_drop = models.BooleanField(
        label='Я понимаю, что если другой участник покинет исследование, то мое участие также завершится.',
        widget=widgets.CheckboxInput)
