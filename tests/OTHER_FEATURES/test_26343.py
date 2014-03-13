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
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Contacts
import time

class test_main(GaiaTestCase):

    _test_apps = ["Gallery", "FM Radio"]
    _img_list  = ('img1.jpg', 'img2.jpg')
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)

        
    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Load a couple of images into the gallery.
        #
        for i in self._img_list:
            self.UTILS.addFileToDevice('./tests/_resources/' + i, destination='DCIM/100MZLLA')
    
        self.UTILS.goHome()
        
        #
        # launch the test apps (lifted directly from gaiatest).
        #
        gallery_app = {
            'name': "Gallery",
            'app': self.apps.launch("Gallery"),
            'card': (DOM.Home.app_card[0], DOM.Home.app_card[1].format("gallery")),
            'close_button': (DOM.Home.app_close[0], DOM.Home.app_close[1].format("gallery"))
        }
        radio_app = {
            'name': "FM Radio",
            'app': self.apps.launch("FM Radio"),
            'card': (DOM.Home.app_card[0], DOM.Home.app_card[1].format("fm")),
            'close_button': (DOM.Home.app_close[0], DOM.Home.app_close[1].format("fm"))
        }

        self.UTILS.touchHomeButton()
        time.sleep(1)
        
        self.UTILS.holdHomeButton()
        
        x = self.UTILS.waitForElements(DOM.Home.cards_view, "App 'cards' list")
        
        #
        # Flick it up (not working currently - retry when marionette toch is working).
        #
# #         x = self.UTILS.getElement(*self.test_apps[len(self.test_apps)-1]["card"])
#         els = self.marionette.find_elements(*DOM.Home.app_cards)
#         from marionette import Actions
#         actions = Actions(self.marionette)
#         for x in els:
#             actions.press(x, x.size["width"], x.size["height"]).move_by_offset(x.size["width"], 0).release()
#             actions.perform()
#             
# #             x_x = int(x.size['width'] / 2)
# #             x_y = int(x.size['height'] / 2)
# USE ACTION CHAIN FLICK()
# #             self.marionette.flick(x, x_x, x_y, x_x, 0, 500)
        
        #
        # For now just click the close_button
        #
        self.UTILS.logComment("(Didn't drag the app 'up' to close it, I just clicked the 'close' button.)")

        # Kill the radio.
        x = self.UTILS.getElement(radio_app["close_button"], "Close button on '" + radio_app["name"] + "' card")
        x.tap()        
        self.UTILS.waitForNotElements(radio_app["card"], "Card for '" + radio_app["name"] + "'", True, 5, False)

        # Open the gallery.
        x = self.UTILS.getElement(gallery_app["card"], "Card for '" + gallery_app["name"] + "'")
        x.tap()
        
        time.sleep(3)
        self.UTILS.switchToFrame(*DOM.Gallery.frame_locator)
