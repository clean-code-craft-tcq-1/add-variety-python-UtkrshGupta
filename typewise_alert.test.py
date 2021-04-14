import unittest
from typewise_alert import TypewiseAlert
from typewise_alert_Exception import Invalid_Input
        
class TypewiseTest(unittest.TestCase):
    def test_infers_breach_as_per_limits(self):
        twa = TypewiseAlert()
        self.assertTrue(twa.infer_breach(20, 50, 100) == 'TOO_LOW')
        self.assertTrue(twa.infer_breach(200, 50, 100) == 'TOO_HIGH')
        self.assertTrue(twa.infer_breach(70, 50, 100) == 'NORMAL')

    def test_to_check_and_alert_temperature_status(self):
        twa = TypewiseAlert()

# Test check and alert functionality ( returns flag as true if succesfully sent to corrsponding targets)

        self.assertTrue(twa.check_and_alert('TO_CONTROLLER', {'cooling_type': 'PASSIVE_COOLING'}, 70))
        self.assertTrue(twa.check_and_alert('TO_EMAIL', {'cooling_type': 'MED_ACTIVE_COOLING'}, 70))
        self.assertTrue(twa.check_and_alert('TO_CONSOLE', {'cooling_type': 'MED_ACTIVE_COOLING'}, 70))

# Dummy alteration of controller, email tcp and console active status
        
        twa.set_controller_status('OFF')
        twa.set_email_tcp_status('OFF')
        twa.set_console_status('OFF')
        self.assertFalse(twa.check_and_alert('TO_CONTROLLER', {'cooling_type': 'PASSIVE_COOLING'}, 70))
        self.assertFalse(twa.check_and_alert('TO_EMAIL', {'cooling_type': 'MED_ACTIVE_COOLING'}, 70))
        self.assertFalse(twa.check_and_alert('TO_CONSOLE', {'cooling_type': 'MED_ACTIVE_COOLING'}, 70))

        twa.set_controller_status('ON')
        twa.set_email_tcp_status('ON')
        twa.set_console_status('ON')
        
# Test to raise Invalid Input arguments exception     
        self.assertRaises(Invalid_Input, twa.check_and_alert, 'TO_EMAIL', {'cooling_type': 'PASSIVE_COOLING'}, float('nan'))
        self.assertRaises(Invalid_Input, twa.check_and_alert, 'TO_MAIL', {'cooling_type': 'PASSIVE_COOLING'}, 30)
        self.assertRaises(Invalid_Input, twa.check_and_alert, 'TO_MAIL', {'cooling_type': 'LOW_ACTIVE_COOLING'}, 30)
        self.assertRaises(Invalid_Input, twa.check_and_alert, 'TO_MAIL', {'cooling_type': 'PASSIVE_COOLING'}, None)
        self.assertRaises(Invalid_Input, twa.check_and_alert, 'TO_MAIL', {'cooling_type': 'LOW_ACTIVE_COOLING'}, None)                   
        self.assertRaises(Invalid_Input, twa.check_and_alert, 'TO_CONSOLE', {'cooling_type': 'PASSIVE_COOLING'}, float('nan'))                   
        self.assertRaises(Invalid_Input, twa.check_and_alert, 'TO_CONSOLE', {'cooling_type': None}, 70)
        self.assertRaises(Invalid_Input, twa.check_and_alert, None, None, None)
        
if __name__ == '__main__':
  unittest.main()