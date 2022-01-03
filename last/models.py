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

author = 'Philipp Chapkovski'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'last'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    global_finish_time = DateTimeField(null=True)
    total_time_in_study = models.FloatField()
    payable = models.BooleanField()
