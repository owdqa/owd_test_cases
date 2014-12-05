#===============================================================================
# 29914: Verify that when sending a mms to multiple recipients (contacts),
# only a new thread will be created for the message
#
# Pre-requisites:
# Contacts imported from different sources (facebook, gmail, hotmail, SIM
# card) into the addressbook
#
# Procedure:
# 1. Open SMS app
# 2. Tap on new to create a new MMS(attach a file)
# 3. Tap on '+' icon to add a recipient. Repeat this step several times
# selecting contacts from different sources (ER1)
# 4. Type some characters and tap on Send (ER2)
# 5. Look at the Inbox (ER3)
#
# Expected results:
# ER1. All the recipients are correctly added
# ER2. The message is sent to all the recipients
# ER3. On the inbox view there would be only one MMS thread for the
# multi-recipient MMS sent
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)

        self.test_msg = "Hello World"

        #
        # Establish which phone number to use.
        #
        num1 = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.contact1 = MockContact(givenName="Name 1", familyName="Surname 1",
                                    name="Name 1 Surname 1", tel={"type": "Mobile", "value": num1})
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact1["tel"]["value"])
        self.UTILS.general.insertContact(self.contact1)

        num2 = self.UTILS.general.get_config_variable("incoming_call_number", "common")
        self.contact2 = MockContact(givenName="Name 3", familyName="Surname 3",
                                    name="Name 3 Surname 3", tel={"type": "Mobile", "value": num2})
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact2["tel"]["value"])
        self.UTILS.general.insertContact(self.contact2)
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()
        self.test_nums = [self.contact1["tel"]["value"], self.contact2["tel"]["value"]]

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.messages.launch()

        # Create a new SMS
        self.messages.startNewSMS()

        # Insert the phone numbers in the To field
        for num in self.test_nums:
            self.messages.addNumbersInToField([num])

        # Create MMS.
        self.messages.enterSMSMsg(self.test_msg)

        # Add an image file
        self.UTILS.general.add_file_to_device('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')
        self.messages.create_mms_image()
        self.gallery.click_on_thumbnail_at_position_mms(0)

        # Click send and wait for the message to be received
        self.messages.sendSMS()
        send_time = self.messages.last_sent_message_timestamp()
        self.messages.closeThread()
        self.messages.openThread(self.contact1["name"])
        self.messages.wait_for_message(send_time=send_time)

        #
        # Obtaining file attached type
        #
        img_type = self.UTILS.element.getElement(DOM.Messages.attach_preview_img_type, "preview type")
        typ = img_type.get_attribute("data-attachment-type")

        if typ != "img":
            self.UTILS.test.test(False, "Incorrect file type. The file must be img ")

        self.messages.closeThread()

        #
        # Check how many elements are there
        #
        self.UTILS.reporting.logResult("info", "Check how many threads are there")
        original_count = self.messages.countNumberOfThreads()
        self.UTILS.reporting.logResult("info", "Number of threads {} in list.".format(original_count))
        self.UTILS.test.test(original_count == 2, "Check how many threads are there")
