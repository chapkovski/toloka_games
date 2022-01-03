from otree.api import Currency as c, currency_range
from ._builtin import WaitPage
from matcher.generic_pages import Page
from .models import Constants


class Instructions(Page):
    form_fields = ['confirm_ret_instructions']
    form_model = 'player'


class RET(Page):
    live_method = 'process_task'

    def get_timeout_seconds(self):
        return self.subsession.duration_in_sec

    def vars_for_template(self):
        r = dict(min_digits=0,
                 max_digits=Constants.num_zero_rows * Constants.len_zero_row
                 )
        return r

    def before_next_page(self):
        self.player.productivity = self.player.num_correct
        self.participant.vars['productivity'] = self.player.productivity


class SecondPartAnnouncement(Page):
    timeout_seconds = 30
    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['group_blocked'] = True
            self.participant.vars['own_block'] = True

    def app_after_this_page(self, upcoming_apps):
        if self.participant.vars.get('group_blocked'):
            return "blocker"


page_sequence = [
    Instructions,
    RET,
    SecondPartAnnouncement,
]
