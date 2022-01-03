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
import random

doc = """
Rock-scissors-paper
"""


class Constants(BaseConstants):
    name_in_url = 'rsp'
    players_per_group = 2
    num_others = players_per_group - 1
    num_rounds = int(environ.get('RSP_ROUNDS', 3))
    instructions_template = 'rsp/includes/instructions.html'
    currency_name = 'очков'
    time_for_decision = 60
    time_for_instructions = 90
    rsp_wp_max_waiting_time = 60
    loss = c(0)
    win = c(100)
    tie = c(50)
    payoff_matrix = {
        0: {0: tie,
            1: win,
            2: loss},
        1: {0: loss,
            1: tie,
            2: win},
        2: {0: win,
            1: loss,
            2: tie},
    }


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.session.get_participants():
                p.vars['payable_round'] = random.randint(1, Constants.num_rounds)
        for p in self.get_players():
            p.payable_round = p.participant.vars.get('payable_round')


class Group(BaseGroup):

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.intermediary_payoff = Constants.payoff_matrix[p1.decision][p2.decision]
        p2.intermediary_payoff = Constants.payoff_matrix[p2.decision][p1.decision]
        for p in self.get_players():
            p.written_outcome = p.get_written_outcome()
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

    @property
    def other(self):
        return self.get_others_in_group()[0]

    def get_written_outcome(self):
        if int(self.intermediary_payoff) == int(Constants.win):
            return 'won'
        if int(self.intermediary_payoff) == int(Constants.loss):
            return 'lost'
        if int(self.intermediary_payoff) == int(Constants.tie):
            return 'tie'

    def outcome(self):
        if int(self.intermediary_payoff) == int(Constants.win):
            return 'Вы выиграли!'
        if int(self.intermediary_payoff) == int(Constants.loss):
            return 'Вы проиграли'
        if int(self.intermediary_payoff) == int(Constants.tie):
            return 'Ничья!'

    written_outcome = models.StringField()
    decision = models.IntegerField(label='Выберите одно из:',
                                   choices=[
                                       (0, 'Камень'),
                                       (1, 'Ножницы'),
                                       (2, 'Бумага'),
                                   ],
                                   widget=widgets.RadioSelect)


def custom_export(players):
    players = players.filter(participant__label__isnull=False)
    participants = set([p.participant for p in players])
    yield ['assignment_id', 'bonus', 'msg', 'participant_code', 'session', ]
    for p in participants:
        if p.vars.get('payable'):
            payable_bonus = round(float(p.vars.get('payoff_in_real_currency', 0)), 2) or 0.01

            yield [p.label, payable_bonus, 'Спасибо за ваше участие!', p.code, p.session.code]
