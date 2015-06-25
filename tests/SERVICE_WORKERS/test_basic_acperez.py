#===============================================================================
# Basic SW test https://acperez.github.io/gecko-sw-test/
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
        self.url = "https://acperez.github.io/gecko-sw-test/"
        self.sw_scope = "https://acperez.github.io/gecko-sw-test/"
        self.sw_header = "https://acperez.github.io!appId=22&inBrowser=1"
        self.script_spec = "https://acperez.github.io/gecko-sw-test/service-worker.js"

    def tearDown(self):
        self.data_layer.disable_wifi()
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.browser.launch()
        self.browser.open_url(self.url)

        register_btn = self.UTILS.element.getElement(dom.acperez_register_btn_dom, "Register Worker button")
        register_btn.tap()

        self.settings.launch()
        time.sleep(2)
        self.settings.developer_settings()
        time.sleep(2)
        self.settings.service_workers_menu()

        div_dom = (DOM.Settings.service_worker_div[0], DOM.Settings.service_worker_div[1].format(self.sw_scope))
        div_elem = self.UTILS.element.getElement(div_dom, "Service worker div")
        self.UTILS.element.scroll_into_view(div_elem)

        header = div_elem.find_element(*DOM.Settings.service_worker_header)
        self.UTILS.test.test(header.text == self.sw_header, "Header found [{}] Expected [{}]".
                             format(header.text, self.sw_header))

        scope = div_elem.find_element(*DOM.Settings.service_worker_scope)
        self.UTILS.test.test(self.sw_scope == scope.text, "Scope found [{}] Expected [{}]".
                             format(scope.text, self.sw_scope))

        script_spec = div_elem.find_element(*DOM.Settings.service_worker_script_spec)
        self.UTILS.test.test(self.script_spec == script_spec.text, "Script spec found [{}] Expected [{}]".
                             format(script_spec.text, self.script_spec))

        worker_url = div_elem.find_element(*DOM.Settings.service_worker_current_url)
        self.UTILS.test.test(self.script_spec == worker_url.text, "URL found [{}] Expected [{}]".
                             format(worker_url.text, self.script_spec))

        unregister_btn = div_elem.find_element(*DOM.Settings.service_worker_unregister_btn)
        unregister_btn.tap()

