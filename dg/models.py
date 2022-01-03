import random

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
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'dg'
    players_per_group = 2
    num_rounds = 1
    endowment = 100
    time_for_decision = 60
    time_for_instructions = 90
    dg_wp_max_waiting_time = 60


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    dg_decision = models.IntegerField(label='Сколько вы пошлете участнику А (от 0 до 100 центов)?', min=0, max=100)
    dg_belief = models.IntegerField(label='Как вы думаете, сколько пошлет вам участник А (от 0 до 100 центов)?', min=0,
                                    max=100)

    def set_payoffs(self):
        try:
            dictator = self.get_player_by_role('dictator')
            recipient = self.get_player_by_role('recipient')
            dictator.payoff = Constants.endowment - (self.dg_decision or 0)
            recipient.payoff = self.dg_decision or 0
        except ValueError:
            # that's kind of a last resort safeguard against drop-outs
            for p in self.get_players():
                p.participant.vars['blocked_in_wp'] = True
                p.participant.vars['group_blocked'] = True
                p.participant.vars['alter_block'] = True

    def set_productivity(self):
        for p in self.get_players():
            p.productivity = p.participant.vars.get('productivity', 0)
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        if p1.productivity > p2.productivity:
            p1.inner_role = 'dictator'
            p2.inner_role = 'recipient'
        elif p1.productivity < p2.productivity:
            p2.inner_role = 'dictator'
            p1.inner_role = 'recipient'
        else:
            ps = [p1, p2]
            random.shuffle(ps)
            ps[0].inner_role = 'dictator'
            ps[1].inner_role = 'recipient'


class Player(BasePlayer):
    productivity = models.IntegerField()
    inner_role = models.StringField()

    @property
    def other(self):
        return self.get_others_in_group()[0]

    def desc_role(self):
        correspondence = dict(dictator='Участник А', recipient='Участник Б')
        return correspondence.get(self.role(), '')

    def role(self):
        return self.inner_role

    def payoff_in_real_currency(self):
        return self.payoff.to_real_world_currency(self.session)

    time_for_decision = models.FloatField()


def custom_export(players):
    players = players.filter(participant__label__isnull=False)
    participants = set([p.participant for p in players])
    yield ['assignment_id', 'bonus', 'msg', 'participant_code', 'session', ]
    for p in participants:
        if p.vars.get('payable'):
            payable_bonus = round(float(p.vars.get('payoff_in_real_currency', 0)), 2) or 0.01
            yield [p.label, payable_bonus, 'Спасибо за ваше участие!', p.code, p.session.code]
