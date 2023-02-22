from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

from .models import (
    SimpleRes, SimpleUniqueRes, UniqueTogetherRes,
    ManyUniqueRes, ManyUniqueTogetherRes, RestoreTogetherRes, ManyRestoreTogetherRes
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

    def test_unique(self):
        obj = SimpleUniqueRes.objects.create(name='TestName')
        obj.delete()

        SimpleUniqueRes.objects.create(name='TestName')

        with self.assertRaises(IntegrityError), transaction.atomic():
            SimpleUniqueRes.objects.create(name='TestName')

        self.assertTrue(SimpleUniqueRes.objects.all().count() == 1)
        self.assertTrue(SimpleUniqueRes.objects.removed().count() == 0)

        SimpleUniqueRes.objects.all().delete()

        self.assertTrue(SimpleUniqueRes.objects.all().count() == 0)
        self.assertTrue(SimpleUniqueRes.objects.removed().count() == 1)

    def test_unique_together(self):
        obj1 = UniqueTogetherRes.objects.create(category='TestCategory', name='TestName1', value=0)
        obj2 = UniqueTogetherRes.objects.create(category='TestCategory', name='TestName2', value=0)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRes.objects.create(category='TestCategory', name='TestName1', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRes.objects.create(category='TestCategory', name='TestName2', value=1)
        obj1.delete()
        obj2.delete()
        obj1 = UniqueTogetherRes.objects.create(category='TestCategory', name='TestName1', value=2)
        obj2 = UniqueTogetherRes.objects.create(category='TestCategory', name='TestName2', value=2)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRes.objects.create(category='TestCategory', name='TestName1', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRes.objects.create(category='TestCategory', name='TestName2', value=3)
        obj1.delete()
        obj1 = UniqueTogetherRes.objects.create(category='TestCategory', name='TestName1', value=4)

        self.assertTrue(UniqueTogetherRes.objects.all().count() == 2)
        self.assertTrue(UniqueTogetherRes.objects.removed().count() == 0)

        obj1.delete()

        self.assertTrue(UniqueTogetherRes.objects.all().count() == 1)
        self.assertTrue(UniqueTogetherRes.objects.removed().count() == 1)

        UniqueTogetherRes.objects.all().delete()

        self.assertTrue(UniqueTogetherRes.objects.all().count() == 0)
        self.assertTrue(UniqueTogetherRes.objects.removed().count() == 2)

    def test_many_unique(self):
        obj = ManyUniqueRes.objects.create(name='TestName', tag='tag1')
        obj.delete()

        obj2 = ManyUniqueRes.objects.create(name='TestName2', tag='tag1')
        self.assertTrue(obj2.pk == obj.pk)

        self.assertTrue(ManyUniqueRes.objects.all().count() == 1)
        self.assertTrue(ManyUniqueRes.objects.removed().count() == 0)

        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueRes.objects.create(name='TestName', tag='tag2')

        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueRes.objects.create(name='TestName3', tag='tag1')

        self.assertTrue(ManyUniqueRes.objects.all().count() == 1)
        self.assertTrue(ManyUniqueRes.objects.removed().count() == 0)
        self.assertTrue(ManyUniqueRes.objects.all().first().tag == 'tag1')

        ManyUniqueRes.objects.get(name='TestName', tag='tag1').delete()

        self.assertTrue(ManyUniqueRes.objects.all().count() == 0)
        self.assertTrue(ManyUniqueRes.objects.removed().count() == 1)

        obj = ManyUniqueRes.objects.create(name='TestName2', tag='tag2')
        obj.delete()

        self.assertTrue(ManyUniqueRes.objects.all().count() == 0)
        self.assertTrue(ManyUniqueRes.objects.removed().count() == 2)

        obj2 = ManyUniqueRes.objects.create(name='TestName2', tag='tag1')
        self.assertTrue(obj2.pk == obj.pk)

        self.assertTrue(ManyUniqueRes.objects.all().count() == 1)
        self.assertTrue(ManyUniqueRes.objects.removed().count() == 1)
        self.assertTrue(ManyUniqueRes.objects.all().first().tag == 'tag2')

        ManyUniqueRes.objects.all().delete()

        self.assertTrue(ManyUniqueRes.objects.all().count() == 0)
        self.assertTrue(ManyUniqueRes.objects.removed().count() == 2)

    def test_many_unique_together(self):
        obj1 = ManyUniqueTogetherRes.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=0)
        obj2 = ManyUniqueTogetherRes.objects.create(category='TestCategory', name='TestName2', tag='tag2', value=0)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRes.objects.create(category='TestCategory', name='TestName1', tag='tag11', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRes.objects.create(category='TestCategory', name='TestName11', tag='tag1', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRes.objects.create(category='TestCategory', name='TestName2', tag='tag22', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRes.objects.create(category='TestCategory', name='TestName22', tag='tag2', value=1)
        obj1.delete()
        obj2.delete()
        obj1 = ManyUniqueTogetherRes.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=2)
        obj2 = ManyUniqueTogetherRes.objects.create(category='TestCategory', name='TestName2', tag='tag2', value=2)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRes.objects.create(category='TestCategory', name='TestName1', tag='tag11', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRes.objects.create(category='TestCategory', name='TestName11', tag='tag1', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRes.objects.create(category='TestCategory', name='TestName2', tag='tag22', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRes.objects.create(category='TestCategory', name='TestName22', tag='tag2', value=3)
        obj1.delete()
        obj1 = ManyUniqueTogetherRes.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=4)

        self.assertTrue(ManyUniqueTogetherRes.objects.all().count() == 2)
        self.assertTrue(ManyUniqueTogetherRes.objects.removed().count() == 0)

        obj1.delete()

        self.assertTrue(ManyUniqueTogetherRes.objects.all().count() == 1)
        self.assertTrue(ManyUniqueTogetherRes.objects.removed().count() == 1)

        ManyUniqueTogetherRes.objects.all().delete()

        self.assertTrue(ManyUniqueTogetherRes.objects.all().count() == 0)
        self.assertTrue(ManyUniqueTogetherRes.objects.removed().count() == 2)

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
