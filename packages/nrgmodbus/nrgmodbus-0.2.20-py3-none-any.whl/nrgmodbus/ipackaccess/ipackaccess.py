#!/bin/usr/python
from .registers import ipackaccess_registers
from nrgmodbus.utilities import combine_registers, combine_u32_registers

class ipackaccess(object):
    """
    class for handling modbus connections to iPackACCESS

    parameters
    ----------
        ip : string
            ip address or domain name of iPack
        port : int
            port for modbus access (default 502)
        unit : int
            slave number on bus (default 1)   
        logger_model : int
            finished good number of connected Symphonie (default 8206)
    """
    def __init__(self, ip='', port=502, logger_model=8206, unit=1, connect=True):
        self.ip = ip
        self.logger_model = logger_model
        self.port = port
        self.unit = unit
        self.init_registers()
        self.e = ''
        if connect == True:
            self.connect()


    def init_registers(self):
        """
        set registers for all available data manually
        each is a list
         0 = register address
         1 = number of registers
        """
        self.hr = ipackaccess_registers()
        

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


    def poll(self, interval=4, reconnect=True, 
             stat=True, rt=True, serial=False,
             diag=False, config=False,
             db='', save_to_db=False,
             echo=False):
        """
        regularly poll registers

        parameters : (default value)
              interval : seconds to wait between polls (4)
             reconnect : automatically reconnect on failure (True)
                  stat : poll statistical registers (True)
                    rt : poll real time registers (True)
                serial : poll serial registers (False)
                  diag : poll diagnostic registers (False)
                config : poll config registers (False)
                    db : sqlite3 db to save to ('')
            save_to_db : save to db? (False)
                  echo : print some data to console (False)

        returns register values as individual and packages arrays
        """
        from time import time, sleep
        i=0
        # set up database connection if save_to_db == True
        while True:
            poll_time = time()
            i += 1
            if self.e != '':
                if reconnect == True:
                    self.connect()
                else:
                    return "Disconnected from {0}, reconnect disabled".format(self.ip)
                self.e = ''

            if stat == True:
                self.return_stat_readings()
            if rt == True:
                self.return_rt_data_readings()
            if serial == True:
                self.return_rt_serial_readings()
            if diag == True:
                self.return_diag_readings()
            if config == True:
                self.return_config()

            if save_to_db == True:
                # do the db things
                pass

            if echo == True:
                if rt == True:
                    print("{0}\t{1}\t{2}\t{3}".format(i,self.date_time,self.rt_ch1,self.rt_ch13))
                else:
                    print("Poll # {0}".format(i))

            while time() < poll_time + interval:
                sleep(0.01)


    def return_diag_readings(self):
        """ data from diagnostic registers
        
        returns
        -------
        dict
            see ipackaccess.registers for more info
        
        """
        for i in self.hr.diag:
            try:
                self.hr.diag[i]['value'] = self.read_single_register(self.hr.diag[i]['reg'])
            except KeyError:
                pass

        self.hr.diag['datetime'] = {'value': f"{str(self.hr.diag['year']['value'])}-{str(self.hr.diag['month']['value']).zfill(2)}-{str(self.hr.diag['day']['value']).zfill(2)} {str(self.hr.diag['hour']['value']).zfill(2)}:{str(self.hr.diag['minute']['value']).zfill(2)}:{str(self.hr.diag['second']['value']).zfill(2)}"}


    def return_system_readings(self):
        """ logger and ipack system information

        returns
        -------
        dict
            see ipackaccess.registers for more info
        
        """
        start_reg = 0
        length = 21

        self.read_result = self.read_single_register([start_reg, length], singles=True)

        self.hr.logger['signed_num_ex']['value'] = combine_u32_registers(self.read_result[0:2])
        self.hr.logger['unsigned_num_ex']['value'] = combine_u32_registers(self.read_result[2:4])
        self.hr.logger['unsigned_16_num_ex']['value'] = self.read_result[4]
        self.hr.logger['site_number']['value'] = combine_u32_registers(self.read_result[5:7])
        self.hr.logger['sn']['value'] = combine_u32_registers(self.read_result[7:9])
        self.hr.logger['model']['value'] = self.read_result[9]
        self.hr.logger['hw_ver']['value'] = combine_u32_registers(self.read_result[10:12])
        self.hr.logger['fw_ver']['value'] = combine_u32_registers(self.read_result[12:14])
        self.hr.ipack['sn']['value'] = combine_u32_registers(self.read_result[14:16])
        self.hr.ipack['model']['value'] = self.read_result[16]
        self.hr.ipack['hw_ver']['value'] = combine_u32_registers(self.read_result[17:19])
        self.hr.ipack['fw_ver']['value'] = combine_u32_registers(self.read_result[19:21])


    def return_all_channel_data(self):
        """
        poll statistical registers
        """
        for ch in self.hr.data_ch:
            for i in self.hr.data_ch[ch]:
                self.hr.data_ch[ch][i]['value'] = self.read_single_register(self.hr.data_ch[ch][i]['reg'])


    def return_channel_data(self, channel):
        """
        poll statistical registers

        parameters
        ----------
            channel : int
                channel number to poll

        returns
        -------
        dict
            populates value of channel dict

        example
        -------
        >>> poller.return_channel_data(1)
        >>> poller.data_ch[1]

        """
        for i in self.hr.data_ch[channel]:
            self.hr.data_ch[channel][i]['value'] = self.read_single_register(self.hr.data_ch[channel][i]['reg'])


    def return_time(self):
        """
        returns time from config registers
        """
        self.read_result = self.read_single_register([1500, 6], singles=True)

        self.hr.samp_time['year']['value'] = self.read_result[0]
        self.hr.samp_time['month']['value'] = self.read_result[1]
        self.hr.samp_time['day']['value'] = self.read_result[2]
        self.hr.samp_time['hour']['value'] = self.read_result[3]
        self.hr.samp_time['minute']['value'] = self.read_result[4]
        self.hr.samp_time['second']['value'] = self.read_result[5]
        self.hr.samp_time['datetime'] = {'value': f"{str(self.hr.samp_time['year']['value'])}-{str(self.hr.samp_time['month']['value']).zfill(2)}-{str(self.hr.samp_time['day']['value']).zfill(2)} {str(self.hr.samp_time['hour']['value']).zfill(2)}:{str(self.hr.samp_time['minute']['value']).zfill(2)}:{str(self.hr.samp_time['second']['value']).zfill(2)}"}


    def return_rt_data_readings(self):
        """ refresh all 'samp' data values """
        self.return_time()

        start_reg = 1506
        length = 100

        self.read_result = self.read_single_register([start_reg, length], singles=True)
        ch = 1
        for i in range(0, len(self.read_result), 2):
            self.hr.data_ch[ch]['samp']['value'] = combine_registers(self.read_result[i:i+2])
            ch += 1
            
        start_reg = 3500
        length = 20

        self.read_result = self.read_single_register([start_reg, length], singles=True)
        ch = 100
        for i in range(0, len(self.read_result), 2):
            self.hr.data_ch[ch]['samp']['value'] = combine_registers(self.read_result[i:i+2])
            ch += 1


    def read_registers(self, list_of_registers_to_read):
        """
        returns array of converted values
        """
        return_values = []
        for reg in list_of_registers_to_read:
            try:
                return_values.append(self.read_single_register(reg))
            except:
                return_values.append(9999)
        return return_values


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


    def monitor(self):
        """

        """
        pass


