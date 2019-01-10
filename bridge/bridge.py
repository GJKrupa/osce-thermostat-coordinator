import paho.mqtt.client as mqtt
from time import sleep
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("LORA/send")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    msg_text = str(msg.payload)
    print("Sending LoRa message")
    BOARD.led_on()
    lora.write_payload(bytes(msg_text))
    lora.set_mode(MODE.TX)
    print("LoRa message sent")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt", 1883, 60)

client.loop_start()

BOARD.setup()

parser = LoRaArgumentParser("Continous LoRa receiver.")
class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([1,0,0,0,0,0])

    def on_tx_done(self):
        print("TxDone")
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        BOARD.led_off()

    def on_rx_done(self):
        BOARD.led_on()
        print("\nRxDone")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        payload_txt = "".join(map(chr, payload))
        print(payload_txt)
        client.publish("LORA/recv", payload_txt)
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        BOARD.led_off()
        self.set_mode(MODE.RXCONT)

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(.5)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            sys.stdout.flush()
            sys.stdout.write("\r%d %d %d" % (rssi_value, status['rx_ongoing'], status['modem_clear']))


lora = LoRaRcvCont(verbose=False)
args = parser.parse_args(lora)

lora.set_mode(MODE.STDBY)
lora.set_freq(868.1)
lora.set_pa_config(pa_select=1)

print(lora)
assert(lora.get_agc_auto_on() == 1)

try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    print(lora)
    BOARD.teardown()