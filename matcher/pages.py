from ._builtin import  WaitPage
from matcher.generic_pages import Page
from django.utils.timezone import now



class FirstWP(WaitPage):
    template_name = 'matcher/FirstWP.html'
    group_by_arrival_time = True

    def _get_wait_page(self):
        self.participant.vars.setdefault('first_wp_arrival', now())
        return super()._get_wait_page()

    def is_displayed(self):
        return self.round_number == 1




class ResultsWaitPage(WaitPage):
    pass





page_sequence = [
    FirstWP,

]
