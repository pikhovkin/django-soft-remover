from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

from .models import SimpleRS, UniqueTogetherRS, ManyUniqueTogetherRS, RestoreTogetherRS, ManyRestoreTogetherRS


class TestSoftRestore(TestCase):
    def test_no_unique(self):
        obj = SimpleRS.objects.create(name='TestName')
        obj.delete()
        obj = SimpleRS.objects.create(name='TestName')
        obj.delete()
        obj = SimpleRS.objects.create(name='TestName')

        self.assertTrue(SimpleRS.objects.all().count() == 1)
        self.assertTrue(SimpleRS.objects.removed().count() == 2)

        obj.delete()

        self.assertTrue(SimpleRS.objects.all().count() == 0)
        self.assertTrue(SimpleRS.objects.removed().count() == 3)

    def test_unique_together(self):
        obj1 = UniqueTogetherRS.objects.create(category='TestCategory', name='TestName1', value=0)
        obj2 = UniqueTogetherRS.objects.create(category='TestCategory', name='TestName2', value=0)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRS.objects.create(category='TestCategory', name='TestName1', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRS.objects.create(category='TestCategory', name='TestName2', value=1)
        obj1.delete()
        obj2.delete()
        obj1 = UniqueTogetherRS.objects.create(category='TestCategory', name='TestName1', value=2)
        obj2 = UniqueTogetherRS.objects.create(category='TestCategory', name='TestName2', value=2)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRS.objects.create(category='TestCategory', name='TestName1', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            UniqueTogetherRS.objects.create(category='TestCategory', name='TestName2', value=3)
        obj1.delete()
        obj1 = UniqueTogetherRS.objects.create(category='TestCategory', name='TestName1', value=4)

        self.assertTrue(UniqueTogetherRS.objects.all().count() == 2)
        self.assertTrue(UniqueTogetherRS.objects.removed().count() == 0)

        obj1.delete()

        self.assertTrue(UniqueTogetherRS.objects.all().count() == 1)
        self.assertTrue(UniqueTogetherRS.objects.removed().count() == 1)

    def test_many_unique_together(self):
        obj1 = ManyUniqueTogetherRS.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=0)
        obj2 = ManyUniqueTogetherRS.objects.create(category='TestCategory', name='TestName2', tag='tag2', value=0)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRS.objects.create(category='TestCategory', name='TestName1', tag='tag11', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRS.objects.create(category='TestCategory', name='TestName11', tag='tag1', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRS.objects.create(category='TestCategory', name='TestName2', tag='tag22', value=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRS.objects.create(category='TestCategory', name='TestName22', tag='tag2', value=1)
        obj1.delete()
        obj2.delete()
        obj1 = ManyUniqueTogetherRS.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=2)
        obj2 = ManyUniqueTogetherRS.objects.create(category='TestCategory', name='TestName2', tag='tag2', value=2)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRS.objects.create(category='TestCategory', name='TestName1', tag='tag11', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRS.objects.create(category='TestCategory', name='TestName11', tag='tag1', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRS.objects.create(category='TestCategory', name='TestName2', tag='tag22', value=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ManyUniqueTogetherRS.objects.create(category='TestCategory', name='TestName22', tag='tag2', value=3)
        obj1.delete()
        obj1 = ManyUniqueTogetherRS.objects.create(category='TestCategory', name='TestName1', tag='tag1', value=4)

        self.assertTrue(ManyUniqueTogetherRS.objects.all().count() == 2)
        self.assertTrue(ManyUniqueTogetherRS.objects.removed().count() == 0)

        obj1.delete()

        self.assertTrue(ManyUniqueTogetherRS.objects.all().count() == 1)
        self.assertTrue(ManyUniqueTogetherRS.objects.removed().count() == 1)

    def test_restore_together(self):
        obj = RestoreTogetherRS.objects.create(name='TestName')
        obj.delete()
        obj = RestoreTogetherRS.objects.create(name='TestName')
        obj.delete()
        obj = RestoreTogetherRS.objects.create(name='TestName')

        self.assertTrue(RestoreTogetherRS.objects.all().count() == 1)
        self.assertTrue(RestoreTogetherRS.objects.removed().count() == 0)

        obj.delete()

        self.assertTrue(RestoreTogetherRS.objects.all().count() == 0)
        self.assertTrue(RestoreTogetherRS.objects.removed().count() == 1)

    def test_many_restore_together(self):
        obj = ManyRestoreTogetherRS.objects.create(category='TestCategory', name='TestName1', value=0)
        obj.delete()
        obj = ManyRestoreTogetherRS.objects.create(category='TestCategory', name='TestName2', value=0)
        obj.delete()
        obj = ManyRestoreTogetherRS.objects.create(category='TestCategory', name='TestName1', value=1)
        obj.delete()
        obj = ManyRestoreTogetherRS.objects.create(category='TestCategory', name='TestName2', value=1)
        obj = ManyRestoreTogetherRS.objects.create(category='TestCategory', name='TestName1', value=2)

        self.assertTrue(ManyRestoreTogetherRS.objects.all().count() == 2)
        self.assertTrue(ManyRestoreTogetherRS.objects.removed().count() == 0)

        obj.delete()

        self.assertTrue(ManyRestoreTogetherRS.objects.all().count() == 1)
        self.assertTrue(ManyRestoreTogetherRS.objects.removed().count() == 1)
