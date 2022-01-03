from otree.api import Page as oTreePage, WaitPage


class Page(oTreePage):
    def get_context_data(self, **context):
        r = super().get_context_data(**context)
        r['maxpages'] = self.participant._max_page_index
        r['page_index'] = self._index_in_pages
        r['progress'] = f'{int(self._index_in_pages / self.participant._max_page_index * 100):d}'
        return r

    def title(self):
        return self.__class__.__name__

    def app_after_this_page(self, upcoming_apps):
        if self.participant.vars.get('group_blocked'):
            return "blocker"


class BlockingPage(Page):
    def is_displayed(self):
        return not self.participant.vars.get('group_blocked')


class GeneralDecisionPage(BlockingPage):
    def before_next_page(self):
        if self.timeout_happened:
            for p in self.group.get_players():
                p.participant.vars['group_blocked'] = True
            self.participant.vars['own_block'] = True
            for p in self.player.get_others_in_group():
                if not p.participant.vars.get('own_block'):
                    p.participant.vars['alter_block'] = True
                    p.participant.vars['payable'] = True


class DecisionWP(WaitPage):
    template_name = 'matcher/FirstWP.html'

    def is_displayed(self):
        return not self.participant.vars.get('group_blocked')
