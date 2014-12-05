# OWD-26340
# Send email via imap with gmail.com - verify the email is sent to the respective account
#   PROCEDURE
#     1- Open email app
#     2- Select gmail account
#     3- Insert a valid gmail account and password
#     4- Press next button
#     5- Press new email button
#     6- Insert an email address to send the email in To: field
#     7- Insert a text in Subject: field
#     8- Insert the email content
#     9- Press send button
#
#   EXPECTED RESULT
#       The email is sent and appears in Sent folder

import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from tests.EMAIL.shared_test_functions.emailing import Emailing


class test_26340(Emailing):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_26340, self).__init__(*args, **kwargs)

    def setUp(self):
        self.testNum = self.__class__.__name__
        self.testType = "gmail"

        self.setUpEmail()

        #
        # Email parameters
        #
        self.username1 = self.UTILS.general.get_config_variable(self.testType.upper() + "_1_user", "common")
        self.email1 = self.UTILS.general.get_config_variable(self.testType.upper() + "_1_email", "common")
        self.passwd1 = self.UTILS.general.get_config_variable(self.testType.upper() + "_1_pass", "common")
        self.user1 = {"username": self.username1, "email": self.email1, "pass": self.passwd1}

        self.username2 = self.UTILS.general.get_config_variable(self.testType.upper() + "_2_user", "common")
        self.email2 = self.UTILS.general.get_config_variable(self.testType.upper() + "_2_email", "common")
        self.passwd2 = self.UTILS.general.get_config_variable(self.testType.upper() + "_2_pass", "common")
        self.user2 = {"username": self.username2, "email": self.email2, "pass": self.passwd2}

        self.data_layer.connect_to_wifi()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.send_email(self.user1, self.user2)
