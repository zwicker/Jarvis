from Holodeck.Settings import Pipe as P
from Outputs.RGBMultiController import NTOWER, NRING
from Outputs.ScreenController import ScreenController as scl
from Holodeck.Engine import EffectTemplate, classname_to_id
from random import randint
import time
import inspect
import sys
IMG_PATH = "Holodeck/Images/"
#location_weather_time
#SKY = [20, 100, 205]
SKY = [200, 200, 230]
SAND = [180, 140, 100]
#GRASS = [50, 125, 0]
GRASS = [139, 90, 19]

def flicker(rgb, flicker = 3):
  randomNum = randint(0,2)

  if randomNum == 0:
    if rgb[0] <= 255 - flicker:
      rgb[0] = rgb[0] + flicker
    if rgb[1] <= 255 - flicker:
      rgb[1] = rgb[1] + flicker
    if rgb[2] <= 255 - flicker:
      rgb[2] = rgb[2] + flicker
  elif randomNum == 1:
    if rgb[0] > 0 + flicker:
      rgb[0] = rgb[0] - flicker
    if rgb[1] > 0 + flicker:
      rgb[1] = rgb[1] - flicker
    if rgb[2] > 0 + flicker:
      rgb[2] = rgb[2] - flicker

  return rgb

class LocationTemplate(EffectTemplate):
  TRANSITION_TIME = 3.0
  
  def __init__(self, pipes, active_effects, remove_cb):
    EffectTemplate.__init__(self, pipes, active_effects, remove_cb)
    self.steady_mapping = dict(
      [(k,c[0]) for (k,c) in self.get_mapping().items()]
    )
    self.transition_timer = time.time()
    self.handle_blacklist()

  def get_blacklist(self):
    cs = inspect.getmembers(sys.modules[__name__], inspect.isclass)    
    result = []
    for n,c in cs:
      if c is LocationTemplate or c is self.__class__:
        continue
      if not issubclass(c, LocationTemplate):
        continue
      result.append(c)
    return result
   
  def wall_img_default(self, prev):
    prev[0] = classname_to_id(self.__class__.__name__)
    return prev

  def window_img_default(self, prev):
    prev[0] = classname_to_id(self.__class__.__name__)
    return prev
    
  def audio_default(self, prev):
    if not self.transition_timer:
      # Ambient audio
      prev[0].append(classname_to_id(self.__class__.__name__))
      return prev
    else:
      # Transition audio
      prev[1].append("swoosh")
      if self.transition_timer + self.TRANSITION_TIME < time.time():
        self.transition_timer = None
      return prev

  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.TOWER: (self.tower, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
      P.WALLIMG: (self.wall_img_default, 1),
      P.WINDOWIMG: (self.window_img_default, 1),
      P.SOUND: (self.audio_default, 1),
    }
  
class ForestEffect(LocationTemplate):
  def floor(self, prev):
    return [102, 55, 0]

  def tower(self, prev):
    return prev

  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return [102, 155, 0]

class PlainsEffect(LocationTemplate):
  def floor(self, prev):
    return GRASS
    
  def tower(self, prev):
    return [(list(SKY)) for i in xrange(NTOWER)]
    
  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return [0, 128, 0]

class TundraEffect(LocationTemplate):
  def floor(self, prev):
    return [255,255,255]
    
  def tower(self, prev):
    return [(list(SKY)) for i in xrange(NTOWER)]

  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return [255,255,255]
    
class RiverEffect(LocationTemplate):
  def floor(self, prev):
    return [50,50,200]

  def tower(self, prev):
    return [(list(SKY)) for i in xrange(NTOWER)]
    
  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return [0,0,255]
    
    
class DesertEffect(LocationTemplate):
  def floor(self, prev):
    return SAND
    
  def tower(self, prev):
    return [flicker(list(SKY)) for i in xrange(NTOWER)]

  def window_top(self, prev):
    return flicker(list(SKY))

  def window_bot(self, prev):
    return SAND

class WaterEffect(LocationTemplate):
  def floor(self, prev):
    return [0,0,255]

  def tower(self, prev):
    return [(list(SKY)) for i in xrange(NTOWER)]

  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return [0,0,255]
50 
class JungleEffect(LocationTemplate):
  def floor(self, prev):
    return [102, 55, 0]
  
  def tower(self, prev):
    return prev

  def window_top(self, prev):
    return [0, 125, 0]

  def window_bot(self, prev):
    return [0, 125, 0]

class BeachEffect(LocationTemplate): 
  def floor(self, prev):
    return SAND

  def tower(self, prev):
    return [(list(SKY)) for i in xrange(NTOWER)]

  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return SAND

class MountainEffect(LocationTemplate):
  def floor(self, prev):
    return [255,255,255]
    
  def tower(self, prev):
    return [(list(SKY)) for i in xrange(NTOWER)]

  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return [255,255,255]
