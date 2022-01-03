from otree.api import Currency as c, currency_range
from ._builtin import Page as oTreePage, WaitPage
import json
from django.utils.timezone import now
from django_user_agents.utils import get_user_agent


class Page(oTreePage):
    template_name = 'fullq/Q1.html'

    def get_context_data(self, **context):
        r = super().get_context_data(**context)
        r['maxpages'] = self.participant._max_page_index
        r['page_index'] = self._index_in_pages
        r['progress'] = f'{int(self._index_in_pages / self.participant._max_page_index * 100):d}'
        return r

    def title(self):
        return self.__class__.__name__


class Intro(Page):
    template_name = 'fullq/Intro.html'

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


class Toloka(Page):
    form_model = 'player'
    form_fields = [
        "toloka_hours_per_week",
        "toloka_main_job",
        "toloka_income_share",
        "toloka_num_surveys",
        "toloka_wage_per_hour",
    ]


class Covid(Page):
    form_model = 'player'
    form_fields = [
        "covid_sick_ego",
        "covid_sick_nearby",
        "covid_vaccine_must",
        "covid_vaccine"
    ]


class Politics(Page):
    form_model = 'player'
    form_fields = ['politics_party',
                   'politics_duma_vote',
                   'politics_president_vote']


class TrustNRisk(Page):
    template_name = 'fullq/TrustNRisk.html'

    def post(self):
        try:
            data = json.loads(self.request.POST.get('surveyholder'))
            if data:
                for k, v in data.items():
                    setattr(self.player, k, v)
        except TypeError:
            pass
        return super().post()


class SES(Page):
    template_name = 'fullq/Q1.html'
    form_model = 'player'
    form_fields = ["happy",
                   "happy_relative",
                   "gender",
                   "age",
                   "income",
                   "nationality",
                   "country",
                   "marital",
                   "employment",
                   "education"
                   ]


page_sequence = [
    Intro,
    Toloka,
    Covid,
    Politics,
    TrustNRisk,
    SES
]
