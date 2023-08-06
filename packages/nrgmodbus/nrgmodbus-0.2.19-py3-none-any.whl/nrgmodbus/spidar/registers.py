
class spidar_registers(object):
    """registers for spidar data
    
    returns
    -------
    dict
    all register identifiers are dicts:
        0 : register number
        1 : register length
        2 : multiplier for rescaling
    
     """
    def __init__(self):
        self.generate_met_dict()
        self.generate_range_gate_dict()

    def generate_met_dict(self):
        """ tph data """
        n = 0 # register offset value

        self.met_data = {}
        self.met_data['pressure'] = {'reg':[n+2, 1], 'type':'UINT16', 'range': '0 to 1000.0', 'units': 'mmHg', 'scaling': 0.1}
        self.met_data['temperature'] = {'reg':[n+3, 1], 'type':'INT16', 'range': '-100.0 to 100.0', 'units': 'C', 'scaling': 0.01}
        self.met_data['humidity'] = {'reg':[n+4, 1], 'type':'UINT16', 'range': '0 to 100.00', 'units': '%', 'scaling': 0.01}
        self.met_data['precipitation'] = {'reg':[n+5, 1], 'type':'UINT16', 'range': '0 to 100', 'units': 'n/a', 'scaling': 1}

    def generate_range_gate_dict(self):
        """ remote sensing data """
        n = 0

        self.wind_data_gate = {}

        for i in range(1, 11):
            self.wind_data_gate[i] = {
                'height': {'reg': [n+5, 1], 'type':'UINT16', 'range': '0 to 1000', 'units': 'm', 'scaling': 1},
                'speed': { 
                    'min': {'reg': [n+6, 1], 'type':'UINT16', 'range': '0 to 40.0', 'units': 'm/s', 'scaling': 0.01},
                    'max': {'reg': [n+7, 1], 'type':'UINT16', 'range': '0 to 40.0', 'units': 'm/s', 'scaling': 0.01},
                    'avg': {'reg': [n+8, 1], 'type':'UINT16', 'range': '0 to 40.0', 'units': 'm/s', 'scaling': 0.01},
                    'sd': {'reg': [n+9, 1], 'type':'UINT16', 'range': '0 to 40.0', 'units': 'm/s', 'scaling': 0.01},
                    },
                'dir': { 
                    'min': {'reg': [n+10, 1], 'type':'UINT16', 'range': '0.0 to 359.9', 'units': 'deg', 'scaling': 0.01},
                    'max': {'reg': [n+11, 1], 'type':'UINT16', 'range': '0.0 to 359.9', 'units': 'deg', 'scaling': 0.01},
                    'avg': {'reg': [n+12, 1], 'type':'UINT16', 'range': '0.0 to 359.9', 'units': 'deg', 'scaling': 0.01},
                    'sd': {'reg': [n+13, 1], 'type':'UINT16', 'range': '0.0 to 359.9', 'units': 'deg', 'scaling': 0.01},
                    },
                'quality': {'reg': [n+14, 1], 'type':'UINT16', 'range': '0 to 100', 'units': 'n/a', 'scaling': 1}
                }
            n += 10