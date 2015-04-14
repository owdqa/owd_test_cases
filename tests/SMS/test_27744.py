#
# 27744: Introduce a valid SMS and click on Back option
#
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(FireCTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Start a new sms.
        #
        self.messages.startNewSMS()

        #
        # Enter a number in the target field.
        #
        self.messages.addNumbersInToField([self.phone_number])

        #
        # Enter a message the message area.
        #
        self.messages.enterSMSMsg("xxx")

        #
        # Click the back button.
        #
        back_btn = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        back_btn.tap()

        #
        # Check for the save/discard popup.
        #
        discard_btn = self.UTILS.element.getElement(DOM.Messages.discard_msg_btn, "Discard button")
        discard_btn.tap()

        #
        # Verify that we're now in the correct place.
        #
        self.UTILS.element.headerCheck("Messages")
        threads = self.UTILS.element.getElement(DOM.Messages.no_threads_message, "No threads message")
        self.UTILS.test.test(threads, "There are no threads, as expected")
