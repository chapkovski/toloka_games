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

from basicq import choices

import random

author = 'Philipp Chapkovski, HSE-Moscow'

doc = """
Your app description
"""



class Constants(BaseConstants):
    name_in_url = 'basicq'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


from django.db.models import DateTimeField


class Player(BasePlayer):
    start_time = DateTimeField(null=True)
    start_timestamp = models.FloatField()
    # user agent block
    useragent_is_mobile = models.BooleanField()
    useragent_is_bot = models.BooleanField()
    useragent_browser_family = models.StringField()
    useragent_os_family = models.StringField()
    useragent_device_family = models.StringField()
    # user agent block END
    age = models.StringField(label='How old are you?',

                             widget=widgets.RadioSelect)
    gender = models.StringField(label='How do you describe yourself?',

                                widget=widgets.RadioSelect)
    def age_choices(self):
        if self.session.config.get('language') == 'ru':
            return choices.AGE_CHOICES_RU
        return choices.AGE_CHOICES
    def gender_choices(self):
        if self.session.config.get('language') == 'ru':
            return choices.GENDER_CHOICES_RU
        return choices.GENDER_CHOICES