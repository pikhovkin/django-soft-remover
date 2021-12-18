from django.db import models

from soft_remover.models import SoftRemovableModel, SoftRestorableModel


class SimpleRem(SoftRemovableModel):
    name = models.CharField(max_length=32)


class SimpleUniqueRem(SoftRemovableModel):
    name = models.CharField(max_length=32, unique=True)


class UniqueTogetherRem(SoftRemovableModel):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('category', 'name', 'remver')


class ManyUniqueRem(SoftRemovableModel):
    name = models.CharField(max_length=32, unique=True)
    tag = models.CharField(max_length=32, unique=True)


class ManyUniqueTogetherRem(SoftRemovableModel):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    tag = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('category', 'name', 'remver'), ('category', 'tag', 'remver'))


class SimpleRes(SoftRestorableModel):
    name = models.CharField(max_length=32)


class SimpleUniqueRes(SoftRestorableModel):
    name = models.CharField(max_length=32, unique=True)


class UniqueTogetherRes(SoftRestorableModel):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('category', 'name')


class ManyUniqueRes(SoftRestorableModel):
    name = models.CharField(max_length=32, unique=True)
    tag = models.CharField(max_length=32, unique=True)


class ManyUniqueTogetherRes(SoftRestorableModel):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    tag = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('category', 'name'), ('category', 'tag'))


class RestoreTogetherRes(SoftRestorableModel):
    name = models.CharField(max_length=32)

    class MetaSoftRemover:
        restore_together = ('name',)


class ManyRestoreTogetherRes(SoftRestorableModel):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class MetaSoftRemover:
        restore_together = ('category', 'name',)
