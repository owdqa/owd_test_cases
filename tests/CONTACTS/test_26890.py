from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts

class test_main(PixiTestCase):

    name = "Obi"
    surname = "Wan"

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

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
        given_name = self.UTILS.element.getElement(DOM.Contacts.given_name_field, "Given name field")
        given_name.send_keys(self.name)

        #
        # Press the 'x'.
        #
        reset = self.UTILS.element.getElement(DOM.Contacts.given_name_reset_icon, "Given name reset icon")
        reset.tap()

        #
        # Click the header, then verify that the field contains nothing.
        #
        self.marionette.find_element("xpath", '//h1[@id="contact-form-title"]').tap()
        given_name = self.UTILS.element.getElement(DOM.Contacts.given_name_field, "Given name field")
        self.UTILS.test.test(given_name.text == "", "Given name field is empty after being cleared.")

        #
        # Add some info. to the field.
        #
        surname = self.UTILS.element.getElement(DOM.Contacts.family_name_field, "Surname field")
        surname.send_keys(self.surname)
        #
        # Press the 'x'.
        #
        reset = self.UTILS.element.getElement(DOM.Contacts.family_name_reset_icon, "Surname reset icon")
        reset.tap()

        #
        # Click the header, then verify that the field contains nothing.
        #
        self.marionette.find_element("xpath", '//h1[@id="contact-form-title"]').tap()
        surname = self.UTILS.element.getElement(DOM.Contacts.family_name_field, "Surname field")
        self.UTILS.test.test(surname.text == "", "Surname field is empty after being cleared.")
