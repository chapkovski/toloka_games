from ._builtin import WaitPage
from matcher.generic_pages import Page, GeneralDecisionPage, DecisionWP, BlockingPage
from otree.api import Currency as c, currency_range
from .models import Constants
from django.utils import timezone
from django.utils.timezone import now

class FirstWP(DecisionWP):
    group_by_arrival_time = True

    def is_displayed(self):
        if self.round_number == 1:
            p = self.participant
            p.vars.setdefault('rsp_wp_arrival', now())
            if (now() - p.vars.get('rsp_wp_arrival', now())).total_seconds() > Constants.rsp_wp_max_waiting_time:
                p.vars['blocked_in_wp'] = True
                p.vars['group_blocked'] = True
                p.vars['alter_block'] = True
                return False
        return super().is_displayed() and self.round_number == 1


class GeneralIntro(BlockingPage):
    def get_timeout_seconds(self):
        return self.session.config.get('time_for_instructions', Constants.time_for_instructions)

    def is_displayed(self):
        return self.round_number == 1 and super().is_displayed()


class Introduction(BlockingPage):
    def get_timeout_seconds(self):
        return self.session.config.get('time_for_instructions', Constants.time_for_instructions)

    def is_displayed(self):
        return self.round_number == 1 and super().is_displayed()


class Decision(GeneralDecisionPage):

    def vars_for_template(self):
        self.participant.vars.setdefault(f'start_time_{self.round_number}', timezone.now())
        return dict()

    def get_timeout_seconds(self):
        return self.session.config.get('time_for_decision', Constants.time_for_decision)

    def before_next_page(self):
        self.player.time_for_decision = (
                    timezone.now() - self.participant.vars.get(f'start_time_{self.round_number}',
                                                               timezone.now())).total_seconds()

    form_model = 'player'
    form_fields = ['decision']


class ResultsWaitPage(DecisionWP):
    after_all_players_arrive = 'set_payoffs'
    body_text = "Ждите решения второго участника"


class Results(BlockingPage):
    def get_timeout_seconds(self):
        return self.session.config.get('time_for_decision', Constants.time_for_decision)


class FinalResults(BlockingPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and super().is_displayed()

    def before_next_page(self):
        self.participant.vars['payable'] = True
        self.participant.vars['payoff_in_real_currency'] = self.player.payoff_in_real_currency()


page_sequence = [
    FirstWP,
    GeneralIntro,
    Introduction,
    Decision,
    ResultsWaitPage,
    Results,
    FinalResults
]
