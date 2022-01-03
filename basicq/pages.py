from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from matcher.generic_pages import Page
from .models import Constants
from django.shortcuts import redirect
from django.utils.timezone import now
from django_user_agents.utils import get_user_agent


class SES(Page):
    def get(self, *args, **kwargs):
        user_agent = get_user_agent(self.request)
        self.player.useragent_is_mobile = user_agent.is_mobile
        self.player.useragent_is_bot = user_agent.is_bot
        self.player.useragent_browser_family = user_agent.browser.family
        self.player.useragent_os_family = user_agent.os.family
        self.player.useragent_device_family = user_agent.device.family
        return super().get()

    def is_displayed(self):
        if self.player.start_time is None:
            current_time = now()
            self.participant.vars['global_start_time'] = current_time
            self.player.start_time = current_time
            self.player.start_timestamp = current_time.timestamp()
        return True
    def vars_for_template(self):
        ru =self.session.config.get('language') == 'ru'
        return dict(gender='Укажите ваш пол' if ru else 'How do you describe yourself?',
                    age='Сколько вам лет?' if ru else 'How old are you?',
                    ru=ru)
    form_model = 'player'
    form_fields = ['age', 'gender',
                   ]


class Last(Page):
    def vars_for_template(self):
        return dict(toloka=self.session.config.get('for_toloka'))


class FinalForProlific(Page):
    def is_displayed(self):
        return self.session.config.get('for_prolific')

    def get(self):
        return redirect(self.session.config.get('prolific_redirect_url'))


page_sequence = [
    SES,
    FinalForProlific,
    Last
]
