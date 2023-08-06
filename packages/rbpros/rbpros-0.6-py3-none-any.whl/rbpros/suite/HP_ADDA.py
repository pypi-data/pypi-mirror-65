import time
from ..device import Board
from ..pin import ANAPin, IOFlow, IOType, MISOPin, MOSIPin, SCLKPin, SPI
from .RBP_34 import RBP_GPIO

GAIN = {'ADS1256_GAIN_1': 0,  # GAIN   1
        'ADS1256_GAIN_2': 1,  # GAIN   2
        'ADS1256_GAIN_4': 2,  # GAIN   4
        'ADS1256_GAIN_8': 3,  # GAIN   8
        'ADS1256_GAIN_16': 4,  # GAIN  16
        'ADS1256_GAIN_32': 5,  # GAIN  32
        'ADS1256_GAIN_64': 6,  # GAIN  64
        }

DRATE = {'ADS1256_30000SPS': 0xF0,  # reset the default values
         'ADS1256_15000SPS': 0xE0,
         'ADS1256_7500SPS': 0xD0,
         'ADS1256_3750SPS': 0xC0,
         'ADS1256_2000SPS': 0xB0,
         'ADS1256_1000SPS': 0xA1,
         'ADS1256_500SPS': 0x92,
         'ADS1256_100SPS': 0x82,
         'ADS1256_60SPS': 0x72,
         'ADS1256_50SPS': 0x63,
         'ADS1256_30SPS': 0x53,
         'ADS1256_25SPS': 0x43,
         'ADS1256_15SPS': 0x33,
         'ADS1256_10SPS': 0x20,
         'ADS1256_5SPS': 0x13,
         'ADS1256_2d5SPS': 0x03
         }

REG = {'REG_STATUS': 0,  # x1H
       'REG_MUX': 1,     # 01H
       'REG_ADCON': 2,   # 20H
       'REG_DRATE': 3,   # F0H
       'REG_IO': 4,      # E0H
       'REG_OFC0': 5,    # xxH
       'REG_OFC1': 6,    # xxH
       'REG_OFC2': 7,    # xxH
       'REG_FSC0': 8,    # xxH
       'REG_FSC1': 9,    # xxH
       'REG_FSC2': 10,   # xxH
       }

CMD = {'CMD_WAKEUP': 0x00,     # Completes SYNC and Exits Standby Mode 0000  0000 (00h)
       'CMD_RDATA': 0x01,      # Read Data 0000  0001 (01h)
       'CMD_RDATAC': 0x03,     # Read Data Continuously 0000   0011 (03h)
       # Stop Read Data Continuously 0000   1111 (0Fh)
       'CMD_SDATAC': 0x0F,
       'CMD_RREG': 0x10,       # Read from REG rrr 0001 rrrr (1xh)
       'CMD_WREG': 0x50,       # Write to REG rrr 0101 rrrr (5xh)
       # Offset and Gain Self-Calibration 1111    0000 (F0h)
       'CMD_SELFCAL': 0xF0,
       'CMD_SELFOCAL': 0xF1,   # Offset Self-Calibration 1111    0001 (F1h)
       'CMD_SELFGCAL': 0xF2,   # Gain Self-Calibration 1111    0010 (F2h)
       # System Offset Calibration 1111   0011 (F3h)
       'CMD_SYSOCAL': 0xF3,
       'CMD_SYSGCAL': 0xF4,    # System Gain Calibration 1111    0100 (F4h)
       # Synchronize the A/D Conversion 1111   1100 (FCh)
       'CMD_SYNC': 0xFC,
       'CMD_STANDBY': 0xFD,    # Begin Standby Mode 1111   1101 (FDh)
       'CMD_RESET': 0xFE,      # Reset to Power-Up Values 1111   1110 (FEh)
       }


class HP_ADPin(ANAPin):

    def __init__(self, num: int, tag=''):
        super().__init__(num, IOFlow.IN, IOType.ANA, tag)
        self.hpad: HP_ADDA = None

    def on_setup(self, host: Board):
        self.hpad = host

    def input(self) -> float:
        return self.hpad.get_value(self.num)

    def output(self, val: float):
        pass


HP_ADDA_SLOTS = [HP_ADPin(0), HP_ADPin(1), HP_ADPin(2), HP_ADPin(3),
                 HP_ADPin(4), HP_ADPin(5), HP_ADPin(6), HP_ADPin(7)]


class HP_ADDA(Board):
    # ADS1256

    RBP_PINS = (MOSIPin(9), MISOPin(10), SCLKPin(11),
                RBP_GPIO(17, IOFlow.IN, tag='drdy'),
                RBP_GPIO(18, tag='rst'), RBP_GPIO(22, tag='cs'))

    def __init__(self):
        super().__init__()
        self.spi = SPI()
        self.spi.set_mode(0b01)
        self.spi.set_speed(3000000)
        self.cs: RBP_GPIO = None
        self.drdy: RBP_GPIO = None
        self.rst: RBP_GPIO = None
        self.scan_mode = 0
        self.slots = HP_ADDA_SLOTS.copy()

    def on_attached(self):
        for pin in self.pins:
            setattr(self, pin.tag, pin)
        self.reset()
        self.wait_ready()
        self.setup(GAIN['ADS1256_GAIN_1'], DRATE['ADS1256_30000SPS'])

    def wait_ready(self):
        for i in range(0, 400000, 1):
            if(self.drdy.input() == 0):
                return
        raise Exception('HP_ADDA timeout')

    def setup(self, gain: int, drate: int):
        assert self.read_chip_id() == 3, 'Fail to read chip id'
        buf = [0, 0, 0, 0, 0, 0, 0, 0]
        buf[0] = (0 << 3) | (1 << 2) | (0 << 1)
        buf[1] = 0x08
        buf[2] = (0 << 5) | (0 << 3) | (gain << 0)
        buf[3] = drate
        self.cs.output(0)
        self.spi.write_byte([CMD['CMD_WREG'] | 0, 0x03])
        self.spi.write_byte(buf)
        self.cs.output(1)
        time.sleep(0.001)

    def reset(self):
        self.rst.output(1)
        time.sleep(0.2)
        self.rst.output(0)
        time.sleep(0.2)
        self.rst.output(1)

    def read_chip_id(self):
        id = self.read_data(REG['REG_STATUS'])
        id = id[0] >> 4
        return id

    def read_data(self, reg: int):
        self.cs.output(0)
        self.spi.write_byte([CMD['CMD_RREG'] | reg, 0x00])
        data = self.spi.read_byte(1)
        self.cs.output(1)
        return data

    def write_cmd(self, reg: int):
        self.cs.output(0)
        self.spi.write_byte([reg])
        self.cs.output(1)

    def write_reg(self, reg, data):
        self.cs.output(0)
        self.spi.write_byte([CMD['CMD_WREG'] | reg, 0x00, data])
        self.cs.output(1)

    def set_channel(self, channel):
        if channel > 7:
            return 0
        self.write_reg(REG['REG_MUX'], (channel << 4) | (1 << 3))

    def set_diff_channel(self, channel):
        if channel == 0:
            self.write_reg(REG['REG_MUX'], (0 << 4) | 1)
        elif channel == 1:
            self.write_reg(REG['REG_MUX'], (2 << 4) | 3)
        elif channel == 2:
            self.write_reg(REG['REG_MUX'], (4 << 4) | 5)
        elif channel == 3:
            self.write_reg(REG['REG_MUX'], (6 << 4) | 7)

    def read_adc_data(self):
        self.wait_ready()
        self.cs.output(0)
        self.spi.write_byte([CMD['CMD_RDATA']])
        buf = self.spi.read_byte(3)
        self.cs.output(1)
        read = (buf[0] << 16) & 0xff0000
        read |= (buf[1] << 8) & 0xff00
        read |= (buf[2]) & 0xff
        if (read & 0x800000):
            read &= 0xF000000
        return read

    def get_value(self, channel):
        value = 0
        if(self.scan_mode == 0):
            if(channel >= 8):
                return 0
            self.set_channel(channel)
            self.write_cmd(CMD['CMD_SYNC'])
            self.write_cmd(CMD['CMD_WAKEUP'])
            value = self.read_adc_data()
        else:
            if(channel >= 4):
                return 0
            self.set_diff_channel(channel)
            self.write_cmd(CMD['CMD_SYNC'])
            self.write_cmd(CMD['CMD_WAKEUP'])
            value = self.read_adc_data()
        return value*5.0/0x7fffff

    def get_values(self):
        values = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, 8, 1):
            values[i] = self.get_value(i)
        return values
