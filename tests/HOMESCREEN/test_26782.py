#===============================================================================
# 26782: Remove all the categories from ev.me
#
# Pre-requisites:
# The user has some app in ev.me
#
# Procedure:
# 1. long-tap in categories (enter remove mode)
# 2. Remove every category
# 3. Check that no more categories are available
#
# Expected results:
# The ev.me page must be empty
#===============================================================================

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings
from marionette import Actions


class test_main(SpreadtrumTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)

        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.EME = EverythingMe(self)
        self.actions = Actions(self.marionette)

        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
            self.apps.set_permission('Smart Collections', 'geolocation', 'deny')
        except:
            self.UTILS.reporting.logComment("Unable to automatically set geolocation permission.")

    def tearDown(self):
        # Restart device to restore collections
        self.device.restart_b2g()
        SpreadtrumTestCase.setUp(self)
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)
        categories = self.UTILS.element.getElements(DOM.EME.all_collections, "All collections")
        for cat in categories:
            name = self.marionette.find_element('css selector', 'span.title', cat.id).text
            self.UTILS.reporting.debug("** Removing collection: {}".format(name))
            self.actions.long_press(cat, 2).perform()
            delete_btn = ("xpath", DOM.Home.app_delete_icon_xpath.format(name))
            delete_button = self.UTILS.element.getElement(delete_btn, "Delete button", False, 30, True)
            delete_button.tap()

            delete = self.UTILS.element.getElement(DOM.Home.app_confirm_delete, "Confirm app delete button")
            delete.tap()

        self.UTILS.element.waitForNotElements(DOM.EME.all_collections, "All collections", timeout=10)
