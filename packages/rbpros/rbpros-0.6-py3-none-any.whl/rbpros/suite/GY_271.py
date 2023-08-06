import math
import time
from typing import List, Union
from ..device import Compass
from ..pin import I2C, IOType

REG_XOUT_LSB = 0x00     # Output Data Registers for magnetic sensor.
REG_XOUT_MSB = 0x01
REG_YOUT_LSB = 0x02
REG_YOUT_MSB = 0x03
REG_ZOUT_LSB = 0x04
REG_ZOUT_MSB = 0x05
REG_STATUS_1 = 0x06     # Status Register.
REG_TOUT_LSB = 0x07     # Output Data Registers for temperature.
REG_TOUT_MSB = 0x08
REG_CONTROL_1 = 0x09    # Control Register #1.
REG_CONTROL_2 = 0x0a    # Control Register #2.
REG_RST_PERIOD = 0x0b   # SET/RESET Period Register.
REG_CHIP_ID = 0x0d      # Chip ID register.

# Flags for Status Register #1.
STAT_DRDY = 0b00000001  # Data Ready.
STAT_OVL = 0b00000010   # Overflow flag.
STAT_DOR = 0b00000100   # Data skipped for reading.

# Flags for Status Register #2.
INT_ENB = 0b00000001    # Interrupt Pin Enabling.
POL_PNT = 0b01000000    # Pointer Roll-over.
SOFT_RST = 0b10000000   # Soft Reset.

# Flags for Control Register 1.
MODE_STBY = 0b00000000  # Standby mode.
MODE_CONT = 0b00000001  # Continuous read mode.
ODR_10HZ = 0b00000000   # Output Data Rate Hz.
ODR_50HZ = 0b00000100
ODR_100HZ = 0b00001000
ODR_200HZ = 0b00001100
RNG_2G = 0b00000000     # Range 2 Gauss: for magnetic-clean environments.
RNG_8G = 0b00010000     # Range 8 Gauss: for strong magnetic fields.
OSR_512 = 0b00000000    # Over Sample Rate 512: less noise, more power.
OSR_256 = 0b01000000
OSR_128 = 0b10000000
OSR_64 = 0b11000000     # Over Sample Rate 64: more noise, less power.


class GY_271(Compass):
    # QMC5883L

    def __init__(self):
        super().__init__()
        self.i2c = I2C(0x0d)
        self.output_data_rate = ODR_100HZ
        self.output_range = RNG_8G
        self.oversampling_rate = OSR_512
        self.mode_cont = MODE_CONT | self.output_data_rate | self.output_range | self.oversampling_rate
        self.mode_stby = MODE_STBY | ODR_10HZ | RNG_2G | OSR_64

    def on_attached(self):
        assert any(p.type == IOType.SCL for p in self.pins) and any(
            p.type == IOType.SDA for p in self.pins), 'Invalid Pins'
        self.setup()

    def destory(self):
        self.set_standby()

    def setup(self):
        assert self.i2c.read_byte(REG_CHIP_ID) == 0xff,  'Fail to read chip id'
        self.set_continuous()

    def set_continuous(self):
        self.i2c.write_byte(REG_CONTROL_2, SOFT_RST)
        self.i2c.write_byte(REG_CONTROL_2, INT_ENB)
        self.i2c.write_byte(REG_RST_PERIOD, 0x01)
        self.i2c.write_byte(REG_CONTROL_1, self.mode_cont)

    def set_standby(self):
        self.i2c.write_byte(REG_CONTROL_2, SOFT_RST)
        self.i2c.write_byte(REG_CONTROL_2, INT_ENB)
        self.i2c.write_byte(REG_RST_PERIOD, 0x01)
        self.i2c.write_byte(REG_CONTROL_1, self.mode_stby)

    def read_word(self, reg: int):
        low = self.i2c.read_byte(reg)
        high = self.i2c.read_byte(reg + 1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, reg: int):
        val = self.read_word(reg)
        if val >= 0x8000:  # 32768
            return val - 0x10000  # 65536
        else:
            return val

    def get_magnet_raw(self) -> List[float]:
        i = 0
        [x, y, z] = [None, None, None]
        while i < 20:  # Timeout after about 0.20 seconds.
            status = self.i2c.read_byte(REG_STATUS_1)
            if status & STAT_OVL:
                print('Magnetic sensor overflow')
                if self.output_range == RNG_2G:
                    print('Consider switching to RNG_8G output range')
            if status & STAT_DOR:
                # Previous measure was read partially, sensor in Data Lock.
                x = self.read_word_2c(REG_XOUT_LSB)
                y = self.read_word_2c(REG_YOUT_LSB)
                z = self.read_word_2c(REG_ZOUT_LSB)
                continue
            if status & STAT_DRDY:
                # Data is ready to read.
                x = self.read_word_2c(REG_XOUT_LSB)
                y = self.read_word_2c(REG_YOUT_LSB)
                z = self.read_word_2c(REG_ZOUT_LSB)
                break
            else:
                # Waiting for DRDY.
                time.sleep(0.01)
                i += 1
        return [x, y, z]

    def get_magnet(self) -> List[Union[float, None]]:
        [x, y, z] = self.get_magnet_raw()
        if x == None or y == None:
            [x1, y1] = [x, y]
        else:
            c = self.calibration
            x1 = x * c[0][0] + y * c[0][1] + c[0][2]
            y1 = x * c[1][0] + y * c[1][1] + c[1][2]
        return [x1, y1]

    def get_bearing_raw(self) -> Union[float, None]:
        [x, y, z] = self.get_magnet_raw()
        if x == None or y == None:
            return None

        b = math.degrees(math.atan2(y, x))
        if b < 0:
            b += 360.0
        return b

    def get_bearing(self) -> Union[float, None]:
        [x, y] = self.get_magnet()
        if x == None or y == None:
            return None

        b = math.degrees(math.atan2(y, x))
        if b < 0:
            b += 360.0
        b += self.declination
        if b < 0.0:
            b += 360.0
        elif b >= 360.0:
            b -= 360.0
        return b

    def detect(self,  timeout: float = 0.01) -> bool:
        value = self.get_bearing()
        if value:
            self.value = value
            return True
        return False
