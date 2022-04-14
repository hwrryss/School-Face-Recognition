from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class MainTable(models.Model):
    class GradeChoice(models.TextChoices):
        fifth_C = '5C', _('5C')
        sixth_C = '6C', _('6C')
        sixth_T = '6T', _('6T')
        seventh_C = '7C', _('7C')
        eighth_C = '8C', _('8C')
        ninth_C = '9C', _('9C')
        tenth_C = '10C', _('10C')
        Teachers = 'Teachers', _('Teachers')

    class StatusChoice(models.TextChoices):
        entered = 'Entered', _('Entered')
        left = 'Left', _('Left')

    grade = models.CharField(_('Grade'), max_length=50, choices=GradeChoice.choices, default=GradeChoice.fifth_C)
    name = models.CharField(_('LFM Names'), max_length=50)
    time = models.TimeField(_('Time'), auto_now=True)
    status = models.CharField(_('Status'), max_length=50, choices=StatusChoice.choices, default=StatusChoice.entered)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Main Table'
        verbose_name_plural = 'Main Tables'
