#
# Starts ftu, selects a language, clicks through to emali field of privacy screen
# and taps it to bring up the kayboard.
# Then it compares screenshot sizes of the keyboard to try and estabish that the
# correct keyboard is being displayed.
#
# Currently used by tests 42,43 and 44.
#

from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.apps import Ftu
from OWDTestToolkit.utils.utils import UTILS

import os


class FtuLangKb(FireCTestCase):

    def __init__(self, parent, lang, sizes):
        self.lang = lang
        self.sizes = sizes
        self.parent = parent
        self.marionette = self.parent.marionette

        self.ftu = Ftu(self.parent)

        # (just to get autocomplete to work in my IDE!)
        self.UTILS = UTILS(self.parent)
        if True:
            self.UTILS = self.parent.UTILS

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
        self.UTILS.test.test((p_a == p_b), x)

    def run(self):
        #
        # Launch ftu app.
        #
        self.ftu.launch()

        #
        # LANGUAGE.
        #
        self.UTILS.test.test(self.ftu.setLanguage(self.lang),
            "Language '" + self.lang + "' is available on this device.", True)
        self.ftu.nextScreen()

        #
        # DATA CONNECTIVITY (skip).
        #
        self.ftu.nextScreen()

        #
        # WIFI CONNECTIVITY (skip).
        #
        self.ftu.nextScreen()

        #
        # TIMEZONE (skip).
        #
        self.ftu.nextScreen()

        #
        # IMPORT CONTACTS (skip).
        #
        self.ftu.nextScreen()

        #
        # PRIVACY SCREEN - share data (skip).
        #
        self.ftu.nextScreen()

        #
        # PRIVACY SCREEN - info. email.
        #
        # Click the email area to display the keyboard.
        x = self.UTILS.element.getElement(DOM.ftu.privacy_email, "Privacy policy email address")
        x.tap()
        self.parent.keyboard._switch_to_keyboard()

        #
        # Take a screenshot of each view and check the size.
        #

        imgnam = self.UTILS.debug.screenShot("42_lowercase_alpha")
        self.UTILS.reporting.logComment("Screenshot of lowercase alpha keyboard = " + imgnam)
        imgsize = os.path.getsize(imgnam)
        self._checkSize("Lowercase alpha", self.sizes[0], imgsize)

        self.keyboard.tap_shift()
        imgnam = self.UTILS.debug.screenShot("42_uppercase_alpha")
        self.UTILS.reporting.logComment("Screenshot of uppercase alpha keyboard = " + imgnam)
        imgsize = os.path.getsize(imgnam)
        self._checkSize("Uppercase alpha", self.sizes[1], imgsize)

        self.parent.keyboard.switch_to_number_keyboard()
        imgnam = self.UTILS.debug.screenShot("42_numeric")
        self.UTILS.reporting.logComment("Screenshot of numeric keyboard = " + imgnam)
        imgsize = os.path.getsize(imgnam)
        self._checkSize("Numeric", self.sizes[2], imgsize)

        self.keyboard.tap_alt()
        imgnam = self.UTILS.debug.screenShot("42_alt_numeric")
        self.UTILS.reporting.logComment("Screenshot of alt numeric keyboard = " + imgnam)
        imgsize = os.path.getsize(imgnam)
        self._checkSize("Alt numeric", self.sizes[3], imgsize)
