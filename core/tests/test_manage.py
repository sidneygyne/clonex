import manage
from django.test import SimpleTestCase
from django.core.management import ManagementUtility

class ManagePyTests(SimpleTestCase):

    def test_manage_main(self):
        utility = ManagementUtility(["manage.py", "check"])
        utility.execute()
        self.assertTrue(hasattr(manage, "main"))
