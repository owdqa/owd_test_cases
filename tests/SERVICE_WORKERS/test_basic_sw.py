#===============================================================================
# Basic SW test
#===============================================================================
import os
import sys
sys.path.insert(1, os.path.dirname(__file__))

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings
import dom


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.browser = Browser(self)
        self.settings = Settings(self)

        self.wifi_name = self.UTILS.general.get_config_variable("ssid", "wifi")
        self.wifi_pass = self.UTILS.general.get_config_variable("password", "wifi")
        self.data_layer.connect_to_wifi()
        self.data_layer.is_wifi_connected()

        self.apps.kill_all()
        self.url = "http://jaoo.github.io/service-worker-testing/index.html"
        self.sw_scope = "http://jaoo.es/service-worker-testing/"
        self.sw_header = "http://jaoo.es!appId=22&inBrowser=1"
        self.script_spec = "http://jaoo.es/service-worker-testing/service.js"

    def tearDown(self):
        self.data_layer.disable_wifi()
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.browser.launch()
        self.browser.open_url(self.url)

        register_btn = self.UTILS.element.getElement(dom.register_btn_dom, "Register Worker button")
        register_btn.tap()

        self.settings.launch()
        time.sleep(2)
        self.settings.developer_settings()
        time.sleep(2)
        self.settings.service_workers_menu()
        header_dom = (DOM.Settings.service_worker_header[0], DOM.Settings.service_worker_header[1].format(self.sw_scope))
        header = self.UTILS.element.getElement(header_dom, "Service worker header")
        self.UTILS.test.test(header.text == self.sw_header, "Header found [{}] Expected [{}]".
                             format(header.text, self.sw_header))

        scope = self.UTILS.element.getElement(DOM.Settings.service_worker_scope, "Service worker scope")
        self.UTILS.test.test(self.sw_scope == scope.text, "Scope found [{}] Expected [{}]".
                             format(scope.text, self.sw_scope))
        script_spec = self.UTILS.element.getElement(DOM.Settings.service_worker_script_spec,
                                                    "Service worker script spec")
        self.UTILS.test.test(self.script_spec == script_spec.text, "Script spec found [{}] Expected [{}]".
                             format(script_spec.text, self.script_spec))
        worker_url = self.UTILS.element.getElement(DOM.Settings.service_worker_current_url,
                                                   "Service worker current url")
        self.UTILS.test.test(self.script_spec == worker_url.text, "URL found [{}] Expected [{}]".
                             format(worker_url.text, self.script_spec))
        unregister_btn = self.UTILS.element.getElement(DOM.Settings.service_worker_unregister_btn,
                                                       "Unregister button")
        unregister_btn.tap()
