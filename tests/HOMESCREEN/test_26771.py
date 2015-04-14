#===============================================================================
# 26771: Launch a intallation doing a long-tap on any app shown
# by everything.me and press Yes button
#
# Procedure:
# 1- Open everything.me
# 2- open a category or search by text
# 3- do a long-tap on any app shown by everything.me
# ER1
# 4-Press Yes button
# ER2
#
# Expected results:
# ER1- The app installation is launched and a confirmation is displayed
# ER2- The application is installed, that means that an icon is placed
# on the last position available on the application grid with the application
# name label.
#===============================================================================


from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM
import time


class test_main(FireCTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    _GROUP_NAME = "Games"

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)

        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.EME = EverythingMe(self)

        #
        # Don't prompt me for geolocation
        #
        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
            self.apps.set_permission('Smart Collections', 'geolocation', 'deny')
        except:
            self.UTILS.reporting.logComment("Unable to automatically set geolocation permission.")

        self.cat_id = "289"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.connect_to_wifi()

        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)
        self.EME.pick_group(self.cat_id)
        self.UTILS.iframe.switchToFrame(*DOM.EME.frame_locator)
        app_name = self.UTILS.element.getElementByXpath(DOM.EME.app_to_install.format("Line")).text
        self.EME.add_app_to_homescreen(app_name)

        self.UTILS.iframe.switchToFrame(*DOM.EME.bookmark_frame_locator)
        time.sleep(2)
        add_btn = self.UTILS.element.getElement(DOM.EME.add_bookmark_btn, "Add bookmark to Home Screen Button")
        add_btn.tap()
        time.sleep(4)

        self.UTILS.home.goHome()
        self.UTILS.app.uninstallApp(app_name)
