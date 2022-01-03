from matcher.generic_pages import Page


class Blocked(Page):
    def is_displayed(self):
        return self.participant.vars.get('own_block')




page_sequence = [
    Blocked,
]
