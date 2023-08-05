from unittest import TestCase
from orkg import ORKG


class TestBackend(TestCase):
    """
    Some test scenarios might need to be adjusted to the content of the running ORKG instance
    """

    def test_auth(self):
        orkg = ORKG(host='https://www.orkg.org/orkg/', creds=('test@test.test', 'test123'))
        self.assertIsNotNone(orkg.token)


