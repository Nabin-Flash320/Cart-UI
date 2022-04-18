from smbus import SMBus
import struct
addr = 0x08 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

def getFromI2C():
    global addr, bus    
    data = bus.read_i2c_block_data(addr, 0)
    dat = data[4*0:(0+1)*4]
    aux = bytearray(dat)
    data_float = struct.unpack("<f", aux)[0]
    return data_float

def sendFromI2C(dir=None):
    global addr, bus
    direction = dir
    if direction == 'Right':
        bus.write_byte(addr, 0x2)
    elif direction == 'Left':
        bus.write_byte(addr, 0x3)
    elif direction == 'Move':
        bus.write_byte(addr, 0x4)

if __name__ == "__main__":
    sendFromI2C()
		
		
		
		
		
		