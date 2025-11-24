from django.test import SimpleTestCase
import manage

class ManageEntryPointTests(SimpleTestCase):
    def test_main_callable(self):
        assert callable(manage.main)
