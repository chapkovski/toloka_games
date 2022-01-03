from otree.api import Currency as c, currency_range
from matcher.generic_pages import Page
from .models import Constants

from django.utils.timezone import now


class BlockedByOther(Page):
    def is_displayed(self):
        if self.participant.vars.get('alter_block'):
            self.player.global_finish_time = now()
            self.player.total_time_in_study = (
                    now() - self.participant.vars.get('global_start_time', now())).total_seconds()
        self.player.payable = self.participant.vars.get('payable')
        return self.participant.vars.get('alter_block')


class Last(Page):
    def is_displayed(self):
        self.player.global_finish_time = now()
        self.player.total_time_in_study = (
                now() - self.participant.vars.get('global_start_time', now())).total_seconds()

        self.player.payable = self.participant.vars.get('payable')
        return self.round_number == Constants.num_rounds


page_sequence = [BlockedByOther, Last]
