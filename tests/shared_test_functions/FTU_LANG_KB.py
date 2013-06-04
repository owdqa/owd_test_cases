#
# Starts FTU, selects a language, clicks through to emali field of privacy screen
# and taps it to bring up the kayboard.
# Then it compares screenshot sizes of the keyboard to try and estabish that the
# correct keyboard is being displayed.
#
# Currently used by tests 42,43 and 44.
#

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
import os

class main():
    
    def __init__(self, p_parent, p_lang, p_sizes):
        self.LANG       = p_lang
        self.SIZES      = p_sizes
        self.parent     = p_parent
        self.marionette = self.parent.marionette
        
        self.FTU        = AppFTU(self.parent)
        
        # (just to get autocomplete to work in my IDE!)
        self.UTILS      = UTILS(self.parent)
        if True: self.UTILS = self.parent.UTILS
        
        self.marionette.set_search_timeout(50)
        self.parent.lockscreen.unlock()
        
        #
        # Turn off all networking.
        #
        self.parent.data_layer.disable_cell_data()
        self.parent.data_layer.disable_wifi()

    def _checkSize(self, p_x, p_a, p_b):
        x = p_x + " keyboard image = "
        x = x + str(p_a) + " bytes (it was " + str(p_b)
        x = x + "). See the screenshot for details."
        self.UTILS.TEST((p_a == p_b), x )
        
    def run(self):

        #
        # Launch FTU app.
        #
        self.FTU.launch()

        #
        # LANGUAGE.
        #
        self.UTILS.TEST(self.FTU.setLanguage(self.LANG), 
            "Language '" + self.LANG + "' is available on this device.", True)
        self.FTU.nextScreen()
        
        #
        # DATA CONNECTIVITY (skip).
        #
        self.FTU.nextScreen()
        
        #
        # WIFI CONNECTIVITY (skip).
        #
        self.FTU.nextScreen()
        
        #
        # TIMEZONE (skip).
        #
        self.FTU.nextScreen()
        
        #
        # IMPORT CONTACTS (skip).
        #
        self.FTU.nextScreen()
        
        #
        # PRIVACY SCREEN - share data (skip).
        #
        self.FTU.nextScreen()
        
        #
        # PRIVACY SCREEN - info. email.
        #
        # Click the email area to display the keyboard.
        x = self.UTILS.getElement(DOM.FTU.privacy_email, "Privacy policy email address")
        x.click()
        self.parent.keyboard._switch_to_keyboard()
        
        #
        # Take a screenshot of each view and check the size.
        #
        
        imgnam  = self.UTILS.screenShot("42_lowercase_alpha")
        self.UTILS.logComment("Screenshot of lowercase alpha keyboard = " + imgnam)
        imgsize = os.path.getsize(imgnam)
        self._checkSize("Lowercase alpha", self.SIZES[0], imgsize)

        self.parent.keyboard.tap_shift()
        imgnam  = self.UTILS.screenShot("42_uppercase_alpha")
        self.UTILS.logComment("Screenshot of uppercase alpha keyboard = " + imgnam)
        imgsize = os.path.getsize(imgnam)
        self._checkSize("Uppercase alpha", self.SIZES[1], imgsize)
        
        self.parent.keyboard.switch_to_number_keyboard()
        imgnam  = self.UTILS.screenShot("42_numeric")
        self.UTILS.logComment("Screenshot of numeric keyboard = " + imgnam)
        imgsize = os.path.getsize(imgnam)
        self._checkSize("Numeric", self.SIZES[2], imgsize)
        
        self.parent.keyboard.tap_alt()
        imgnam  = self.UTILS.screenShot("42_alt_numeric")
        self.UTILS.logComment("Screenshot of alt numeric keyboard = " + imgnam)
        imgsize = os.path.getsize(imgnam)
        self._checkSize("Alt numeric", self.SIZES[3], imgsize)
        
