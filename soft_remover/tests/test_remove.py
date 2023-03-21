from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

from .models import (
    SimpleRem,
    SimpleUniqueRem, SimpleUniqueRem2,
    UniqueTogetherRem, UniqueTogetherRem2,
    ManyUniqueRem, ManyUniqueRem2,
    ManyUniqueTogetherRem, ManyUniqueTogetherRem2,
)


class TestSoftRemove(TestCase):
    def test_no_unique(self):
        obj = SimpleRem.objects.create(name='TestName')
        obj.delete()
        obj = SimpleRem.objects.create(name='TestName')
        obj.delete()
        obj = SimpleRem.objects.create(name='TestName')

        self.assertTrue(SimpleRem.objects.all().count() == 1)
        self.assertTrue(SimpleRem.objects.removed().count() == 2)

        obj.delete()

        self.assertTrue(SimpleRem.objects.all().count() == 0)
        self.assertTrue(SimpleRem.objects.removed().count() == 3)

        SimpleRem.objects.create(name='TestName')

        SimpleRem.objects.all().delete()

        self.assertTrue(SimpleRem.objects.all().count() == 0)
        self.assertTrue(SimpleRem.objects.removed().count() == 4)
        self.assertTrue(SimpleRem.all_objects.all().count() == 4)

        SimpleRem.objects.create(name='TestName')

        self.assertTrue(SimpleRem.objects.all().count() == 1)
        self.assertTrue(SimpleRem.objects.removed().count() == 4)
        self.assertTrue(SimpleRem.all_objects.all().count() == 5)

        SimpleRem.objects.first().delete_fully()

        self.assertTrue(SimpleRem.objects.all().count() == 0)
        self.assertTrue(SimpleRem.objects.removed().count() == 4)
        self.assertTrue(SimpleRem.all_objects.all().count() == 4)

        SimpleRem.objects.all().delete_fully()
        SimpleRem.objects.removed().delete_fully()

        self.assertTrue(SimpleRem.objects.all().count() == 0)
        self.assertTrue(SimpleRem.objects.removed().count() == 0)
        self.assertTrue(SimpleRem.all_objects.all().count() == 0)

    def _unique(self, model):
        obj = model.objects.create(name='TestName1')
        obj.delete()

        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(name='TestName1')

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 1)

        model.objects.create(name='TestName2')

        model.objects.all().delete()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 2)
        self.assertTrue(model.all_objects.all().count() == 2)

        model.objects.create(name='TestName3')

        self.assertTrue(model.objects.all().count() == 1)
        self.assertTrue(model.objects.removed().count() == 2)
        self.assertTrue(model.all_objects.all().count() == 3)

        model.objects.first().delete_fully()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 2)
        self.assertTrue(model.all_objects.all().count() == 2)

        model.objects.all().delete_fully()
        model.objects.removed().delete_fully()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 0)
        self.assertTrue(model.all_objects.all().count() == 0)

    def test_unique(self):
        self._unique(SimpleUniqueRem)

    def test_unique2(self):
        self._unique(SimpleUniqueRem2)

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
        self.assertTrue(model.objects.removed().count() == 3)

        obj1.delete()

        self.assertTrue(model.objects.all().count() == 1)
        self.assertTrue(model.objects.removed().count() == 4)

        model.objects.all().delete()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 5)
        self.assertTrue(model.all_objects.all().count() == 5)

        model.objects.create(category='TestCategory', name='TestName1', value=4)

        self.assertTrue(model.objects.all().count() == 1)
        self.assertTrue(model.objects.removed().count() == 5)
        self.assertTrue(model.all_objects.all().count() == 6)

        model.objects.first().delete_fully()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 5)
        self.assertTrue(model.all_objects.all().count() == 5)

        model.objects.all().delete_fully()
        model.objects.removed().delete_fully()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 0)
        self.assertTrue(model.all_objects.all().count() == 0)

    def test_unique_together(self):
        self._unique_together(UniqueTogetherRem)

    def test_unique_together2(self):
        self._unique_together(UniqueTogetherRem2)

    def _many_unique(self, model):
        obj = model.objects.create(name='TestName1', tag='tag11')
        obj.delete()

        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(name='TestName1', tag='tag12')
        with self.assertRaises(IntegrityError), transaction.atomic():
            model.objects.create(name='TestName2', tag='tag11')

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 1)

        model.objects.create(name='TestName2', tag='tag21')

        model.objects.all().delete()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 2)
        self.assertTrue(model.all_objects.all().count() == 2)

        model.objects.create(name='TestName3', tag='tag31')

        self.assertTrue(model.objects.all().count() == 1)
        self.assertTrue(model.objects.removed().count() == 2)
        self.assertTrue(model.all_objects.all().count() == 3)

        model.objects.first().delete_fully()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 2)
        self.assertTrue(model.all_objects.all().count() == 2)

        model.objects.all().delete_fully()
        model.objects.removed().delete_fully()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 0)
        self.assertTrue(model.all_objects.all().count() == 0)

    def test_many_unique(self):
        self._many_unique(ManyUniqueRem)

    def test_many_unique2(self):
        self._many_unique(ManyUniqueRem2)

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
        self.assertTrue(model.objects.removed().count() == 3)

        obj1.delete()

        self.assertTrue(model.objects.all().count() == 1)
        self.assertTrue(model.objects.removed().count() == 4)

        model.objects.all().delete()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 5)
        self.assertTrue(model.all_objects.all().count() == 5)

        model.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=4)

        self.assertTrue(model.objects.all().count() == 1)
        self.assertTrue(model.objects.removed().count() == 5)
        self.assertTrue(model.all_objects.all().count() == 6)

        model.objects.first().delete_fully()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 5)
        self.assertTrue(model.all_objects.all().count() == 5)

        model.objects.all().delete_fully()
        model.objects.removed().delete_fully()

        self.assertTrue(model.objects.all().count() == 0)
        self.assertTrue(model.objects.removed().count() == 0)
        self.assertTrue(model.all_objects.all().count() == 0)

    def test_many_unique_together(self):
        self._many_unique_together(ManyUniqueTogetherRem)

    def test_many_unique_together2(self):
        self._many_unique_together(ManyUniqueTogetherRem2)
