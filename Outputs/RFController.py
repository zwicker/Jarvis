import time
import serial
import struct
import logging
from Controller import Controller
from config import RF

class RFController(Controller):
  CMD_FET1 = 0x00
  CMD_FET2 = 0x01
  CMD_FET3 = 0x03
  CMD_RELAY = 0x02
  CMD_IR_BUFFER = 0x10
  CMD_IR_SEND = 0x11
  CMD_IR_RESET = 0x12
  CMD_IR_TEST = 0x14
  CMD_IR_ON = 0x15
  CMD_IR_OFF = 0x16

  DATA_LEN = 5

  def write(self, chars):
    assert(len(chars) == 5)
    try:
      self.ser.write(chars)
      v = self.ser.readline()

      while v.strip() != "":
        self.logger.warn(v)
        v = self.ser.readline()
    except serial.SerialException:
      self.logger.error("Serial error occurred")

  def __init__(self, ser, default_target = 'livingroom', ir_path = "Outputs/IRCommandFiles/"):
    Controller.__init__(self)
    self.ser = ser
    self.ir_path = ir_path
    self.logger.setLevel(logging.INFO)
    assert (ser.readline().strip() == "Ready")

    self.set_default_target(default_target)

  def set_default_target(self, tgt):
    self.default_target = tgt
    self.set_target(self.default_target)

  def set_target(self,tgt):
    self.write(RF[tgt])

  def send_cmd(self, cmd, val, target = None):
    if val == "ON":
      val = 0x01
    elif val == "OFF":
      val = 0x00

    if target and target != self.default_target:
      self.set_target(target)
    
    self.logger.debug("Sending " + str(cmd) + str(val))
    chars = chr(cmd) + struct.pack('>h', int(val)) + ('\0' * (self.DATA_LEN - 3))
    self.write(chars)

    if target and target != self.default_target:
      self.set_target(self.default_target)

  def send_IR(self, fil, target = None):
    with open(self.ir_path + fil, 'r') as f:
      data = f.read()
    data = [d.strip() for d in data.split(",")]

    self.send_cmd(self.CMD_IR_RESET, 0, target)
    for b in data:
      self.send_cmd(self.CMD_IR_BUFFER, int(b), target)

    self.send_cmd(self.CMD_IR_SEND, 3, target)

    self.logger.info("IR written")
    time.sleep(0.5)

if __name__ == "__main__":
  import logging
  import time
  logging.basicConfig()
  ser = serial.Serial("/dev/ttyUSB1", 115200)

  tgt = raw_input("livingroom or hackspace? or todd?")
  con = RFController(ser, tgt)

  while True:
    cmdstr = raw_input("CMD (RELAY/FET1/2 ON/OFF, IR <file>):")
    if len(cmdstr.split()) == 1:
      if cmdstr == "SCDN":
        con.send_IR("ProjectorScreenDown.txt")
      elif cmdstr == "SCST":
        con.send_IR("ProjectorScreenStop.txt")
      elif cmdstr == "SCUP":
        con.send_IR("ProjectorScreenUp.txt")
      elif cmdstr == "IRTEST":
        con.send_cmd(con.CMD_IR_TEST, val)
      elif cmdstr == "IRON":
        con.send_cmd(con.CMD_IR_ON, 0)
      elif cmdstr == "IROFF":
        con.send_cmd(con.CMD_IR_OFF, 0)
      continue
      

    (cmd, val) = cmdstr.split()

    if cmd == "RELAY":
      con.send_cmd(con.CMD_RELAY, val)
    elif cmd == "FET1":
      con.send_cmd(con.CMD_FET1, val)
    elif cmd == "FET2":
      con.send_cmd(con.CMD_FET2, val)
    elif cmd == "FET3":
      con.send_cmd(con.CMD_FET3, val)
    elif cmd == "IR":
      con.send_IR(val)

      
