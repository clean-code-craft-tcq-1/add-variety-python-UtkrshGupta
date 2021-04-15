import unittest
from unittest.mock import Mock
from unittest import mock
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

# Tests using mocking
    
    #using Mock object creation
    
    def test_mocking_typewiseAlert_using_mock_object(self):
        TypewiseAlert = Mock()            
        TypewiseAlert.send_to_controller('TO_LOW')
        self.assertRaises(AssertionError, TypewiseAlert.send_to_controller.assert_called_with, 'TO_HIGH')
        TypewiseAlert.check_and_alert('TO_CONTROLLER', {'cooling_type': 'PASSIVE_COOLING'}, 70)
        self.assertIsNone(TypewiseAlert.check_and_alert.assert_called())
        self.assertIsNone(TypewiseAlert.check_and_alert.assert_called_once())
        TypewiseAlert.check_and_alert('TO_EMAIL', {'cooling_type': 'PASSIVE_COOLING'}, 70)
        self.assertRaises(AssertionError, TypewiseAlert.check_and_alert.assert_called_once)
        self.assertRaisesRegex(AssertionError, \
                                """Expected 'check_and_alert' to have been called once. Called 2 times""", \
                                TypewiseAlert.check_and_alert.assert_called_once)
        
        
        TypewiseAlert.classify_temperature_breach('PASSIVE_COOLING', 20)
        self.assertRaisesRegex(AssertionError, \
                               'expected call not found.', \
                               TypewiseAlert.classify_temperature_breach.assert_called_with,\
                              'PASSIVE_COOL', 20)
        
    #using patch
    
    @mock.patch('typewise_alert.TypewiseAlert.send_to_controller')
    def test_mocking_for_send_to_controller_failure(self, mock_send_to_controller):
        actual_result = mock_send_to_controller.send_to_controller('TO_LOW')
        mock_send_to_controller.retrun_value = 'CONTROLLER_INVOKE'
        self.assertNotEqual(actual_result, mock_send_to_controller)
        self.assertRaises(AssertionError,mock_send_to_controller.send_to_controller.assert_called_with, 'TO_HIGH')
        
    @mock.patch('typewise_alert.TypewiseAlert..send_to_email')
    def mock_mocking_test_for_send_to_email_failure(self, mock_send_to_email):
        actual_result = mock_send_to_email.send_to_email('TO_LOW')
        mock_send_to_email.retrun_value = 'EMAIL_SENT'
        self.assertNotEqual(actual_result, mock_send_to_email)
        self.assertRaises(AssertionError, mock_send_to_email.send_to_email.assert_called_with, 'TO_HIGH')
        self.assertIsNone(mock_send_to_email.send_to_email.assert_called_once())

    @mock.patch('typewise_alert.TypewiseAlert.send_to_console')
    def test_mocking_for_send_to_console_failure(self, mock_send_to_console):
        actual_result = mock_send_to_console.send_to_console('TO_LOW')
        mock_send_to_console.retrun_value = 'CONSOLE_LOGGED'
        self.assertNotEqual(actual_result, mock_send_to_console)
        
if __name__ == '__main__':
  unittest.main()