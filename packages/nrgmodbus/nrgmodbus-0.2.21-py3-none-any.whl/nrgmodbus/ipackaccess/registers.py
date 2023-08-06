gust_channels = list(range(1,13))
no_gust_channels = list(range(13,51))
calc_channels = list(range(100, 110))


class ipackaccess_registers(object):
    """ """
    def __init__(self):
        self.generate_system_dict()
        self.generate_datetime_dict()
        self.generate_channel_dict()
        self.generate_diag_dict()


    def generate_system_dict(self):
        """generate dict of logger and ipack data"""
        self.logger = {}
        self.ipack = {}
        self.logger['signed_num_ex'] = {'reg': [0, 2]}
        self.logger['unsigned_num_ex'] = {'reg': [2, 2]}
        self.logger['unsigned_16_num_ex'] = {'reg': [4, 1]}
        self.logger['site_number'] = {'reg': [5, 2]}
        self.logger['sn'] = {'reg': [7, 2]}
        self.logger['model'] = {'reg': [9, 1]}
        self.logger['hw_ver'] = {'reg': [10, 2]}
        self.logger['fw_ver'] = {'reg': [12, 2]}
        self.ipack['sn'] = {'reg': [14, 2]}
        self.ipack['model'] = {'reg': [16, 1]}
        self.ipack['hw_ver'] = {'reg': [17, 2]}
        self.ipack['fw_ver'] = {'reg': [19, 2]}


    def generate_datetime_dict(self):
        """generate dicts of date/time data"""
        self.samp_time = {}
        self.samp_time['year'] = {'reg': [1500, 1]}
        self.samp_time['month'] = {'reg': [1501, 1]}
        self.samp_time['day'] = {'reg': [1502, 1]}
        self.samp_time['hour'] = {'reg': [1503, 1]}
        self.samp_time['minute'] = {'reg': [1504, 1]}
        self.samp_time['second'] = {'reg': [1505, 1]}

        self.sta_time = {}
        self.sta_time['year'] = {'reg': [2500, 1]}
        self.sta_time['month'] = {'reg': [2501, 1]}
        self.sta_time['day'] = {'reg': [2502, 1]}
        self.sta_time['hour'] = {'reg': [2503, 1]}
        self.sta_time['minute'] = {'reg': [2504, 1]}
        self.sta_time['second'] = {'reg': [2505, 1]}

    def generate_channel_dict(self):
        """generate dictionary of all registers

        returns
        -------
        dict
            for counter channels: avg, sd, max, min, gust, samp
            for analog, serial and calc channels: avg, sd, max, min, samp

        example
        -------
        >>> self.data_ch[1]['avg']['value']

        """
        self.data_ch = {}
        n = 2506 # statistic start register
        m = 1506 # sample/realtime start register
        b = 2
        for i in gust_channels:
            self.data_ch[i] = {'avg': {'reg': [n, 2]}, 'sd': {'reg': [n + b, 2]}, 'max': {'reg': [n + 2*b, 2]}, 'min': {'reg': [n + 3*b, 2]}, 'gust': {'reg': [n + 4*b, 2]}, 'samp': {'reg': [m, 2]} }
            n += 5*b
            m += 2

        for i in no_gust_channels:
            self.data_ch[i] = {'avg': {'reg': [n, 2]}, 'sd': {'reg': [n + b, 2]}, 'max': {'reg': [n + 2*b, 2]}, 'min': {'reg': [n + 3*b, 2]}, 'samp': {'reg': [m, 2]} }
            n += 4*b
            m +=2

        n = 4000 # statistic start register
        m = 3500 # sample/realtime start register
        for i in calc_channels:
            self.data_ch[i] = {'avg': {'reg': [n, 2]}, 'sd': {'reg': [n + b, 2]}, 'max': {'reg': [n + 2*b, 2]}, 'min': {'reg': [n + 3*b, 2]}, 'samp': {'reg': [m, 2]} }
            n += 4*b
            m += 2


    def generate_diag_dict(self):
        """generate dict of diagnostic data"""
        self.diag = {}
        self.diag['year'] = {'reg': [3000, 1]}
        self.diag['month'] = {'reg': [3001, 1]}
        self.diag['day'] = {'reg': [3002, 1]}
        self.diag['hour'] = {'reg': [3003, 1]}
        self.diag['minute'] = {'reg': [3004, 1]}
        self.diag['second'] = {'reg': [3005, 1]}
        self.diag['temp'] = {'reg': [3006, 2]}
        self.diag['12v_bat'] = {'reg': [3008, 2]}
        self.diag['12v_cur'] = {'reg': [3010, 2]}
        self.diag['2v_bat'] = {'reg': [3012, 2]}
        self.diag['5v_cur'] = {'reg': [3014, 2]}
        self.diag['sd_inst'] = {'reg': [3016, 1]}
        self.diag['sd_free'] = {'reg': [3017, 2]}
        self.diag['sd_used'] = {'reg': [3019, 2]}
