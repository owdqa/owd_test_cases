#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContact

class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.email      = Email(self)
                
        #
        # Get details of our test contacts.
        #
        email1 = self.UTILS.get_os_variable("GMAIL_1_EMAIL")
        email2 = self.UTILS.get_os_variable("GMAIL_2_EMAIL")
        email3 = self.UTILS.get_os_variable("HOTMAIL_1_EMAIL")
        self.Contact_1 = MockContact(email = [{
            'type': 'Personal',
            'value': email1}, {
            'type': 'Personal',
            'value': email2}, {
            'type': 'Personal',
            'value': email3}
        ])

        #
        # We're not testing adding a contact, so just stick one 
        # into the database.
        #
        self.UTILS.insertContact(self.Contact_1)
        
        self._email_subject = "TEST " + str(time.time())
        self._email_message = "Test message"
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
    
        self.UTILS.getNetworkConnection()
        
        #
        # Set up to use email (with account #1).
        #
        em_user = self.UTILS.get_os_variable("GMAIL_1_USER")
        em_email= self.UTILS.get_os_variable("GMAIL_1_EMAIL")
        em_pass = self.UTILS.get_os_variable("GMAIL_1_PASS")
        self.email.launch()
        self.email.setupAccount(em_user, em_email, em_pass)
        
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # View the details of our contact.
        #
        self.contacts.viewContact(self.Contact_1['name'])
        
        #
        # Click the 2nd email button
        #
        emailBTN = self.UTILS.getElement( ("id", DOM.Contacts.email_button_spec_id % 1), 
                                        "2nd send Email address in for this contact")
        emailBTN.tap()

        #
        # Switch to email frame.
        #
        time.sleep(5)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Email.frame_locator) 
        
        #
        # Verify the 'to' field is correct.
        #
        expected_to = self.Contact_1["email"][1]["value"]
        y = self.UTILS.getElement(DOM.Email.compose_to_from_contacts, "'To' field")
        self.UTILS.TEST(y.text == expected_to,
                        "The 'to' field contains '" + expected_to + "' (it was (" + y.text + ").")
        
        #
        # Fill in the rest and send it.
        #
#         msg_subject = self.UTILS.getElement(DOM.Email.compose_subject, "'Subject' field")
#         msg_msg     = self.UTILS.getElement(DOM.Email.compose_msg, "Message field")
#         msg_subject.send_keys(self._email_subject)
#         msg_msg.send_keys(self._email_message)
        self.UTILS.typeThis(DOM.Email.compose_subject, "'Subject' field", self._email_subject, True, False)
        self.UTILS.typeThis(DOM.Email.compose_msg    , "Message field"  , self._email_message, True, False, False)

         
        #
        # Send the message.
        #
        self.email.sendTheMessage()