from gaiatest import GaiaTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.browser import Browser


class test_main(GaiaTestCase):

    link = "www.wikipedia.o"
    test_msg = "Test " + link + " this."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.browser = Browser(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.connect_to_network()

        #
        # Launch messages app.
        #
        self.messages.launch()
  
        #
        # Create and send a new test message.
        #
        self.messages.create_and_send_sms([self.phone_number], self.test_msg)
  
        #
        # Wait for the last message in this thread to be a 'received' one
        # and click the link.
        #
        x = self.messages.wait_for_message()
        self.UTILS.test.test(x, "Received a message.", True)



        boolOK=False
        try:
            x.find_element("tag name", "a")
        except:
            boolOK = True


        self.UTILS.test.test(boolOK, "The web address is not a link in the text message")