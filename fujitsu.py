# Fujitsu air conditioner remote AR-REA2E

from piir import Remote
from datetime import datetime

class Fujitsu_AR_REA2E:
  format = {
    "format": {
      "preamble": [
        8,
        4
      ],
      "coding": "ppm",
      "zero": [
        1,
        1
      ],
      "one": [
        1,
        3
      ],
      "postamble": [
        1
      ],
      "pre_data": "14 63 00 10 10",
      "timebase": 420,
      "gap": 84000,
      "carrier": 38000,
    },
    "keys": {}
  }

  power = False
  mode = 'cool'
  temperature = 18
  fan_speed = 0
  swing = False

  
  def __init__(self, gpio):
    self.remote = Remote(self.format, gpio)

  def send(self):
    data = []

    if self.power == False:
      data.extend([0x02, 0xFD])
      self.remote.send_data(bytes(data))
      return

    data.extend([0xFE, 0x09, 0x30])

    if self.temperature < 18 or self.temperature > 30:
      raise ValueError('temperature must be between 18 and 30 celsius')


    data.append(0x20 + (self.temperature - 18) * 0x10)

    if self.mode == 'auto':
      data.append(0)
    elif self.mode == 'cool':
      data.append(1)
    elif self.mode == 'dry':
      data.append(2)
    elif self.mode == 'fan':
      data.append(3)
    elif self.mode == 'heat':
      data.append(4)
    else:
      raise ValueError('mode must be one of auto, cool, dry, fan, heat')
    
    if self.fan_speed < 0 or self.fan_speed > 40:
      raise ValueError('fan_speed must be 0 for auto or an integer between 1 and 4 for fixed')
    
    if self.fan_speed == 0:
      d = 0
    else:
      d = 5 - self.fan_speed

    if self.swing:
      d |= 0x10

    data.append(d)
    
    now = datetime.now()

    data.extend([int('0x' + str(now.hour), 0), now.isoweekday(), int('0x' + str(now.minute), 0)])

    data.append(0x20)
    
    # Checksum
    data.append(self.checksum(data))

    print(' '.join(format(x, '02x') for x in data))

    self.remote.send_data(bytes(data))

  def checksum(self, data: list):
    s = 0
    for i in range(2, len(data)):
        s = s + data[i]
    return 0x100 - s & 0xFF