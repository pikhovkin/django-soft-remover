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


class SimpleUniqueRem2(SoftRemovableModel, TestModelWithDefaultManager):
    name = models.CharField(max_length=32)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(name__isnull=False), name='dsr_surem_name_not_null'),
            models.UniqueConstraint(fields=('name',), name='dsr_surem_name'),
        ]


class UniqueTogetherRem(SoftRemovableModel, TestModelWithDefaultManager):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('category', 'name', 'remver')


class UniqueTogetherRem2(SoftRemovableModel, TestModelWithDefaultManager):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(value__lte=32768), name='dsr_utrem_value_lte_32768'),
            models.UniqueConstraint(fields=['category', 'name', 'remver'], name='dsr_utrem_category_name_remver'),
            models.CheckConstraint(check=models.Q(value__gte=0), name='dsr_utrem_value_gte_0'),
        ]


class ManyUniqueRem(SoftRemovableModel, TestModelWithDefaultManager):
    name = models.CharField(max_length=32, unique=True)
    tag = models.CharField(max_length=32, unique=True)


class ManyUniqueRem2(SoftRemovableModel, TestModelWithDefaultManager):
    name = models.CharField(max_length=32, unique=True)
    tag = models.CharField(max_length=32)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(name__isnull=False), name='dsr_murem_name_not_null'),
            models.UniqueConstraint(fields=('tag',), name='dsr_murem_tag'),
        ]


class ManyUniqueTogetherRem(SoftRemovableModel, TestModelWithDefaultManager):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    tag = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('category', 'name', 'remver'), ('category', 'tag', 'remver'))


class ManyUniqueTogetherRem2(SoftRemovableModel, TestModelWithDefaultManager):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    tag = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('category', 'tag', 'remver')
        constraints = [
            models.CheckConstraint(check=models.Q(value__lte=32768), name='dsr_mutrem_value_lte_32768'),
            models.UniqueConstraint(fields=['category', 'name', 'remver'], name='dsr_mutrem_category_name_remver'),
            models.CheckConstraint(check=models.Q(value__gte=0), name='dsr_mutrem_value_gte_0'),
        ]


class SimpleRes(SoftRestorableModel, TestModelWithDefaultManager):
    name = models.CharField(max_length=32)


class SimpleUniqueRes(SoftRestorableModel, TestModelWithDefaultManager):
    name = models.CharField(max_length=32, unique=True)


class SimpleUniqueRes2(SoftRestorableModel, TestModelWithDefaultManager):
    name = models.CharField(max_length=32)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(name__isnull=False), name='dsr_sures_name_not_null'),
            models.UniqueConstraint(fields=('name',), name='dsr_sures_name'),
        ]


class UniqueTogetherRes(SoftRestorableModel, TestModelWithDefaultManager):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('category', 'name')


class UniqueTogetherRes2(SoftRestorableModel, TestModelWithDefaultManager):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(value__lte=32768), name='dsr_utres_value_lte_32768'),
            models.UniqueConstraint(fields=['category', 'name'], name='dsr_utres_category_name_remver'),
            models.CheckConstraint(check=models.Q(value__gte=0), name='dsr_utres_value_gte_0'),
        ]


class ManyUniqueRes(SoftRestorableModel, TestModelWithDefaultManager):
    name = models.CharField(max_length=32, unique=True)
    tag = models.CharField(max_length=32, unique=True)


class ManyUniqueRes2(SoftRestorableModel, TestModelWithDefaultManager):
    name = models.CharField(max_length=32, unique=True)
    tag = models.CharField(max_length=32)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(name__isnull=False), name='dsr_mures_name_not_null'),
            models.UniqueConstraint(fields=('tag',), name='dsr_mures_tag'),
        ]


class ManyUniqueTogetherRes(SoftRestorableModel, TestModelWithDefaultManager):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    tag = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('category', 'name'), ('category', 'tag'))


class ManyUniqueTogetherRes2(SoftRestorableModel, TestModelWithDefaultManager):
    category = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    tag = models.CharField(max_length=32)
    value = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('category', 'tag')
        constraints = [
            models.CheckConstraint(check=models.Q(value__lte=32768), name='dsr_mutres_value_lte_32768'),
            models.UniqueConstraint(fields=['category', 'name'], name='dsr_mutres_category_name_remver'),
            models.CheckConstraint(check=models.Q(value__gte=0), name='dsr_mutres_value_gte_0'),
        ]


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
