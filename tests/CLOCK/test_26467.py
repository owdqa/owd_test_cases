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
#from datetime 
import datetime, time   

class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.clock      = Clock(self)
                        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch clock app.
        #
        self.apps.kill_all()
        time.sleep(3)
        self.clock.launch()
        
        #
        # Check that the face is analog.
        #
        x = self.UTILS.getElement(DOM.Clock.analog_face, "Analog clock face")
        
        #
        # Tap the clock face.
        #
        self.UTILS.logResult("info", "Tapping the clock face ...")
        try:
            x.tap()
            self.wait_for_element_displayed(*DOM.Clock.digital_face)
        except:
            #
            # For some reason this randomly doesn't work, so try again.
            #
            self.UTILS.logResult("info", 
                                 "<b>Note:</b> failed to tap the analog face - " +
                                 "suspect this is just a Marionette issue so I'm trying again.")
            self.apps.kill_all()
            time.sleep(2)
            self.clock.launch()
            x = self.UTILS.getElement(DOM.Clock.analog_face, "Analog clock face")
            x.tap()
            
        
        #
        # Check this is now the digital clock face.
        #
        self.UTILS.waitForElements(DOM.Clock.digital_face, "Digital clock face")
        
        #
        # Verify the time is correct (digits for hh and mm need to be padded).
        #
        device_ampm = self.UTILS.getElement( ("id", "clock-hour24-state"), "Clock time am / pm").text
        device_hhmm = self.UTILS.getElement( ("id", "clock-time"), "Clock time hh:mm").text
        device_hh   = device_hhmm.split(":")[0].zfill(2)
        device_mm   = device_hhmm.split(":")[1].zfill(2)
        
        device_time = device_hh + ":" + device_mm + device_ampm.zfill(2)
         
        now_hhmm = time.strftime("%I:%M")
        now_ampm = time.strftime("%r")[-2:]
        now_time = now_hhmm + now_ampm
         
        self.UTILS.TEST(now_time == device_time, 
                        "Digital display time is correct (now = '" + now_time + "', display = '" + device_time + "').",
                        False)
        
        #
        # Tap the clock face.
        #
        x = self.UTILS.getElement(DOM.Clock.digital_face, "Digital clock face", False)
        self.UTILS.logResult("info", "Tapping the clock face ...")
        try:
            x.tap()
            self.wait_for_element_displayed(*DOM.Clock.analog_face)
        except:
            #
            # For some reason this randomly doesn't work, so try again.
            #
            self.UTILS.logResult("info", 
                                 "<b>Note:</b> failed to tap the digital face - " +
                                 "suspect this is just a Marionette issue so I'm trying again.")
            self.UTILS.switchToFrame(*DOM.Clock.frame_locator)
            x = self.UTILS.getElement(DOM.Clock.digital_face, "Digital clock face")
            x.tap()
        
        #
        # Check that the face is analog again.
        #
        self.UTILS.waitForElements(DOM.Clock.analog_face, "Analog clock face")
        
