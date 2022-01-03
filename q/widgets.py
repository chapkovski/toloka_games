from otree.forms.widgets import RadioSelect


class OtherRadioSelect(RadioSelect):
    template_name = 'q/widgets/radio.html'

    def __init__(self, other=None, *args, **kwargs):
        self.other = other
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        c = super().get_context(name, value, attrs)
        c['other'] = self.other
        return c


from django import forms


class LikertWidget(forms.RadioSelect):
    template_name = 'q/widgets/likert.html'

    class Media:
        css = {
            'all': ('likert.css',)
        }

    def __init__(self, quote, label, left, right, *args, **kwargs):
        self.quote = quote
        self.label = label
        self.left = left
        self.right = right

        super().__init__(*args, **kwargs)

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)

        context.update({'choices': self.choices,
                        'quote': self.quote,
                        'label': self.label,
                        'left': self.left,
                        'right': self.right,
                        'optimal_width': round(85 / len(self.choices), 2),

                        })
        return context


class BlockedCheckbox(forms.RadioSelect):
    template_name = 'q/widgets/blocked_checkbox.html'


    class Media:
        css = {
            'all': ('blocked_checkbox.css',
                    "https://cdn.jsdelivr.net/npm/pretty-checkbox@3.0/dist/pretty-checkbox.min.css")
        }
        js = ('https://cdn.jsdelivr.net/npm/vue@2.6.11',
              'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.15/lodash.core.min.js',
              "https://cdn.jsdelivr.net/npm/pretty-checkbox-vue@1.1/dist/pretty-checkbox-vue.min.js")

    def __init__(self, label, choices, blocked, *args, **kwargs):
        self.label = label
        self.inner_choices = choices
        self.blocked = blocked
        super().__init__(*args, **kwargs)

    def choices_for_vue(self):
        return [dict(value=int(value), text=str(text)) for value, text in self.inner_choices]

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)

        context.update(dict(inner_choices=self.choices_for_vue(), blocked=self.blocked, label=self.label))
        return context
