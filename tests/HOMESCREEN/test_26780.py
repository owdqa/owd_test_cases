#===============================================================================
# 26780: Verify that when an app is launched from everything.me a bottom
# bar is shown so that the user can go back, go forward, refresh, bookmark
# and close the bottom bar
#
# Procedure:
# 1- Navigate to everything.me main page
# 2- Type a category in the search bar (e.g. Sports)
# 3- Open an app from this category
#
# Expected results:
# The wrapper occupies a minimal amount of the screen and it is only opened
# when the user taps on it. A wizard to allow the user know about the wrapper
# will be shown first time user opens an application with the wrapper.
#===============================================================================
import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


class test_main(FireCTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)

        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.EME = EverythingMe(self)
        self.cat_id = "207"
        self.app_name = "Simon Says"

        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
            self.apps.set_permission('Smart Collections', 'geolocation', 'deny')
            self.apps.set_permission('Search Results', 'geolocation', 'deny')
        except:
            self.UTILS.reporting.logComment("Unable to automatically set geolocation permission.")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.connect_to_wifi()

        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)

        search_input = self.UTILS.element.getElement(DOM.EME.search_field, "Search input field")
        search_input.tap()
        self.UTILS.general.keyboard.send("Games")
        self.UTILS.iframe.switchToFrame(*DOM.EME.search_frame_locator)
        btn = self.UTILS.element.getElement(DOM.EME.suggestions_notice_confirm_btn, "Suggestions confirmation button",
                                            timeout=30)
        btn.tap()
        time.sleep(5)
        simon = self.UTILS.element.getElementByXpath(DOM.EME.app_to_install.format(self.app_name))
        simon_url = simon.get_attribute("data-identifier")
        self.UTILS.reporting.debug("Simon Says URL: {}".format(simon_url))
        simon.tap()
        time.sleep(5)
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForElements(DOM.EME.footer_navigation_bar, "Footer navigation bar", timeout=30)
        bar = self.UTILS.element.getElement(DOM.EME.footer_navigation_bar, "Footer navigation bar")
        bar.tap()

        self.UTILS.element.waitForElements(DOM.EME.launched_button_back, "Button bar - back button")
        self.UTILS.element.waitForElements(DOM.EME.launched_button_forward, "Button bar - forward button")
        self.UTILS.element.waitForElements(DOM.EME.launched_button_reload, "Button bar - reload button")
        self.UTILS.element.waitForElements(DOM.EME.launched_button_bookmark, "Button bar - bookmark button")
        self.UTILS.element.waitForElements(DOM.EME.launched_button_close, "Button bar - close button")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of the button bar:", x)
