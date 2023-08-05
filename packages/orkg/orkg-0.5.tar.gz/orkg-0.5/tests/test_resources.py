from unittest import TestCase
from orkg import ORKG


class TestResources(TestCase):
    """
    Some test scenarios might need to be adjusted to the content of the running ORKG instance
    """
    orkg = ORKG()

    def test_by_id(self):
        res = self.orkg.resources.by_id('R1')
        self.assertTrue(res.succeeded)

    def test_get(self):
        res = self.orkg.resources.get()
        self.assertTrue(res.succeeded)
        self.assertEqual(len(res.content), 10)

    def test_get_with_items(self):
        count = 30
        res = self.orkg.resources.get(items=30)
        self.assertTrue(res.succeeded)
        self.assertEqual(len(res.content), 30)

    def test_add(self):
        label = "test"
        res = self.orkg.resources.add(label=label)
        self.assertTrue(res.succeeded)
        self.assertEqual(res.content['label'], label)

    def test_find_or_add(self):
        import random
        import string
        label = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(15))
        old = self.orkg.resources.add(label=label)
        self.assertTrue(old.succeeded, 'Creating first resource is a success')
        self.assertEqual(old.content['label'], label, 'The first resource has the correct label')
        new = self.orkg.resources.find_or_add(label=label)
        self.assertTrue(new.succeeded, 'Creating second resource is a success')
        self.assertEqual(new.content['id'], old.content['id'], 'the two resources have the same id')

    def test_add_with_class(self):
        label = "test"
        cls = "Coco"
        res = self.orkg.resources.add(label=label, classes=[cls])
        self.assertTrue(res.succeeded)
        self.assertEqual(res.content['label'], label)
        self.assertIn(cls, res.content['classes'])

    def test_update(self):
        res = self.orkg.resources.add(label="Coco")
        self.assertTrue(res.succeeded)
        label = "test"
        res = self.orkg.resources.update(id=res.content['id'], label=label)
        self.assertTrue(res.succeeded)
        res = self.orkg.resources.by_id(res.content['id'])
        self.assertTrue(res.succeeded)
        self.assertEqual(res.content['label'], label)
