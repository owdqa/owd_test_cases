#===============================================================================
# 27051: Verify that the number of contacts to be imported is shown
#
# Pre-requisites:
# To have a Hotmail account with several contacts available to show/import
#
# Procedure:
# 1. Open Contacts app
# 2. Go to Settings
# 3. Tap on Import from Hotmail
# 4. The log in screen is shown
# 5. Introduce a valid user/password
# 6. Tap on Sign In
# 7. Once the list of contacts is shown verify whether the number of contacts
# to be imported is shown
#
# Expected results:
# There should appear the number of contacts available to be imported
#===============================================================================

import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.hotmail_user = self.UTILS.general.get_config_variable("hotmail_2_email", "common")
        self.hotmail_passwd = self.UTILS.general.get_config_variable("hotmail_2_pass", "common")

        # Get details of our test contacts.
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Set up to use data connection.
        self.data_layer.connect_to_cell_data()

        self.contacts.launch()

        login_result = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)

        # Login unsuccessful or no available contacts to import
        if not login_result:
            self.UTILS.test.test(False, "Login unsuccessful")

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.hotmail_import_frame, via_root_frame=False)
        contact_list = self.UTILS.element.getElements(DOM.Contacts.import_conts_list, "Contact list")
        cont_count = len(contact_list)

        num_contacts = self.UTILS.element.getElement(DOM.Contacts.import_num_of_conts, "Number of contacts")
        self.UTILS.reporting.logResult("info", "Detected message '{}'.".format(num_contacts.text))

        self.UTILS.test.test(str(cont_count) in num_contacts.text, "'{}' contains the real count, which is {}.".\
                        format(num_contacts.text, cont_count))
