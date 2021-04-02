class TypewiseAlert:
    def __init__(self):
        self.__cooling_types = { 
                'PASSIVE_COOLING': {'lowerLimit': 0, 'upperLimit': 35},
                'HI_ACTIVE_COOLING': {'lowerLimit': 0, 'upperLimit': 45},
                'MED_ACTIVE_COOLING': {'lowerLimit': 0, 'upperLimit': 40}   
            }
        
        self.__alert_message_targets = { 
                'TO_CONTROLLER': self.send_to_controller,
                'TO_EMAIL': self.send_to_email
            }
        
        self.__breach_type_email_message = {
                'TOO_LOW': {
                    'recepient': "a.b@c.com",
                    'message': 'Hi, the temperature is {}'
                    },
                
                'TOO_HIGH': {
                    'recepient': "a.b@c.com",
                    'message': 'Hi, the temperature is {}'
                    }
            }
        
        self.__local_controller_header = 0xfeed
        
    def get_cooling_type_limits(self, cooling_type):
        if cooling_type is not None:
            return self.__cooling_types[cooling_type].values()

    def infer_breach(self, value, lowerLimit, upperLimit):
        if value < lowerLimit:
            return 'TOO_LOW'
        if value > upperLimit:
            return 'TOO_HIGH'
        return 'NORMAL'
        
    def classify_temperature_breach(self, cooling_type, temperature_in_C):
        lower_limit, upper_limit = self.get_cooling_type_limits(cooling_type)
        return self.infer_breach(temperature_in_C, lower_limit, upper_limit)

    def check_and_alert(self, alert_target, battery_char, temperature_in_C):
        breach_type =\
        self.classify_temperature_breach(battery_char['cooling_type'], temperature_in_C)
        if breach_type is not None:
            self.__alert_message_targets[alert_target](breach_type)
            return 'SENT'
        
    def send_to_controller(self, breach_type):
        print(f'{self.__local_controller_header}, {breach_type}')

    def send_to_email(self, breach_type):
        print(f"To: {self.__breach_type_email_message[breach_type]['recepient']}")
        print(self.__breach_type_email_message[breach_type]['message'].format(breach_type.replace("_"," ").lower()))
        

