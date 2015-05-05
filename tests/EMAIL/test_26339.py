# OWD-26339
# Receive email via activesync with hotmail.com - verify the email is
# received from the correct account the email was sent from
#
#   PROCEDURE
#       1- Open email app
#       2- Select hotmail account
#       3- Insert a valid hotmail account and password
#       4- Press next button
#       5- Open Inbox folder
#       6- Send an email(with subject and content) from another account to the email address configured in the device
#       7- Press update button in the device
#
#   EXPECTED RESULT
#       The email is received an shows the correct information
import time
import sys
sys.path.insert(1, "./")
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from tests.EMAIL.shared_test_functions.emailing import Emailing


class test_26339(Emailing):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_26339, self).__init__(*args, **kwargs)

    def setUp(self):
        self.testNum = self.__class__.__name__
        self.test_type = "hotmail"

        self.setUpEmail()

        # Email parameters
        self.username1 = self.UTILS.general.get_config_variable(self.test_type + "_1_user", "common")
        self.email1 = self.UTILS.general.get_config_variable(self.test_type + "_1_email", "common")
        self.passwd1 = self.UTILS.general.get_config_variable(self.test_type + "_1_pass", "common")
        self.user1 = {"username": self.username1, "email": self.email1, "pass": self.passwd1}

        self.username2 = self.UTILS.general.get_config_variable(self.test_type + "_2_user", "common")
        self.email2 = self.UTILS.general.get_config_variable(self.test_type + "_2_email", "common")
        self.passwd2 = self.UTILS.general.get_config_variable(self.test_type + "_2_pass", "common")
        self.user2 = {"username": self.username2, "email": self.email2, "pass": self.passwd2}

        self.data_layer.connect_to_wifi()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.send_email(self.user1, self.user2)
        time.sleep(2)
        self.apps.kill_all()
        time.sleep(2)
        self.receive_email(self.user2, self.user1)
