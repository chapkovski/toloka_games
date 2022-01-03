from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from django.db import models as djmodels
import random
from django.db.models.signals import post_save
from django.db.models import Sum
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'ret'
    players_per_group = None
    num_rounds = 1
    num_zero_rows = 10  # how many rows of 1/0 are generated for counting zeros RET
    len_zero_row = 5  # how long is each RET counting zero row
    ret_timeout_seconds = 12


class Subsession(BaseSubsession):
    @property
    def duration_in_sec(self):
        dur = self.session.config.get('ret_duration', 1)
        return dur * 60

    @property
    def duration_formatted(self):
        dur = self.session.config.get('ret_duration', 1)
        if dur == 1:
            return f'{dur} минуты'
        else:  # ugly fix
            return f'{dur} минут'

    def creating_session(self):
        for p in self.get_players():
            p.productivity = random.randint(0, 10)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    productivity = models.IntegerField()
    num_answered = models.IntegerField(initial=0)
    num_correct = models.IntegerField(initial=0)
    num_incorrect = models.IntegerField(initial=0)
    confirm_ret_instructions = models.BooleanField(label='Я понимаю, что от того, сколько заданий я успею сделать, зависит то, стану ли я участником А или Б',
                                           widget=widgets.CheckboxInput)
    def prepare_task(self, task):
        return {'task': task.as_dict(),
                'num_correct': self.num_correct,
                'num_incorrect': self.num_incorrect,
                }

    def process_task(self, data):
        player = self
        answer = data.get('answer')
        if not answer:

            unanswered_tasks = player.tasks.filter(answer__isnull=True)
            if unanswered_tasks.exists():
                task = unanswered_tasks.first()
            else:
                task = player.tasks.create()
            response = self.prepare_task(task)
        else:
            oldtask = player.tasks.filter(answer__isnull=True).first()
            oldtask.answer = answer
            oldtask.save()
            player.num_answered += 1
            if answer == oldtask.correct_answer:
                player.num_correct += 1
            else:
                player.num_incorrect += 1
            newtask = player.tasks.create()
            response = self.prepare_task(newtask)
            player.save()
        return {self.id_in_group: response}


class Task(djmodels.Model):
    player = djmodels.ForeignKey(to=Player, related_name='tasks', on_delete=djmodels.CASCADE)
    correct_answer = models.IntegerField()
    answer = models.IntegerField(null=True)

    def get_body(self):
        return list(self.zeroes.all().values_list('zstring', flat=True))

    def as_dict(self):
        return {
            'correct_answer': self.correct_answer,
            'body': self.get_body()}

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if not created:
            return
        for i in range(Constants.num_zero_rows):
            zstring = ''.join([str(random.choice([0, 1])) for i in range(Constants.len_zero_row)])
            instance.zeroes.create(zstring=zstring, num_zeroes=zstring.count('0'))
        instance.correct_answer = instance.zeroes.all().aggregate(Sum('num_zeroes'))['num_zeroes__sum']
        instance.save()


class ZeroString(djmodels.Model):
    task = djmodels.ForeignKey(to=Task, related_name='zeroes', on_delete=djmodels.CASCADE)
    zstring = models.LongStringField()
    num_zeroes = models.IntegerField()


post_save.connect(Task.post_create, sender=Task)
