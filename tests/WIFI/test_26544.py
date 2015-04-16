from OWDTestToolkit.firec_testcase import FireCTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(FireCTestCase):

    def setUp(self):
        # Set up child objects...
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        #
        # Open the Settings application.
        #
        self.settings.launch()
        self.settings.wifi()
        self.settings.wifi_switchOn()

        self.UTILS.reporting.logResult('info', 'ready to look for networks')
        cuca = self.UTILS.element.getElements(
            DOM.Settings.wifi_available_networks, "Available networks", False)
        available_networks = [n.text for n in cuca]
        self.UTILS.reporting.logResult("info", "Found {} networks".format(len(available_networks)))
        
        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult('info', "Screenshot", screenshot)

        for index, network in enumerate(available_networks):
            self.UTILS.reporting.logResult('info', 'Iterating over network #{}'.format(index))
            # self.UTILS.element.scroll_into_view(network)

            try:
                # network.find_element(*("css selector", "aside.secured"))
                # network.find_element(*("css selector", "small[data-l10n-id='securedBy']"))
                self.marionette.find_element(
                    *('xpath', '//li//a[text()="{}"]//..//aside[contains(@class, "secured")]'.format(network)))
                self.marionette.find_element(
                    *('xpath', '//li//a[text()="{}"]//..//small[@data-l10n-id="securedBy"]'.format(network)))
                self.UTILS.reporting.logResult('info', "Network [{}] is secured".format(network))
            except:
                self.UTILS.reporting.logResult('info', "Network [{}] is NOT secured".format(network))
