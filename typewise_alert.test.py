import unittest
from typewise_alert import TypewiseAlert
        
class TypewiseTest(unittest.TestCase):
    def test_infers_breach_as_per_limits(self):
        twa = TypewiseAlert()
        self.assertTrue(twa.infer_breach(20, 50, 100) == 'TOO_LOW')
        self.assertTrue(twa.infer_breach(200, 50, 100) == 'TOO_HIGH')
        self.assertTrue(twa.infer_breach(70, 50, 100) == 'NORMAL')

    def test_to_check_and_alert_temperature_status(self):
        twa = TypewiseAlert()
        self.assertTrue(twa.check_and_alert('TO_CONTROLLER', {'cooling_type': 'PASSIVE_COOLING'}, 70)=='CONTROLLER_INVOKED')
        self.assertTrue(twa.check_and_alert('TO_EMAIL', {'cooling_type': 'MED_ACTIVE_COOLING'}, 70)=='EMAIL_SENT')
        self.assertTrue(twa.check_and_alert('TO_CONSOLE', {'cooling_type': 'MED_ACTIVE_COOLING'}, 70)=='LOGGED_ON_CONSOLE')
        self.assertTrue(twa.check_and_alert('TO_EMAIL', {'cooling_type': 'PASSIVE_COOLING'}, float('nan')) == 'INVALID_INPUT')
        self.assertTrue(twa.check_and_alert('TO_MAIL', {'cooling_type': 'PASSIVE_COOLING'}, 30) == 'INVALID_INPUT')
        self.assertTrue(twa.check_and_alert('TO_MAIL', {'cooling_type': 'LOW_ACTIVE_COOLING'}, 30) == 'INVALID_INPUT')
        self.assertTrue(twa.check_and_alert('TO_MAIL', {'cooling_type': 'PASSIVE_COOLING'}, None) == 'INVALID_INPUT')
        self.assertTrue(twa.check_and_alert('TO_MAIL', {'cooling_type': 'LOW_ACTIVE_COOLING'}, None) == 'INVALID_INPUT')                   
        
if __name__ == '__main__':
  unittest.main()