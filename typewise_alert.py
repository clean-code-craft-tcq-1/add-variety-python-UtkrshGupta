from math import isnan
from typewise_alert_Exception import Invalid_Input
class TypewiseAlert:
#  Constructor
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
        
        self.__breach_type_email_data = {
                'NORMAL': {
                    'Sender': "sender@org.com",
                    'Recepient': "a.b@c.com",
                    'Subject': "Automatic Breach Alert Notification",
                    'Message': 'Hi, the temperature is in Normal state'
                    },
                
                'TOO_LOW': {
                    'Sender': "sender@org.com",
                    'recepient': "a.b@c.com",
                    'Subject': "Automatic Breach Alert Notification",
                    'Message': 'Hi, the temperature is Too Low'
                    },
                
                'TOO_HIGH': {
                    'Sender': "sender@org.com",
                    'Recepient': "a.b@c.com",
                    'Subject': "Automatic Breach Alert Notification",
                    'Message': 'Hi, the temperature is Too Low'
                    }
            }
        
        self.__target_sent_to_status = {
                'TO_CONTROLLER': False,
                'TO_EMAIL': False,
                'TO_CONSOLE': False
            }
        self.__controller_active_status = 'ON'
        self.__email_tcp_status = 'ON'
        self.__console_active_status = 'ON'
        self.__local_controller_header = 0xfeed
     
# Public Methods    
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
    
    def get_breach_type(self, battery_char, temperature_in_C):
        if battery_char is not None:
            return self.classify_temperature_breach(battery_char['cooling_type'], temperature_in_C)
        return "INVALID_INPUT"
        
    
    def check_and_alert(self, alert_target, battery_char, temperature_in_C):

        breach_type = \
            self.get_breach_type(battery_char, temperature_in_C)
            
        if self.__check_if_alert_target_and_breach_type_are_valid(alert_target, breach_type):
            return self.__alert_message_targets[alert_target](breach_type)
        else:
            raise Invalid_Input('Invalid Input Arguments')
            return

# Controller Alert Methods            
    def send_to_controller(self, breach_type):
        self.__target_sent_to_status['TO_CONTROLLER'] = False
        status = None
        if self.get_controller_status() == 'ON':
            status = self.call_controller(breach_type)
        
        if status == 'OK':
            self.__target_sent_to_status['TO_CONTROLLER'] = True 
        
        return self.__target_sent_to_status['TO_CONTROLLER']
        
    def call_controller(self, breach_type):
        if breach_type in self.__breach_type_email_data.keys():
            print(f'CONTROLLER MESSAGE: {self.__local_controller_header}, {breach_type}')
            return 'OK'
        
    
    def get_controller_status(self):
        return self.__controller_active_status

    def set_controller_status(self, status):
        self.__controller_active_status = status
        return self.__controller_active_status

# Email Alert Methods  
    def send_to_email(self, breach_type):
        self.__target_sent_to_status['TO_EMAIL'] = False
        status = None
        if self.get_email_tcp_status() == 'ON':        
            email_data = self.get_email_data(breach_type) 
            status = self.generate_email(email_data)
        
        if status == 'OK':
            self.__target_sent_to_status['TO_EMAIL'] = True   
        
        return self.__target_sent_to_status['TO_EMAIL']
    
    def get_email_data(self, breach_type):
        if breach_type in self.__breach_type_email_data.keys():
            return self.__breach_type_email_data[breach_type]
        
    def generate_email(self, email_data):
        #Dummy data printing    
        if email_data is not None:
            print(f"From: {email_data['Sender']}")
            print(f"To: {email_data['Recepient']}")
            print(f"Subject: {email_data['Subject']}")
            print(f"Body: {email_data['Message']}")
            return 'OK'

    def get_email_tcp_status(self):
        return self.__email_tcp_status
    

    def set_email_tcp_status(self, status):
        self.__email_tcp_status = status
        return self.__email_tcp_status

# Console Alert Methods    
    def send_to_console(self, breach_type):
        self.__target_sent_to_status['TO_CONSOLE'] = False
        status = None
        if self.get_console_status() == 'ON':          
            status = self.call_console_logger(breach_type)
        
        if status == 'OK':
            self.__target_sent_to_status['TO_CONSOLE'] = True 
        
        return self.__target_sent_to_status['TO_CONSOLE']
    

    def call_console_logger(self, breach_type):
        print(f'CONSOLE MESSAGE: Temperatue is {breach_type.replace("_"," ")}')
        return 'OK'
    

    def get_console_status(self):
        return self.__console_active_status
    
    
    def set_console_status(self, status):
        self.__console_active_status = status
        return self.__console_active_status    
    

# Private Methods    
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
        