from django.db import models
from django.utils.translation import gettext_lazy as _


class Person(models.Model):
    class GradeChoice(models.TextChoices):
        fifth_C = '5С', _('5С')
        sixth_C = '6С', _('6С')
        sixth_T = '6Т', _('6Т')
        seventh_C = '7С', _('7С')
        eighth_C = '8С', _('8С')
        ninth_C = '9С', _('9С')
        tenth_C = '10С', _('10С')
        Teachers = 'Учитель', _('Учитель')

    class StatusChoice(models.TextChoices):
        entered = 'Вошел', _('Вошел')
        left = 'Вышел', _('Вышел')
        unknown = 'Неизвестно', _('Неизвестно')

    class ReasonChoice(models.TextChoices):
        unknown = 'Неизвестно', _('Неизвестно')
        illness = 'Болеет', _('Болеет')
        quarantine = 'Карантин', _('Карантин')
        family = 'Семейные-обстоятельства', _('Семейные-обстоятельства')
        other = 'Другое', _('Другое')


    grade = models.CharField(_('Grade'), max_length=50, choices=GradeChoice.choices, default=GradeChoice.fifth_C)
    name = models.CharField(_('LFM Names'), max_length=50)
    time = models.TimeField(_('Time'))
    status = models.CharField(_('Status'), max_length=50, choices=StatusChoice.choices, default=StatusChoice.entered)
    reason = models.CharField(_('Reason'), max_length=50, choices=ReasonChoice.choices, default=ReasonChoice.unknown)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
