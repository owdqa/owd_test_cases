#===============================================================================
# 27736: Press delete without any conversation selected
#
# Procedure:
# 1- Access to SMS app
# 2- Press edit button
# 3- Try Press delete button
#
# Expected results:
# It is impossible to press the button "delete" or if we press the button,
# it doesn't do anything
#===============================================================================

from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Using target telephone number " + self.phone_number)
        self.incoming_sms_num = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.messages.launch()

        sms_msg = "Just creating a message thread."
        self.UTILS.messages.create_incoming_sms(self.phone_number, sms_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(sms_msg, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.incoming_sms_num, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)

        # Return to main SMS page.
        self.messages.closeThread()

        # Press the edit button (without selecting any threads).
        self.messages.editAndSelectThreads([])

        # Check that the delete button is not enabled.
        delete_btn = self.UTILS.element.getElement(DOM.Messages.threads_delete_button, "Delete button")
        disabled = delete_btn.get_attribute("disabled")
        self.UTILS.test.test(disabled, "Delete button is not enabled.")
