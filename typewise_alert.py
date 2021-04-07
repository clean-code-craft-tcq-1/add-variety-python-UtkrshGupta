from math import isnan

class TypewiseAlert:
    def __init__(self):
        self.__cooling_types = { 
                'PASSIVE_COOLING': {'lowerLimit': 0, 'upperLimit': 35},
                'HI_ACTIVE_COOLING': {'lowerLimit': 0, 'upperLimit': 45},
                'MED_ACTIVE_COOLING': {'lowerLimit': 0, 'upperLimit': 40}   
            }
        
        self.__alert_message_targets = { 
                'TO_CONTROLLER': self.send_to_controller,
                'TO_EMAIL': self.send_to_email,
                'TO_CONSOLE': self.send_to_console
            }
        
        self.__breach_type_email_message = {
                'NORMAL': {
                    'sender': "sender@org.com",
                    'recepient': "a.b@c.com",
                    'message': 'Hi, the temperature is in {} state'
                    },
                
                'TOO_LOW': {
                    'sender': "sender@org.com",
                    'recepient': "a.b@c.com",
                    'message': 'Hi, the temperature is {}'
                    },
                
                'TOO_HIGH': {
                    'sender': "sender@org.com",
                    'recepient': "a.b@c.com",
                    'message': 'Hi, the temperature is {}'
                    }
            }
        
        self.__local_controller_header = 0xfeed
     
    def get_cooling_type_limits(self, cooling_type):
        return self.__cooling_types[cooling_type].values()

    def infer_breach(self, value, lowerLimit, upperLimit):
        if value < lowerLimit:
            return 'TOO_LOW'
        if value > upperLimit:
            return 'TOO_HIGH'
        return 'NORMAL'
    
    def classify_temperature_breach(self, cooling_type, temperature_in_C):
        if self.__is_cooling_type_and_temperature_valid(cooling_type, temperature_in_C):
            lower_limit, upper_limit = self.get_cooling_type_limits(cooling_type)
            return self.infer_breach(temperature_in_C, lower_limit, upper_limit)
        else:
            return 'INVALID_INPUT'
        
    def check_and_alert(self, alert_target, battery_char, temperature_in_C):
        breach_type =\
            self.classify_temperature_breach(battery_char['cooling_type'], temperature_in_C)
        
        if self.__check_if_alert_target_and_breach_type_are_valid(alert_target, breach_type):
            return self.__alert_message_targets[alert_target](breach_type)
        else:
            return 'INVALID_INPUT'
        
    def send_to_controller(self, breach_type):
        print(f'CONTROLLER MESSAGE: {self.__local_controller_header}, {breach_type}')
        return "CONTROLLER_INVOKED"

    def send_to_email(self, breach_type):
        print(f"From: {self.__breach_type_email_message[breach_type]['sender']}")
        print(f"To: {self.__breach_type_email_message[breach_type]['recepient']}")
        print(self.__breach_type_email_message[breach_type]['message'].format(breach_type.replace("_"," ")))
        return 'EMAIL_SENT'
    
    def send_to_console(self, breach_type):
        print(f'CONSOLE MESSAGE: Temperatue is {breach_type.replace("_"," ")}')
        return 'LOGGED_ON_CONSOLE'
    
    def __is_input_temperature_valid(self, temperature_in_C):
        if temperature_in_C != None and not isnan(temperature_in_C):
            return True
        return False
    
    def __is_cooling_type_and_temperature_valid(self, cooling_type, temperature_in_C):
        if self.__is_input_temperature_valid(temperature_in_C) and cooling_type in self.__cooling_types.keys():
            return True
        return False
     
    def __check_if_alert_target_and_breach_type_are_valid(self, alert_target, breach_type):
        if alert_target in self.__alert_message_targets.keys() and \
            breach_type != 'INVALID_INPUT':
                return True
        return False   