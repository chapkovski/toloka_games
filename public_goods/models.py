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
from os import environ

doc = """
PGG standard
"""


class Constants(BaseConstants):
    name_in_url = 'public_goods'
    players_per_group = 3
    num_others = players_per_group - 1
    num_rounds = int(environ.get('PGG_ROUNDS', 3))
    instructions_template = 'public_goods/includes/instructions.html'
    endowment = c(100)
    multiplier = 1.5
    currency_name = 'очков'
    time_for_decision = 60
    time_for_instructions = 90
    pgg_wp_max_waiting_time = 60


import random


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.session.get_participants():
                p.vars['payable_round'] = random.randint(1, Constants.num_rounds)
        for p in self.get_players():
            p.payable_round = p.participant.vars.get('payable_round')


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution or 0 for p in self.get_players()])
        self.individual_share = (self.total_contribution * Constants.multiplier / Constants.players_per_group)
        for p in self.get_players():
            p.intermediary_payoff = (Constants.endowment - (p.contribution or 0)) + self.individual_share
            if p.payable_round == self.round_number:
                p.payoff = p.intermediary_payoff


class Player(BasePlayer):
    def current_payoff_in_real_currency(self):
        return self.intermediary_payoff.to_real_world_currency(self.session)

    def payoff_in_real_currency(self):
        return self.in_round(self.payable_round).payoff.to_real_world_currency(self.session)

    time_for_decision = models.FloatField()
    intermediary_payoff = models.CurrencyField()
    payable_round = models.IntegerField()
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment,
        label=f"Сколько вы готовы вложить в общий проект (от 0 до {Constants.endowment})?"
    )


def custom_export(players):
    players = players.filter(participant__label__isnull=False)
    participants = set([p.participant for p in players])
    yield ['assignment_id', 'bonus', 'msg', 'participant_code', 'session', ]
    for p in participants:
        if p.vars.get('payable'):
            payable_bonus = round(float(p.vars.get('payoff_in_real_currency', 0)), 2) or 0.01
            yield [p.label, payable_bonus, 'Спасибо за ваше участие!', p.code, p.session.code]
