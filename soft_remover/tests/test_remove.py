from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

from .models import (
    SimpleRem, SimpleUniqueRem, UniqueTogetherRem,
    ManyUniqueRem, ManyUniqueTogetherRem
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

    def test_unique(self):
        obj = SimpleUniqueRem.objects.create(name='TestName1')
        obj.delete()

        with self.assertRaises(IntegrityError), transaction.atomic():
            SimpleUniqueRem.objects.create(name='TestName1')

        self.assertTrue(SimpleUniqueRem.objects.all().count() == 0)
        self.assertTrue(SimpleUniqueRem.objects.removed().count() == 1)

        SimpleUniqueRem.objects.create(name='TestName2')

        SimpleUniqueRem.objects.all().delete()

        self.assertTrue(SimpleUniqueRem.objects.all().count() == 0)
        self.assertTrue(SimpleUniqueRem.objects.removed().count() == 2)
        self.assertTrue(SimpleUniqueRem.all_objects.all().count() == 2)

        SimpleUniqueRem.objects.create(name='TestName3')

        self.assertTrue(SimpleUniqueRem.objects.all().count() == 1)
        self.assertTrue(SimpleUniqueRem.objects.removed().count() == 2)
        self.assertTrue(SimpleUniqueRem.all_objects.all().count() == 3)

        SimpleUniqueRem.objects.first().delete_fully()

        self.assertTrue(SimpleUniqueRem.objects.all().count() == 0)
        self.assertTrue(SimpleUniqueRem.objects.removed().count() == 2)
        self.assertTrue(SimpleUniqueRem.all_objects.all().count() == 2)

        SimpleUniqueRem.objects.all().delete_fully()
        SimpleUniqueRem.objects.removed().delete_fully()

        self.assertTrue(SimpleUniqueRem.objects.all().count() == 0)
        self.assertTrue(SimpleUniqueRem.objects.removed().count() == 0)
        self.assertTrue(SimpleUniqueRem.all_objects.all().count() == 0)

    def test_unique_together(self):
        obj1 = UniqueTogetherRem.objects.create(category='TestCategory', name='TestName1', value=0)
        obj2 = UniqueTogetherRem.objects.create(category='TestCategory', name='TestName2', value=0)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRem.objects.create(category='TestCategory', name='TestName1', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRem.objects.create(category='TestCategory', name='TestName2', value=1)
        obj1.delete()
        obj2.delete()
        obj1 = UniqueTogetherRem.objects.create(category='TestCategory', name='TestName1', value=2)
        obj2 = UniqueTogetherRem.objects.create(category='TestCategory', name='TestName2', value=2)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRem.objects.create(category='TestCategory', name='TestName1', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRem.objects.create(category='TestCategory', name='TestName2', value=3)
        obj1.delete()
        obj1 = UniqueTogetherRem.objects.create(category='TestCategory', name='TestName1', value=4)

        self.assertTrue(UniqueTogetherRem.objects.all().count() == 2)
        self.assertTrue(UniqueTogetherRem.objects.removed().count() == 3)

        obj1.delete()

        self.assertTrue(UniqueTogetherRem.objects.all().count() == 1)
        self.assertTrue(UniqueTogetherRem.objects.removed().count() == 4)

        UniqueTogetherRem.objects.all().delete()

        self.assertTrue(UniqueTogetherRem.objects.all().count() == 0)
        self.assertTrue(UniqueTogetherRem.objects.removed().count() == 5)
        self.assertTrue(UniqueTogetherRem.all_objects.all().count() == 5)

        UniqueTogetherRem.objects.create(category='TestCategory', name='TestName1', value=4)

        self.assertTrue(UniqueTogetherRem.objects.all().count() == 1)
        self.assertTrue(UniqueTogetherRem.objects.removed().count() == 5)
        self.assertTrue(UniqueTogetherRem.all_objects.all().count() == 6)

        UniqueTogetherRem.objects.first().delete_fully()

        self.assertTrue(UniqueTogetherRem.objects.all().count() == 0)
        self.assertTrue(UniqueTogetherRem.objects.removed().count() == 5)
        self.assertTrue(UniqueTogetherRem.all_objects.all().count() == 5)

        UniqueTogetherRem.objects.all().delete_fully()
        UniqueTogetherRem.objects.removed().delete_fully()

        self.assertTrue(UniqueTogetherRem.objects.all().count() == 0)
        self.assertTrue(UniqueTogetherRem.objects.removed().count() == 0)
        self.assertTrue(UniqueTogetherRem.all_objects.all().count() == 0)

    def test_many_unique(self):
        obj = ManyUniqueRem.objects.create(name='TestName1', tag='tag11')
        obj.delete()

        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueRem.objects.create(name='TestName1', tag='tag12')
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueRem.objects.create(name='TestName2', tag='tag11')

        self.assertTrue(ManyUniqueRem.objects.all().count() == 0)
        self.assertTrue(ManyUniqueRem.objects.removed().count() == 1)

        ManyUniqueRem.objects.create(name='TestName2', tag='tag21')

        ManyUniqueRem.objects.all().delete()

        self.assertTrue(ManyUniqueRem.objects.all().count() == 0)
        self.assertTrue(ManyUniqueRem.objects.removed().count() == 2)
        self.assertTrue(ManyUniqueRem.all_objects.all().count() == 2)

        ManyUniqueRem.objects.create(name='TestName3', tag='tag31')

        self.assertTrue(ManyUniqueRem.objects.all().count() == 1)
        self.assertTrue(ManyUniqueRem.objects.removed().count() == 2)
        self.assertTrue(ManyUniqueRem.all_objects.all().count() == 3)

        ManyUniqueRem.objects.first().delete_fully()

        self.assertTrue(ManyUniqueRem.objects.all().count() == 0)
        self.assertTrue(ManyUniqueRem.objects.removed().count() == 2)
        self.assertTrue(ManyUniqueRem.all_objects.all().count() == 2)

        ManyUniqueRem.objects.all().delete_fully()
        ManyUniqueRem.objects.removed().delete_fully()

        self.assertTrue(ManyUniqueRem.objects.all().count() == 0)
        self.assertTrue(ManyUniqueRem.objects.removed().count() == 0)
        self.assertTrue(ManyUniqueRem.all_objects.all().count() == 0)

    def test_many_unique_together(self):
        obj1 = ManyUniqueTogetherRem.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=0)
        obj2 = ManyUniqueTogetherRem.objects.create(category='TestCategory', name='TestName2', tag='tag2', value=0)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRem.objects.create(category='TestCategory', name='TestName1', tag='tag11', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRem.objects.create(category='TestCategory', name='TestName11', tag='tag1', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRem.objects.create(category='TestCategory', name='TestName2', tag='tag22', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRem.objects.create(category='TestCategory', name='TestName22', tag='tag2', value=1)
        obj1.delete()
        obj2.delete()
        obj1 = ManyUniqueTogetherRem.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=2)
        obj2 = ManyUniqueTogetherRem.objects.create(category='TestCategory', name='TestName2', tag='tag2', value=2)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRem.objects.create(category='TestCategory', name='TestName1', tag='tag11', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRem.objects.create(category='TestCategory', name='TestName11', tag='tag1', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRem.objects.create(category='TestCategory', name='TestName2', tag='tag22', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRem.objects.create(category='TestCategory', name='TestName22', tag='tag2', value=3)
        obj1.delete()
        obj1 = ManyUniqueTogetherRem.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=4)

        self.assertTrue(ManyUniqueTogetherRem.objects.all().count() == 2)
        self.assertTrue(ManyUniqueTogetherRem.objects.removed().count() == 3)

        obj1.delete()

        self.assertTrue(ManyUniqueTogetherRem.objects.all().count() == 1)
        self.assertTrue(ManyUniqueTogetherRem.objects.removed().count() == 4)

        ManyUniqueTogetherRem.objects.all().delete()

        self.assertTrue(ManyUniqueTogetherRem.objects.all().count() == 0)
        self.assertTrue(ManyUniqueTogetherRem.objects.removed().count() == 5)
        self.assertTrue(ManyUniqueTogetherRem.all_objects.all().count() == 5)

        ManyUniqueTogetherRem.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=4)

        self.assertTrue(ManyUniqueTogetherRem.objects.all().count() == 1)
        self.assertTrue(ManyUniqueTogetherRem.objects.removed().count() == 5)
        self.assertTrue(ManyUniqueTogetherRem.all_objects.all().count() == 6)

        ManyUniqueTogetherRem.objects.first().delete_fully()

        self.assertTrue(ManyUniqueTogetherRem.objects.all().count() == 0)
        self.assertTrue(ManyUniqueTogetherRem.objects.removed().count() == 5)
        self.assertTrue(ManyUniqueTogetherRem.all_objects.all().count() == 5)

        ManyUniqueTogetherRem.objects.all().delete_fully()
        ManyUniqueTogetherRem.objects.removed().delete_fully()

        self.assertTrue(ManyUniqueTogetherRem.objects.all().count() == 0)
        self.assertTrue(ManyUniqueTogetherRem.objects.removed().count() == 0)
        self.assertTrue(ManyUniqueTogetherRem.all_objects.all().count() == 0)
