from otree.api import Currency as c, currency_range
from ._builtin import WaitPage

from .models import Constants
from django.utils.timezone import now
from matcher.generic_pages import Page, GeneralDecisionPage, DecisionWP, BlockingPage


class FirstWP(DecisionWP):
    group_by_arrival_time = True
    after_all_players_arrive = 'set_productivity'

    def is_displayed(self):
        if self.round_number == 1:
            p = self.participant
            p.vars.setdefault('dg_wp_arrival', now())
            if (now() - p.vars.get('dg_wp_arrival', now())).total_seconds() > Constants.dg_wp_max_waiting_time:
                p.vars['blocked_in_wp'] = True
                p.vars['group_blocked'] = True
                p.vars['alter_block'] = True
                return False
        return super().is_displayed() and self.round_number == 1


class RoleAnnouncement(BlockingPage):
    def get_timeout_seconds(self):
        return self.session.config.get('time_for_instructions', Constants.time_for_instructions)


class DictatorDecision(GeneralDecisionPage):
    form_model = 'group'
    form_fields = ['dg_decision']

    def is_displayed(self):
        return super().is_displayed() and self.player.role() == 'dictator'

    def vars_for_template(self):
        self.participant.vars.setdefault(f'dg_start_time_{self.round_number}', now())
        return dict()

    def get_timeout_seconds(self):
        return self.session.config.get('time_for_decision', Constants.time_for_decision)

    def before_next_page(self):
        super().before_next_page()
        self.player.time_for_decision = (
                now() - self.participant.vars.get(f'dg_start_time_{self.round_number}',
                                                  now())).total_seconds()


class RecipientBelief(GeneralDecisionPage):
    form_model = 'group'
    form_fields = ['dg_belief']

    def is_displayed(self):
        return super().is_displayed() and self.player.role() == 'recipient'

    def vars_for_template(self):
        self.participant.vars.setdefault(f'dg_start_time_{self.round_number}', now())
        return dict()

    def get_timeout_seconds(self):
        return self.session.config.get('time_for_decision', Constants.time_for_decision)

    def before_next_page(self):
        super().before_next_page()
        self.player.time_for_decision = (
                now() - self.participant.vars.get(f'dg_start_time_{self.round_number}',
                                                  now())).total_seconds()


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(BlockingPage):
    def before_next_page(self):
        self.participant.vars['payable'] = True
        self.participant.vars['payoff_in_real_currency'] = self.player.payoff_in_real_currency()

page_sequence = [
    FirstWP,
    RoleAnnouncement,
    DictatorDecision,
    RecipientBelief,
    ResultsWaitPage,
    Results
]
