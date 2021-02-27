from django.db import models

from soft_remover.models import SoftRemovableModel, SoftRestorableModel


class SimpleRM(SoftRemovableModel):
    name = models.CharField(max_length=32)


class UniqueTogetherRM(SoftRemovableModel):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('category', 'name', 'remver')


class ManyUniqueTogetherRM(SoftRemovableModel):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    tag = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('category', 'name', 'remver'), ('category', 'tag', 'remver'))


class SimpleRS(SoftRestorableModel):
    name = models.CharField(max_length=32)


class UniqueTogetherRS(SoftRestorableModel):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('category', 'name')


class ManyUniqueTogetherRS(SoftRestorableModel):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    tag = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('category', 'name'), ('category', 'tag'))


class RestoreTogetherRS(SoftRestorableModel):
    name = models.CharField(max_length=32)

    class MetaSoftRemover:
        restore_together = ('name',)


class ManyRestoreTogetherRS(SoftRestorableModel):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class MetaSoftRemover:
        restore_together = ('category', 'name',)
