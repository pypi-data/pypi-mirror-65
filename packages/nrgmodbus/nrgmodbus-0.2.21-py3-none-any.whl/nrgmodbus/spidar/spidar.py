#!/bin/usr/python
from .registers import spidar_registers
from nrgmodbus.utilities import convert_hex_to_float

class spidar_v1(object):
    """ 
    class for handling modbus connections to Spidar V1 systems

    parameters
    ----------
        ip : string
            ip address or domain name of spidar
        port : int
            port for modbus access (default 502)
        unit : int
            slave number on bus (default 1) 
    """
    def __init__(self, ip='', port=502, unit=1, connect=False):
        self.ip = ip
        self.port = port
        self.unit = unit
        self.init_registers()
        self.e = ''
        if connect == True:
            self.connect()


    def init_registers(self):
        self.hr = spidar_registers()


    def connect(self):
        """
        initialize self.ip, self.port, self.unit
        """
        from pymodbus.client.sync import ModbusTcpClient as ModbusClient

        self.client = ModbusClient(host=self.ip,port=self.port,unit=self.unit)
        print("Connecting to {0}... \t\t".format(self.ip), end="", flush=True)
        try:
            self.client.connect()
            if self.client.is_socket_open() == True:
                print("[OK]")
            else:
                self.client.connect()
                if self.client.is_socket_open != True:
                    raise ValueError('Could Not Connect to {0}'.format(self.ip))
        except Exception as e:
            self.e = e
            print("[FAILED]")
            print(self.e)


    def disconnect(self):
        print("Disconnecting from {0}... \t\t".format(self.ip), end="", flush=True)
        try:
            self.client.close()
            print("[OK]")
        except Exception as e:
            print("[ERROR]")
            print(e)


    def return_rt_data_readings(self):
        """ refresh all registers """
        start_reg = 0
        length = 105

        self.read_result = self.read_single_register([start_reg, length], singles=True)

        self.hr.met_data['pressure']['value'] = self.read_result[1] * self.hr.met_data['pressure']['scaling']

        self.hr.met_data['temperature']['value'] = self.read_result[2] * self.hr.met_data['temperature']['scaling']
        if self.hr.met_data['temperature']['scaling'] > 100: self.hr.met_data['temperature']['value'] -= 656
        
        self.hr.met_data['humidity']['value'] = self.read_result[3] * self.hr.met_data['humidity']['scaling']
        self.hr.met_data['precipitation']['value'] = self.read_result[4] * self.hr.met_data['precipitation']['scaling']

        n = 5

        for gate in range(1, 10 + 1):
            self.hr.wind_data_gate[gate]['height']['value'] = self.read_result[n]
            self.hr.wind_data_gate[gate]['speed']['min']['value'] = self.read_result[n+1] * self.hr.wind_data_gate[gate]['speed']['min']['scaling']
            self.hr.wind_data_gate[gate]['speed']['max']['value'] = self.read_result[n+2] * self.hr.wind_data_gate[gate]['speed']['max']['scaling']
            self.hr.wind_data_gate[gate]['speed']['avg']['value'] = self.read_result[n+3] * self.hr.wind_data_gate[gate]['speed']['avg']['scaling']
            self.hr.wind_data_gate[gate]['speed']['sd']['value'] = self.read_result[n+4] * self.hr.wind_data_gate[gate]['speed']['sd']['scaling']
            self.hr.wind_data_gate[gate]['dir']['min']['value'] = self.read_result[n+5] * self.hr.wind_data_gate[gate]['dir']['min']['scaling']
            self.hr.wind_data_gate[gate]['dir']['max']['value'] = self.read_result[n+6] * self.hr.wind_data_gate[gate]['dir']['max']['scaling']
            self.hr.wind_data_gate[gate]['dir']['avg']['value'] = self.read_result[n+7] * self.hr.wind_data_gate[gate]['dir']['avg']['scaling']
            self.hr.wind_data_gate[gate]['dir']['sd']['value'] = self.read_result[n+8] * self.hr.wind_data_gate[gate]['dir']['sd']['scaling']
            self.hr.wind_data_gate[gate]['quality']['value'] = self.read_result[n+9]

            n += 10


    def read_single_register(self, register, singles=False):
        """
        wrapper for pymodbus, returns single value
        """       
        import struct
        import traceback

        try:
            rr = self.client.read_holding_registers(register[0], register[1], unit=1)
            self.rr = rr

            if register[1] == 2 and singles == False:
                flo = combine_registers(rr.registers)

            elif register[1] > 2 and singles == False:
                flo = []
                for i in range(0, len(rr.registers), 2):
                    temp = combine_registers([rr.registers[i], rr.registers[i+1]])
                    flo.append(temp)

            elif register[1] > 2 and singles == True:
                flo = rr.registers

            else:
                flo = rr.registers[0]

            return flo

        except Exception as e:
            self.e = e
            self.rr=rr
            return 9999

