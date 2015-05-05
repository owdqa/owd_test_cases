# OWD-26338
# Send email via activesync with hotmail.com - verify the email is sent to the respective account
#
#   PROCEDURE
#       1- Open email app
#       2- Select hotmail account
#       3- Insert a valid hotmail account and password
#       4- Press next button
#       5- Press new email button
#       6- Insert an email address to send the email in To: field (or select one from contacts using +)
#       7- Insert a text in Subject: field
#       8- Insert the email content
#       9- Press send button
#   EXPECTED RESULT
#       The email is sent and appears in Sent folder. You should verify if the email is received by the addressee.

import time
import sys
sys.path.insert(1, "./")
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from tests.EMAIL.shared_test_functions.emailing import Emailing


class test_26338(Emailing):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_26338, self).__init__(*args, **kwargs)

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
        self.UTILS.reporting.logResult('info', 'Account info: {}'.format(self.user1))
        self.send_email(self.user1, self.user2)
        time.sleep(2)
        self.apps.kill_all()
        time.sleep(2)
        self.receive_email(self.user2, self.user1)
