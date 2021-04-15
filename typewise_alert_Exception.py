class Invalid_Input(Exception):
    def __init__(self, message='Invalid Input Arguments'):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f'{self.message}'