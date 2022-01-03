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

author = 'Philipp Chapkovski'

doc = """
Matching app
"""
from django.db.models import DateTimeField


class Constants(BaseConstants):
    name_in_url = 'matcher'
    players_per_group = None
    num_rounds = 1
    max_waiting_time = 60
    wp_update_freq = 10


class Subsession(BaseSubsession):
    def group_by_arrival_time_method(self, waiting_players):
        group_size = self.session.config.get('group_size')
        max_waiting_time = self.session.config.get('matching_waiting_time')
        if len(waiting_players) >= group_size:
            matched_group = waiting_players[:group_size]
            matched_group = sorted(matched_group, key=lambda x: x.participant.vars.get('productivity', 0), reverse=True)
            for w in matched_group:
                w.matching_time = (now() - w.participant.vars.get('first_wp_arrival', now())).total_seconds()
            return matched_group
        for i in waiting_players:
            if (now() - i.participant.vars.get('first_wp_arrival', now())).total_seconds() > max_waiting_time:
                i.blocked_in_wp = True
                i.matching_time = (now() - i.participant.vars.get('first_wp_arrival', now())).total_seconds()
                i.participant.vars['blocked_in_wp'] = True
                i.participant.vars['group_blocked'] = True
                i.participant.vars['alter_block'] = True
                i.participant.vars['payable'] = True
                return [i]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    blocked_in_wp = models.BooleanField(initial=False)
    matching_time = models.FloatField()
