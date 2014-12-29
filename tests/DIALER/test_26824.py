from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer

class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.test_number = "123456789"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()
        self.dialer.enterNumber(self.test_number)

        add_to_contacts_button = self.UTILS.element.getElement(DOM.Dialer.add_to_contacts_button, "Add to contacts button")
        add_to_contacts_button.tap()

        cancel_button = self.UTILS.element.getElement(DOM.Dialer.cancel_action, "Cancel button")
        cancel_button.tap()

        phone_field = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = phone_field.get_attribute("value")
        self.UTILS.test.test(str(self.test_number) in dialer_num, "After cancelling, phone number field still contains '%s' (it was %s)." % \
                                                       (self.test_number,dialer_num))
