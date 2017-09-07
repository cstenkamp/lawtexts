class ValuedProperty():
    def __init__(self):
        self.value = None

    def setValue(self, value):
        if not value == '':
            self.value = value
        else:
            print('empty value field')

class Voltage(ValuedProperty):
    def __init__(self):
        super(Voltage,self).__init__()

class Wattage(ValuedProperty):
    def __init__(self):
        super(Wattage,self).__init__()

class Temperature(ValuedProperty):
    def __init__(self):
        super(Temperature,self).__init__()

class Pressure(ValuedProperty):
    def __init__(self):
        super(Pressure,self).__init__()

class Volume(ValuedProperty):
    def __init__(self):
        super(Volume,self).__init__()

class Content(ValuedProperty):
    def __init__(self):
        super(Content,self).__init__()