from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(GaiaTestCase):

    test_msg = "First message."

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Launch messages app.
        self.messages.launch()

        # Create and send some new tests messages.
        self.messages.create_and_send_sms([self.phone_number], self.test_msg)
        self.messages.wait_for_message()

        self.messages.go_back()

        # Delete this thread.
        self.messages.deleteThreads([self.phone_number])

        # Check thread isn't there anymore.
        self.UTILS.element.waitForNotElements(("xpath", DOM.Messages.thread_selector_xpath.format(self.phone_number)),
                                      "Thread")
