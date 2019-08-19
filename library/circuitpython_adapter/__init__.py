class not_SMBus:
    """not_SMBus

    :param ~microcontroller.pin SCL: The pin the i2c SCL line is connected to. If not defined, defaults to board.SCL

    :param ~microcontroller.pin SDA: The pin the i2c SDA line is connected to. If not defined, defaults to board.SDA
    
    :param *args: Unused, only exists to prevent errors when used as a drop in for SMBus
    """
    def __init__(self, SCL=None, SDA=None, *args):
        import board
        import busio

        if SCL is None:
            SCL = board.SCL
        
        if SDA is None:
            SDA = board.SDA
        
        self.i2c = busio.I2C(SCL, SDA)

    def write_i2c_block_data(self, i2c_address, register, values):
        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto(i2c_address, bytes([register] + values))
            
        finally:
            self.i2c.unlock()

    def read_i2c_block_data(self, i2c_address, register, bit_width):
        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto(i2c_address, bytes([register]), stop=False)
            buffer = bytearray(bit_width)
            self.i2c.readfrom_into(i2c_address, buffer)
            return list(buffer)

        finally:
            self.i2c.unlock()