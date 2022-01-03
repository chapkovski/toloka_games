from otree.api import Currency as c, currency_range
from ._builtin import Page as oTreePage, WaitPage
from .models import Constants
from django.utils.timezone import now
from django_user_agents.utils import get_user_agent
class Page(oTreePage):
    def get_context_data(self, **context):
        r = super().get_context_data(**context)
        r['maxpages'] = self.participant._max_page_index
        r['page_index'] = self._index_in_pages
        r['progress'] = f'{int(self._index_in_pages / self.participant._max_page_index * 100):d}'
        return r

    def title(self):
        return self.__class__.__name__


class Intro(Page):
    def get(self, *args, **kwargs):
        user_agent = get_user_agent(self.request)
        self.player.useragent_is_mobile = user_agent.is_mobile
        self.player.useragent_is_bot = user_agent.is_bot
        self.player.useragent_browser_family = user_agent.browser.family
        self.player.useragent_os_family = user_agent.os.family
        self.player.useragent_device_family = user_agent.device.family
        return super().get()

    def is_displayed(self):
        if self.player.global_start_time is None:
            self.participant.vars['global_start_time'] = now()
            self.player.global_start_time = now()
        return True
    form_model = 'player'
    form_fields = [ 'understand_drop']




page_sequence = [Intro]
