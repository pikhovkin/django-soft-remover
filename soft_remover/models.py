from django.db import transaction, models
from django.utils.translation import gettext_lazy as _

from .managers import SoftRemovableManager, SoftRestorableManager


__all__ = (
    'SoftRemovableManager',
    'SoftRestorableManager',
)


class BaseSoftRemovableModel(models.Model):
    is_removed = models.BooleanField(_('Removed'), default=False, editable=False)

    objects = SoftRemovableManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_removed = True
        self.save(using=using)


class SoftRemovableModel(BaseSoftRemovableModel):
    remver = models.PositiveIntegerField(_('Removal version'), default=0, editable=False)

    objects = SoftRemovableManager()

    class Meta:
        abstract = True

    @property
    def _safe_fields(self):
        fields = self._meta.unique_together
        fields = fields[0] if fields else fields
        if isinstance(fields, str):
            fields = self._meta.unique_together
        fields = set(fields) - {'remver'}
        return {field: getattr(self, field) for field in fields}

    def delete(self, using=None, keep_parents=False):
        self.remver = self.__class__.objects.removed().filter(**self._safe_fields).count() + 1
        super().delete(using=using, keep_parents=keep_parents)


class SoftRestorableModel(BaseSoftRemovableModel):
    objects = SoftRestorableManager()

    class Meta:
        abstract = True

    @property
    def _safe_fields(self):
        restore_together = getattr(getattr(self, 'MetaSoftRemover', None), 'restore_together', [])
        fields = self._meta.unique_together or restore_together
        fields = fields[0] if fields else fields
        if isinstance(fields, str):
            fields = self._meta.unique_together or restore_together
        return {field: getattr(self, field) for field in fields}

    def restore(self, using=None):
        self.is_removed = False
        self.save(using=using)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.pk and self._safe_fields:
            try:
                instance = self.__class__.objects.removed().get(**self._safe_fields)
                instance.restore()
                self.pk = instance.pk
                return
            except self.DoesNotExist:
                ...
        super().save(*args, **kwargs)
