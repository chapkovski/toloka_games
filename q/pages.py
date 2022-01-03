from otree.api import Currency as c, currency_range
from matcher.generic_pages import BlockingPage
import json
from pprint import pprint


class Comment(BlockingPage):
    template_name = 'q/Q1.html'
    form_model = 'player'
    form_fields = ["comment"]


class TrustNRisk(BlockingPage):

    def post(self):
        try:
            data = json.loads(self.request.POST.get('surveyholder'))
            if data:
                for k, v in data.items():
                    setattr(self.player, k, v)
        except TypeError:
            pass
        return super().post()


class SES(BlockingPage):
    template_name = 'q/Q1.html'
    form_model = 'player'
    form_fields = ["gender",
                   "age",
                   "income",
                   "marital",
                   "employment",
                   "education"
                   ]


page_sequence = [
    Comment,
    TrustNRisk,
    SES,

]
