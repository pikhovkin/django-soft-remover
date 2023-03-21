from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

from .models import (
    SimpleRes,
    SimpleUniqueRes, SimpleUniqueRes2,
    UniqueTogetherRes, UniqueTogetherRes2,
    ManyUniqueRes, ManyUniqueRes2,
    ManyUniqueTogetherRes, ManyUniqueTogetherRes2,
    RestoreTogetherRes, ManyRestoreTogetherRes,
)


class TestSoftRestore(TestCase):
    def test_no_unique(self):
        obj = SimpleRes.objects.create(name='TestName')
        obj.delete()
        obj = SimpleRes.objects.create(name='TestName')
        obj.delete()
        obj = SimpleRes.objects.create(name='TestName')

        self.assertTrue(SimpleRes.objects.all().count() == 1)
        self.assertTrue(SimpleRes.objects.removed().count() == 2)

        obj.delete()

        self.assertTrue(SimpleRes.objects.all().count() == 0)
        self.assertTrue(SimpleRes.objects.removed().count() == 3)

        SimpleRes.objects.create(name='TestName')

        SimpleRes.objects.all().delete()

        self.assertTrue(SimpleRes.objects.all().count() == 0)
        self.assertTrue(SimpleRes.objects.removed().count() == 4)
        self.assertTrue(SimpleRes.all_objects.all().count() == 4)

        SimpleRes.objects.create(name='TestName')

        self.assertTrue(SimpleRes.objects.all().count() == 1)
        self.assertTrue(SimpleRes.objects.removed().count() == 4)
        self.assertTrue(SimpleRes.all_objects.all().count() == 5)

        SimpleRes.objects.first().delete_fully()

        self.assertTrue(SimpleRes.objects.all().count() == 0)
        self.assertTrue(SimpleRes.objects.removed().count() == 4)
        self.assertTrue(SimpleRes.all_objects.all().count() == 4)

        SimpleRes.objects.all().delete_fully()
        SimpleRes.objects.removed().delete_fully()

        self.assertTrue(SimpleRes.objects.all().count() == 0)
        self.assertTrue(SimpleRes.objects.removed().count() == 0)
        self.assertTrue(SimpleRes.all_objects.all().count() == 0)

    def _unique(self, model):
        obj = model.objects.create(name='TestName')
        obj.delete()

        model.objects.create(name='TestName')

        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(name='TestName')

        self.assertTrue(model.objects.all().count() == 1)
        self.assertTrue(model.objects.removed().count() == 0)

        model.objects.all().delete()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 1)
        self.assertTrue(model.all_objects.all().count() == 1)

        model.objects.all().delete_fully()
        model.objects.removed().delete_fully()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 0)
        self.assertTrue(model.all_objects.all().count() == 0)

    def test_unique(self):
        self._unique(SimpleUniqueRes)

    def test_unique2(self):
        self._unique(SimpleUniqueRes2)

    def _unique_together(self, model):
        obj1 = model.objects.create(category='TestCategory', name='TestName1', value=0)
        obj2 = model.objects.create(category='TestCategory', name='TestName2', value=0)
        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(category='TestCategory', name='TestName1', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(category='TestCategory', name='TestName2', value=1)
        obj1.delete()
        obj2.delete()
        obj1 = model.objects.create(category='TestCategory', name='TestName1', value=2)
        obj2 = model.objects.create(category='TestCategory', name='TestName2', value=2)
        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(category='TestCategory', name='TestName1', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(category='TestCategory', name='TestName2', value=3)
        obj1.delete()
        obj1 = model.objects.create(category='TestCategory', name='TestName1', value=4)

        self.assertTrue(model.objects.all().count() == 2)
        self.assertTrue(model.objects.removed().count() == 0)

        obj1.delete()

        self.assertTrue(model.objects.all().count() == 1)
        self.assertTrue(model.objects.removed().count() == 1)

        model.objects.all().delete()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 2)
        self.assertTrue(model.all_objects.all().count() == 2)

        model.objects.create(category='TestCategory', name='TestName1', value=4)

        self.assertTrue(model.objects.all().count() == 1)
        self.assertTrue(model.objects.removed().count() == 1)
        self.assertTrue(model.all_objects.all().count() == 2)

        model.objects.first().delete_fully()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 1)
        self.assertTrue(model.all_objects.all().count() == 1)

        model.objects.all().delete_fully()
        model.objects.removed().delete_fully()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 0)
        self.assertTrue(model.all_objects.all().count() == 0)

    def test_unique_together(self):
        self._unique_together(UniqueTogetherRes)

    def test_unique_together2(self):
        self._unique_together(UniqueTogetherRes2)

    def _many_unique(self, model):
        obj = model.objects.create(name='TestName', tag='tag1')
        obj.delete()

        obj2 = model.objects.create(name='TestName2', tag='tag1')
        self.assertTrue(obj2.pk == obj.pk)

        self.assertTrue(model.objects.all().count() == 1)
        self.assertTrue(model.objects.removed().count() == 0)

        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(name='TestName', tag='tag2')

        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(name='TestName3', tag='tag1')

        self.assertTrue(model.objects.all().count() == 1)
        self.assertTrue(model.objects.removed().count() == 0)
        self.assertTrue(model.objects.all().first().tag == 'tag1')

        model.objects.get(name='TestName', tag='tag1').delete()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 1)

        obj = model.objects.create(name='TestName2', tag='tag2')
        obj.delete()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 2)

        obj2 = model.objects.create(name='TestName2', tag='tag1')
        self.assertTrue(obj2.pk == obj.pk)

        self.assertTrue(model.objects.all().count() == 1)
        self.assertTrue(model.objects.removed().count() == 1)
        self.assertTrue(model.objects.all().first().tag == 'tag2')

        model.objects.all().delete()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 2)
        self.assertTrue(model.all_objects.all().count() == 2)

        model.objects.create(name='TestName', tag='tag1')

        self.assertTrue(model.objects.all().count() == 1)
        self.assertTrue(model.objects.removed().count() == 1)
        self.assertTrue(model.all_objects.all().count() == 2)

        model.objects.first().delete_fully()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 1)
        self.assertTrue(model.all_objects.all().count() == 1)

        model.objects.all().delete_fully()
        model.objects.removed().delete_fully()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 0)
        self.assertTrue(model.all_objects.all().count() == 0)

    def test_many_unique(self):
        self._many_unique(ManyUniqueRes)

    def test_many_unique2(self):
        self._many_unique(ManyUniqueRes2)

    def _many_unique_together(self, model):
        obj1 = model.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=0)
        obj2 = model.objects.create(category='TestCategory', name='TestName2', tag='tag2', value=0)
        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(category='TestCategory', name='TestName1', tag='tag11', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(category='TestCategory', name='TestName11', tag='tag1', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(category='TestCategory', name='TestName2', tag='tag22', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(category='TestCategory', name='TestName22', tag='tag2', value=1)
        obj1.delete()
        obj2.delete()
        obj1 = model.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=2)
        obj2 = model.objects.create(category='TestCategory', name='TestName2', tag='tag2', value=2)
        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(category='TestCategory', name='TestName1', tag='tag11', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(category='TestCategory', name='TestName11', tag='tag1', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(category='TestCategory', name='TestName2', tag='tag22', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(category='TestCategory', name='TestName22', tag='tag2', value=3)
        obj1.delete()
        obj1 = model.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=4)

        self.assertTrue(model.objects.all().count() == 2)
        self.assertTrue(model.objects.removed().count() == 0)

        obj1.delete()

        self.assertTrue(model.objects.all().count() == 1)
        self.assertTrue(model.objects.removed().count() == 1)

        model.objects.all().delete()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 2)
        self.assertTrue(model.all_objects.all().count() == 2)

        model.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=0)

        self.assertTrue(model.objects.all().count() == 1)
        self.assertTrue(model.objects.removed().count() == 1)
        self.assertTrue(model.all_objects.all().count() == 2)

        model.objects.first().delete_fully()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 1)
        self.assertTrue(model.all_objects.all().count() == 1)

        model.objects.all().delete_fully()
        model.objects.removed().delete_fully()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 0)
        self.assertTrue(model.all_objects.all().count() == 0)

    def test_many_unique_together(self):
        self._many_unique_together(ManyUniqueTogetherRes)

    def test_many_unique_together2(self):
        self._many_unique_together(ManyUniqueTogetherRes2)

    def test_restore_together(self):
        obj = RestoreTogetherRes.objects.create(name='TestName')
        obj.delete()
        obj = RestoreTogetherRes.objects.create(name='TestName')
        obj.delete()
        obj = RestoreTogetherRes.objects.create(name='TestName')

        self.assertTrue(RestoreTogetherRes.objects.all().count() == 1)
        self.assertTrue(RestoreTogetherRes.objects.removed().count() == 0)

        obj.delete()

        self.assertTrue(RestoreTogetherRes.objects.all().count() == 0)
        self.assertTrue(RestoreTogetherRes.objects.removed().count() == 1)

        RestoreTogetherRes.objects.create(name='TestName')

        RestoreTogetherRes.objects.all().delete()

        self.assertTrue(RestoreTogetherRes.objects.all().count() == 0)
        self.assertTrue(RestoreTogetherRes.objects.removed().count() == 1)
        self.assertTrue(RestoreTogetherRes.all_objects.all().count() == 1)

        RestoreTogetherRes.objects.create(name='TestName')

        self.assertTrue(RestoreTogetherRes.objects.all().count() == 1)
        self.assertTrue(RestoreTogetherRes.objects.removed().count() == 0)
        self.assertTrue(RestoreTogetherRes.all_objects.all().count() == 1)

        RestoreTogetherRes.objects.first().delete_fully()

        self.assertTrue(RestoreTogetherRes.objects.all().count() == 0)
        self.assertTrue(RestoreTogetherRes.objects.removed().count() == 0)
        self.assertTrue(RestoreTogetherRes.all_objects.all().count() == 0)

        RestoreTogetherRes.objects.create(name='TestName')

        self.assertTrue(RestoreTogetherRes.objects.all().count() == 1)
        self.assertTrue(RestoreTogetherRes.objects.removed().count() == 0)
        self.assertTrue(RestoreTogetherRes.all_objects.all().count() == 1)

        RestoreTogetherRes.objects.all().delete_fully()
        RestoreTogetherRes.objects.removed().delete_fully()

        self.assertTrue(RestoreTogetherRes.objects.all().count() == 0)
        self.assertTrue(RestoreTogetherRes.objects.removed().count() == 0)
        self.assertTrue(RestoreTogetherRes.all_objects.all().count() == 0)

    def test_many_restore_together(self):
        obj = ManyRestoreTogetherRes.objects.create(category='TestCategory', name='TestName1', value=0)
        obj.delete()
        obj = ManyRestoreTogetherRes.objects.create(category='TestCategory', name='TestName2', value=0)
        obj.delete()
        obj = ManyRestoreTogetherRes.objects.create(category='TestCategory', name='TestName1', value=1)
        obj.delete()
        obj = ManyRestoreTogetherRes.objects.create(category='TestCategory', name='TestName2', value=1)
        obj = ManyRestoreTogetherRes.objects.create(category='TestCategory', name='TestName1', value=2)

        self.assertTrue(ManyRestoreTogetherRes.objects.all().count() == 2)
        self.assertTrue(ManyRestoreTogetherRes.objects.removed().count() == 0)

        obj.delete()

        self.assertTrue(ManyRestoreTogetherRes.objects.all().count() == 1)
        self.assertTrue(ManyRestoreTogetherRes.objects.removed().count() == 1)

        ManyRestoreTogetherRes.objects.all().delete()

        self.assertTrue(ManyRestoreTogetherRes.objects.all().count() == 0)
        self.assertTrue(ManyRestoreTogetherRes.objects.removed().count() == 2)
        self.assertTrue(ManyRestoreTogetherRes.all_objects.all().count() == 2)

        ManyRestoreTogetherRes.objects.create(category='TestCategory', name='TestName1', value=0)

        self.assertTrue(ManyRestoreTogetherRes.objects.all().count() == 1)
        self.assertTrue(ManyRestoreTogetherRes.objects.removed().count() == 1)
        self.assertTrue(ManyRestoreTogetherRes.all_objects.all().count() == 2)

        ManyRestoreTogetherRes.objects.first().delete_fully()

        self.assertTrue(ManyRestoreTogetherRes.objects.all().count() == 0)
        self.assertTrue(ManyRestoreTogetherRes.objects.removed().count() == 1)
        self.assertTrue(ManyRestoreTogetherRes.all_objects.all().count() == 1)

        ManyRestoreTogetherRes.objects.all().delete_fully()
        ManyRestoreTogetherRes.objects.removed().delete_fully()

        self.assertTrue(ManyRestoreTogetherRes.objects.all().count() == 0)
        self.assertTrue(ManyRestoreTogetherRes.objects.removed().count() == 0)
        self.assertTrue(ManyRestoreTogetherRes.all_objects.all().count() == 0)
