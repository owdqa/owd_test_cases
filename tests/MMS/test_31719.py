#
# TC_MMSTC_COMPT_015b
# USIM Addresses
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.gallery import Gallery


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)
        self.gallery = Gallery(self)

        self.test_num = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.cont = MockContact(tel={"type": "Mobile", "value": self.test_num})

        self.UTILS.general.insertContact(self.cont)
        self.UTILS.general.add_file_to_device('./tests/_resources/imga.jpg', destination='DCIM/100MZLLA')
        self.UTILS.reporting.logComment("Using target telephone number " + self.cont["tel"]["value"])

    def tearDown(self):
        self.UTILS.general.remove_file('imga.jpg', 'DCIM/100MZLLA')
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.messages.launch()

        self.messages.startNewSMS()
        self.messages.enterSMSMsg("Test")

        self.messages.create_mms_image()
        self.gallery.click_on_thumbnail_at_position_mms(0)

        # Search for our contact.
        time.sleep(5)
        self.messages.selectAddContactButton()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        self.contacts.search(self.cont["name"])
        self.contacts.check_search_results(self.cont["name"])

        result = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Contacts search results")
        for contact in result:
            if contact.text == self.cont["name"]:
                contact.tap()
                break

        self.apps.switch_to_displayed_app()

        # Now check the correct name is in the 'To' list.
        self.messages.checkIsInToField(self.cont["name"])
        self.messages.sendSMS()
