#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts

class test_main(GaiaTestCase):

    name = "Obi"
    surname = "Wan"

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Click create new contact.
        #
        self.contacts.start_create_new_contact()

        #
        # Add some info. to the field.
        #
        self.UTILS.general.typeThis(DOM.Contacts.given_name_field,
                            "Given name field",
                            self.name,
                            p_no_keyboard=False,
                            p_clear=True,
                            p_enter=False,
                            p_validate=True,
                            p_remove_keyboard=False)

        #
        # Press the 'x'.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.given_name_reset_icon, "Given name reset icon")
        x.tap()

        #
        # Click the header, then verify that the field contains nothing.
        #
        self.marionette.find_element("tag name", "h1").tap()
        x = self.UTILS.element.getElement(DOM.Contacts.given_name_field, "Given name field")
        self.UTILS.test.TEST(x.text == "", "Given name field is empty after being cleared.")

        #
        # Add some info. to the field.
        #
        self.UTILS.general.typeThis(DOM.Contacts.family_name_field,
                            "Surname field",
                            self.surname,
                            p_no_keyboard=False,
                            p_clear=True,
                            p_enter=False,
                            p_validate=True,
                            p_remove_keyboard=False)

        #
        # Press the 'x'.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.family_name_reset_icon, "Surname reset icon")
        x.tap()

        #
        # Click the header, then verify that the field contains nothing.
        #
        self.marionette.find_element("tag name", "h1").tap()
        x = self.UTILS.element.getElement(DOM.Contacts.family_name_field, "Surname field")
        self.UTILS.test.TEST(x.text == "", "Surname field is empty after being cleared.")
