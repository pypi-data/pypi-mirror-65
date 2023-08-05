import time
from .mcp_expander import McpExpander, Blind, BlindControl
import RPi.GPIO as GPIO


class BlindsCircuit():
    mcp = []
    blinds_list = []
    blind_controls_list = []
    
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(22, GPIO.OUT)
        GPIO.output(22, GPIO.LOW)
        time.sleep(.5)
        GPIO.output(22, GPIO.HIGH)
        GPIO.setup(23, GPIO.IN)
        GPIO.add_event_detect(23, GPIO.RISING, callback=self.event_detect, bouncetime=300)

        for value in range(0x20, 0x25):
            self.mcp.append(McpExpander(address=value,))

        
        for l in self.mcp:
            if(isinstance(l, Blind)):
                self.blinds_list.append(l.get_blinds_list())
            elif(isinstance(l, BlindControl) ):
                self.blind_controls_list.append(l.get_blinds_control_list())

    """ function called from GPIO.add_event_detect"""
    def event_detect(self):
        print("not working my callback from event detect")

    """get unnested list of blinds"""
    def get_blinds_list(self): 
        return_list = []
        for x in self.mcp :
            for blind in x.get_blinds_list():
                return_list.append(blind)
        return return_list

    """get unnested list of blind controls (input switches)"""
    def get_blind_controls_list(self): 
        return_list = []
        for x in self.blind_controls_list:
            for blind_controls in x:
                return_list.append(blind_controls)
        return return_list

    def set_blinds_up(self, blinds_direction = "up", blinds_controlled = [], *args, **kvargs):
        self.set_blinds(blinds_direction="up", blinds_controlled = blinds_controlled)

    def set_blinds_down(self, blinds_direction = "down", blinds_controlled = [], *args, **kvargs):
        self.set_blinds(blinds_direction="down", blinds_controlled = blinds_controlled)

    def set_blinds(self, blinds_direction = "stop", blinds_controlled = [], *args, **kvargs):
        #print(f"self.get_blinds_list()):{self.get_blinds_list())}, blinds_controlled:{blinds_controlled}")
        for i in blinds_controlled:
            if(i < len(self.get_blinds_list())):
                #blind = self.get_blinds_list()[i]
                #getattr(blind, (f"{(blinds_direction).lower()}"))()
                getattr(self.get_blinds_list()[i],  (f"{(blinds_direction).lower()}"))()
                #exec(f"self.get_blinds_list(){[i]}.{(blinds_direction).lower()}()")

            


    def apply_changes_to_output(self):
        for m in self.mcp:
            m.apply_changes_to_output()

    def get_interrupt_signal(self):
        if(GPIO.input(23)):
            self.mcp[4].read_input_on_interrupt()
        return GPIO.input(23)


    def __str__(self):
        return_string = ""
        for s in self.mcp:         
            return_string = "#{} {}#\n".format(return_string, str(s) )
        return return_string

    
