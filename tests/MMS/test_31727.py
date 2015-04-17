#
# 31727: Sending PNG file
#
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery


class test_main(PixiTestCase):

    test_msg = "Hello World"

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.test_msg = "Test message for test 31727"
        self.UTILS.general.add_file_to_device('./tests/_resources/300x300.png', destination='DCIM/100MZLLA')

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        self.messages.launch()
        self.messages.startNewSMS()
        self.messages.addNumbersInToField([self.phone_number])
        self.messages.enterSMSMsg(self.test_msg)
        self.messages.create_mms_image()
        self.gallery.click_on_thumbnail_at_position_mms(0)
        self.messages.sendSMS()

        self.messages.wait_for_message()
        self.messages.check_last_message_contents(self.test_msg, mms=True)
        self.messages.verify_mms_received('img', self.phone_number)
