from django.db import models

from soft_remover.models import SoftRemovableModel, SoftRestorableModel


class TestModelWithDefaultManager(models.Model):
    all_objects = models.Manager()

    class Meta:
        abstract = True


class SimpleRem(SoftRemovableModel, TestModelWithDefaultManager):
    name = models.CharField(max_length=32)


class SimpleUniqueRem(SoftRemovableModel, TestModelWithDefaultManager):
    name = models.CharField(max_length=32, unique=True)


class UniqueTogetherRem(SoftRemovableModel, TestModelWithDefaultManager):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('category', 'name', 'remver')


class ManyUniqueRem(SoftRemovableModel, TestModelWithDefaultManager):
    name = models.CharField(max_length=32, unique=True)
    tag = models.CharField(max_length=32, unique=True)


class ManyUniqueTogetherRem(SoftRemovableModel, TestModelWithDefaultManager):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    tag = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('category', 'name', 'remver'), ('category', 'tag', 'remver'))


class SimpleRes(SoftRestorableModel, TestModelWithDefaultManager):
    name = models.CharField(max_length=32)


class SimpleUniqueRes(SoftRestorableModel, TestModelWithDefaultManager):
    name = models.CharField(max_length=32, unique=True)


class UniqueTogetherRes(SoftRestorableModel, TestModelWithDefaultManager):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('category', 'name')


class ManyUniqueRes(SoftRestorableModel, TestModelWithDefaultManager):
    name = models.CharField(max_length=32, unique=True)
    tag = models.CharField(max_length=32, unique=True)


class ManyUniqueTogetherRes(SoftRestorableModel, TestModelWithDefaultManager):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    tag = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('category', 'name'), ('category', 'tag'))


class RestoreTogetherRes(SoftRestorableModel, TestModelWithDefaultManager):
    name = models.CharField(max_length=32)

    class MetaSoftRemover:
        restore_together = ('name',)


class ManyRestoreTogetherRes(SoftRestorableModel, TestModelWithDefaultManager):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class MetaSoftRemover:
        restore_together = ('category', 'name',)
