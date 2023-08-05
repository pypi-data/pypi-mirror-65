#from blind import blind
from bitstring import BitArray
from smbus2 import SMBus 
import RPi.GPIO as GPIO

address_map = {
    0x00: 'IODIRA',   0x01: 'IODIRB',   0x02: 'IPOLA',   0x03: 'IPOLB',
    0x04: 'GPINTENA', 0x05: 'GPINTENB', 0x06: 'DEFVALA', 0x07: 'DEFVALB',
    0x08: 'INTCONA',  0x09: 'INTCONB',  0x0a: 'IOCONA',   0x0b: 'IOCONB',
    0x0c: 'GPPUA',    0x0d: 'GPPUB',    0x0e: 'INTFA',   0x0f: 'INTFB',
    0x10: 'INTCAPA',  0x11: 'INTCAPB',  0x12: 'GPIOA',   0x13: 'GPIOB',
    0x14: 'OLATA',    0x15: 'OLATB'
}
    
register_map = {value: key for key, value in address_map.items()}
#max_len = max(len(key) for key in register_map)

class Blind():
    blind_count = []
    blind_count.append(0)
    

    def __init__(self, *args, **kwargs):
        self.address = 0x20
        self.gpio_register = "gpa"
        self.interrupt_bits = "empty"
        self.output_bits = "empty"
        self.down_bit = 0
        self.blind_number = self.blind_count[0]
        self.blind_count[0] = self.blind_count[0] +1
        
        for key, value in kwargs.items():
            for var in vars(self):  #iterate through vriables in function
                if(key == var):
                    setattr(self, var, value)  #assign value to function variable
                
        self.up_bit = self.down_bit + 1

    #def inc_blind_count
    def up(self):
        if(self.interrupt_bits.all(1, [self.down_bit, self.up_bit]) and self.output_bits.all(1, [self.down_bit, self.up_bit])):
            self.output_bits.set(False, self.up_bit)
            print(f"Blind: {self.blind_number}, going ↑UP↑ ...")
        else:
            self.output_bits.set(True, [self.down_bit, self.up_bit])
            print(f"Blind: {self.blind_number}, ↑stop↑ ...")

    def down(self):
        if(self.interrupt_bits.all(1, [self.down_bit, self.up_bit-1]) and self.output_bits.all(1, [self.down_bit, self.up_bit])):
            self.output_bits.set(False, self.down_bit)
            print(f"Blind: {self.blind_number}, going ↓DOWN↓ ...")
        else:
            self.output_bits.set(True, [self.down_bit, self.up_bit])
            print(f"Blind: {self.blind_number}, ↓stop↓ ...")

    def stop(self):
        if(self.interrupt_bits.any(1, [self.down_bit, self.up_bit]) or self.output_bits.any(1, [self.down_bit, self.up_bit])):
            self.output_bits.set(True, [self.down_bit, self.up_bit])
            print(f"Blind: {self.blind_number}, ←stop→ ...")

    def __str__(self):
        return_string = f"Blind number:{ self.blind_number }, Adress:{self.address}, {self.gpio_register},output_bits:{self.output_bits[self.down_bit: self.up_bit+1]}, " 
        return str(f"{return_string} interrupt_bits:{self.interrupt_bits[self.down_bit: self.up_bit+1]} " )

class BlindControl():
    blind_count = []
    blind_count.append(0)

    def __init__(self, *args, **kwargs):
        self.address = 0x24
        self.gpio_register = "gpa"
        self.interrupt_bits = "empty"
        self.input_bits = "empty"
        self.down_bit = 0
        self.blind_number = self.blind_count[0]
        self.blind_count[0] = self.blind_count[0] +1
        
        for key, value in kwargs.items():
            for var in vars(self):  #iterate through vriables in function
                if(key == var):
                    setattr(self, var, value)  #assign value to function variable
        self.up_bit = self.down_bit + 1


    def get_input(self):
        if(self.input_bits[self.up_bit]):
            print(f"Imput: Switch {self.blind_number}, pushed for ↑UP↑ ...")
            return [self.blind_number, "UP"]
        if(self.input_bits[self.down_bit]):
            print(f"Imput: Switch {self.blind_number}, pushed for ↓DOWN↓ ...")
            return [self.blind_number, "DOWN"]
        else:
            pass


    def __str__(self):
        return_string = f"Blind control number:{self.blind_number}, Adress:{self.address}, {self.gpio_register}, input_bits:{self.input_bits[self.down_bit: self.up_bit+1]}"
        return str(f"{return_string} interrupt_bits:{self.interrupt_bits[self.down_bit: self.up_bit+1]} ")



class McpExpander():

    def __init__(self, *args, **kwargs):
        self.blinds = []
        self.blind_controls = []
        self.address = 0x20
  
        self.output_state = {'gpa': BitArray(uintle=0xff, length=8), 'gpb': BitArray(uintle=0xff, length=8)}
        self.interrupt_state = {'gpa': BitArray(uintle=0xff, length=8), 'gpb' : BitArray(uintle=0xff, length=8)}
        self.input_state = {'gpa': BitArray(uintle=0x00, length=8), 'gpb': BitArray(uintle=0x00, length=8)}

        self.bits_gpa = self.output_state["gpa"]
        self.bits_gpb = self.output_state["gpb"]
        self.bits_gpa_i = self.interrupt_state["gpa"]
        self.bits_gpb_i =self.interrupt_state["gpb"]

        for key, value in kwargs.items():
            """assign values to variables"""
            for var in vars(self):
                if(key == var):
                   setattr(self, key, value)


        self.mcp_expander = {"address": self.address, "output_state": self.output_state, "interrupt_state": self.interrupt_state}

        if (self.address < 0x24):
            self.make_blinds_from_outputs()
        else:
            self.make_blind_controls_from_inputs()

    """make eight blinds from gpa(eight bits) and gpb(gpb eight) bits, each blind takes up two bits"""
    def make_blinds_from_outputs(self, address = 0x20):
        device = self.address
        with SMBus(1) as bus:
            bus.write_byte(0x77, 0x05)
            bus.write_byte_data(device, register_map['GPIOA'], 0xFF)
            bus.write_byte_data(device, register_map['GPIOB'], 0xFF)
            bus.write_byte_data(device, register_map['GPPUA'], 0xFF)
            bus.write_byte_data(device, register_map['GPPUB'], 0xFF)
            bus.write_byte_data(device, register_map['IODIRA'], 0x00)
            bus.write_byte_data(device, register_map['IODIRB'], 0x00)

        for i in range(8):
            down_bit = i*2
            if(i < 4): #gpa bits
                self.blinds.append(Blind (address=self.address, output_bits=self.bits_gpb, 
                    interrupt_bits=self.bits_gpb_i, gpio_register="gpb", down_bit=down_bit))
            elif(i >= 4): #gpa bits
                down_bit -= 8
                self.blinds.append(Blind (address=self.address, output_bits=self.bits_gpa, 
                    interrupt_bits=self.bits_gpa_i, gpio_register="gpa", down_bit=down_bit))


    def make_blind_controls_from_inputs(self, address = 0x24, number_of_blind_controls=8):
        device = self.address
        with SMBus(1) as bus:
            bus.write_byte(0x77, 0x05)
            bus.write_byte_data(0x24, register_map['IOCONA'], 0x6A) #bit7=bank, bit6=mirror,   
            bus.write_byte_data(0x24, register_map['IODIRA'], 0xFF)
            bus.write_byte_data(0x24, register_map['IODIRB'], 0xFF)
            bus.write_byte_data(0x24, register_map['GPINTENA'], 0xFF)
            bus.write_byte_data(0x24, register_map['GPINTENB'], 0xFF)
            bus.write_byte_data(0x24, register_map['DEFVALA'], 0xFF)
            bus.write_byte_data(0x24, register_map['DEFVALB'], 0xFF)
            bus.write_byte_data(0x24, register_map['INTCONA'], 0xFF)
            bus.write_byte_data(0x24, register_map['INTCONB'], 0xFF)
            bus.write_byte_data(0x24, register_map['IPOLA'], 0xFF)
            bus.write_byte_data(0x24, register_map['IPOLB'], 0xFF)


           #value_a = bus.read_byte_data(0x24, register_map['INTCAPA'])
            #value_b = bus.read_byte_data(0x24, register_map['INTCAPB'])
            gpioa = bus.read_byte_data(0x24, register_map['GPIOA'])
            gpiob = bus.read_byte_data(0x24, register_map['GPIOB'])
            self.bits_gpa_i.overwrite(f"0x{gpioa:02x}", 0)
            self.bits_gpb_i.overwrite(f"0x{gpiob:02x}", 0)
            self.bits_gpa.overwrite(f"0x{gpioa:02x}", 0)
            self.bits_gpb.overwrite(f"0x{gpiob:02x}", 0)
        
        for i in range(number_of_blind_controls):
            down_bit = i*2
            if(i < 4): #gpb bits
                self.blind_controls.append(BlindControl (address=self.address, input_bits=self.bits_gpb, 
                    interrupt_bits=self.bits_gpb_i, gpio_register = "gpb", down_bit = down_bit, output_state = self.output_state))
            elif(i >= 4): #gpa bits
                down_bit -= 8
                self.blind_controls.append(BlindControl (address=self.address, input_bits=self.bits_gpa, 
                    interrupt_bits=self.bits_gpa_i, gpio_register = "gpa", down_bit = down_bit, output_state = self.output_state))

    def read_input_on_interrupt(self):
        with SMBus(1) as bus:
            bus.write_byte(0x77, 0x05)
            #vala = bus.read_byte_data(0x24, register_map['GPIOA'])
            #valb = bus.read_byte_data(0x24, register_map['GPIOB'])
            #value_a = bus.read_byte_data(0x24, register_map['INTCAPA'])
            #value_b = bus.read_byte_data(0x24, register_map['INTCAPB'])
            gpioa = bus.read_byte_data(0x24, register_map['GPIOA'])
            gpiob = bus.read_byte_data(0x24, register_map['GPIOB'])
            self.bits_gpa.overwrite(f"0x{gpioa:02x}", 0)
            self.bits_gpb.overwrite(f"0x{gpiob:02x}", 0)



    def apply_changes_to_output(self):
        with SMBus(1) as bus:
            bus.write_byte(0x77, 0x05)
            bus.write_byte_data(self.address, register_map['GPIOA'], self.bits_gpa.uintle)
            bus.write_byte_data(self.address, register_map['GPIOB'], self.bits_gpb.uintle)
            gpioa = bus.read_byte_data(self.address, register_map['GPIOA'])
            gpiob = bus.read_byte_data(self.address, register_map['GPIOB'])
            self.bits_gpa_i.overwrite(f"0x{gpioa:02x}", 0)
            self.bits_gpb_i.overwrite(f"0x{gpiob:02x}", 0)
                

    def get_blinds_list(self):
        return self.blinds

    def get_blinds_controls_list(self):
        return self.blinds_controls


    def __str__(self): 
        return_string = f"McpAddress: {self.address}, {self.output_state}, {self.interrupt_state}\n"
        for s in self.blinds:
                return_string = f"{return_string} {str(s)}\n"
        for s in self.blind_controls:
                return_string = f"{return_string} {str(s)}\n"
        return return_string
