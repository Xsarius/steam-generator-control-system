import minimalmodbus, struct

class Keller23sx():
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, unit=1, registers_dict={}):
        self.registers_dict = registers_dict
        self.socket = minimalmodbus.Instrument(port=port, slaveaddress=unit)
        self.socket.serial.baudrate=baudrate
        self.socket.serial.timeout = 3

    def read(self, reg_name):
        data = self.get_register(reg_name)
        register_addr = data[0]
        num_of_registers = data[1]
        raw_data = self.socket.read_registers(registeraddress=register_addr, number_of_registers=num_of_registers)
        raw_data[0] = raw_data[0]<<16
        corr_data = raw_data[0] | raw_data[1]
        corr_data = struct.unpack('!f', bytes.fromhex('{:x}'.format(corr_data)))[0]

        return float('%.4f' % corr_data)

    def write(self, register_addr, data):
        return self.socket.write_float(registeraddress=register_addr)

    def get_register(self, name):
        curr_reg = self.registers_dict[name]
        dec_reg_val = int(curr_reg[0],16)
        num_of_regs = curr_reg[1]
        return [dec_reg_val, num_of_regs]

if __name__ == "__main__":
    dev = Keller23sx()
    print(dev.socket.read_registers(registeraddress=2,number_of_registers=2))