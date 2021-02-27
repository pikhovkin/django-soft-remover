from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

from .models import SimpleRM, UniqueTogetherRM, ManyUniqueTogetherRM


class TestSoftRemove(TestCase):
    def test_no_unique(self):
        obj = SimpleRM.objects.create(name='TestName')
        obj.delete()
        obj = SimpleRM.objects.create(name='TestName')
        obj.delete()
        obj = SimpleRM.objects.create(name='TestName')

        self.assertTrue(SimpleRM.objects.all().count() == 1)
        self.assertTrue(SimpleRM.objects.removed().count() == 2)

        obj.delete()

        self.assertTrue(SimpleRM.objects.all().count() == 0)
        self.assertTrue(SimpleRM.objects.removed().count() == 3)

    def test_unique_together(self):
        obj1 = UniqueTogetherRM.objects.create(category='TestCategory', name='TestName1', value=0)
        obj2 = UniqueTogetherRM.objects.create(category='TestCategory', name='TestName2', value=0)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRM.objects.create(category='TestCategory', name='TestName1', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRM.objects.create(category='TestCategory', name='TestName2', value=1)
        obj1.delete()
        obj2.delete()
        obj1 = UniqueTogetherRM.objects.create(category='TestCategory', name='TestName1', value=2)
        obj2 = UniqueTogetherRM.objects.create(category='TestCategory', name='TestName2', value=2)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRM.objects.create(category='TestCategory', name='TestName1', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRM.objects.create(category='TestCategory', name='TestName2', value=3)
        obj1.delete()
        obj1 = UniqueTogetherRM.objects.create(category='TestCategory', name='TestName1', value=4)

        self.assertTrue(UniqueTogetherRM.objects.all().count() == 2)
        self.assertTrue(UniqueTogetherRM.objects.removed().count() == 3)

        obj1.delete()

        self.assertTrue(UniqueTogetherRM.objects.all().count() == 1)
        self.assertTrue(UniqueTogetherRM.objects.removed().count() == 4)

    def test_many_unique_together(self):
        obj1 = ManyUniqueTogetherRM.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=0)
        obj2 = ManyUniqueTogetherRM.objects.create(category='TestCategory', name='TestName2', tag='tag2', value=0)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRM.objects.create(category='TestCategory', name='TestName1', tag='tag11', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRM.objects.create(category='TestCategory', name='TestName11', tag='tag1', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRM.objects.create(category='TestCategory', name='TestName2', tag='tag22', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRM.objects.create(category='TestCategory', name='TestName22', tag='tag2', value=1)
        obj1.delete()
        obj2.delete()
        obj1 = ManyUniqueTogetherRM.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=2)
        obj2 = ManyUniqueTogetherRM.objects.create(category='TestCategory', name='TestName2', tag='tag2', value=2)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRM.objects.create(category='TestCategory', name='TestName1', tag='tag11', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRM.objects.create(category='TestCategory', name='TestName11', tag='tag1', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRM.objects.create(category='TestCategory', name='TestName2', tag='tag22', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRM.objects.create(category='TestCategory', name='TestName22', tag='tag2', value=3)
        obj1.delete()
        obj1 = ManyUniqueTogetherRM.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=4)

        self.assertTrue(ManyUniqueTogetherRM.objects.all().count() == 2)
        self.assertTrue(ManyUniqueTogetherRM.objects.removed().count() == 3)

        obj1.delete()

        self.assertTrue(ManyUniqueTogetherRM.objects.all().count() == 1)
        self.assertTrue(ManyUniqueTogetherRM.objects.removed().count() == 4)
