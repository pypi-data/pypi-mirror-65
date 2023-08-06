import pygame, sys
import pygame.gfxdraw
from math import pi
import dashdraw

none_color = (246, 246, 246)
COLOR = (66, 165, 245)
GRAY = (none_color[0] - 40, none_color[1] - 40, none_color[2] - 40)
BLACK = (0,0,0)

class Event:
  def __init__(self):
    pass

  def active(self, e, functions = []):
    for f in functions:
      f(e)

class Gauge:
    
  STD = 0
  ARROW = 1
  BAR = 2
  
  def __init__(self, screen, (x, y), size=100, thickness=5, color=COLOR, display=STD):
    self.screen = screen
    self.x = x
    self.y = y
    self.size = size
    self.color = color
    self.display = display
    self.thickness = thickness
    self.value = 0
    self.maxim = 360

  def set_value(self, value):
    self.value = value

  def draw(self, value = None):
    if value <> None:
      self.set_value(value)
    if self.display == Gauge.STD:

      if self.value == 1:
        angle = 269
      else:
        angle = int((360 * self.value) - 90)
      dashdraw.circle(self.screen, self.x, self.y, self.size, self.thickness, none_color)
      dashdraw.arc(self.screen, self.x, self.y, self.size, self.thickness, 270 , angle, self.color)
      
      font = pygame.font.SysFont(None, int(self.size * 0.75))
      text = font.render('{:.1f}%'.format(self.value*100), True, self.color)
      self.screen.blit(text, (self.x - text.get_rect().centerx, int(self.y - text.get_rect().centery * 0.8)))

    elif self.display == Gauge.ARROW:
      variation = (360 - self.maxim) // 2

      v = int((self.maxim * (1 - self.value)) + variation)
      v_arrow =  int((self.maxim * self.value) + variation)

      dashdraw.arc(self.screen, self.x, self.y, self.size - 5, self.thickness,variation - 270, -variation +90, none_color)
      dashdraw.arc(self.screen, self.x, self.y, self.size - 5, self.thickness,variation - 270, -v + 90, self.color)

      font = pygame.font.SysFont(None, 15)
      text = font.render('{:.1f}%'.format(self.value*100), True, none_color)
      self.screen.blit(text, (self.x + 5 - text.get_rect().centerx, self.y + 20))      

      dashdraw.triangle(self.screen, 10, self.size, (self.x, self.y), BLACK, v_arrow)
      dashdraw.triangle(self.screen, 10, 10, (self.x, self.y), BLACK, v_arrow + 180)
      

    elif self.display == Gauge.BAR:
      font = pygame.font.SysFont(None, int(self.size * 0.5))
      text = font.render('{:.1f}%'.format(self.value*100), True, self.color)
      bar = pygame.Rect(self.x - self.size, self.y, int(self.size * 0.2), self.size)
      g_bar = pygame.Rect(self.x - self.size, self.y + int(self.size * (1 - self.value)), int(self.size * 0.2), int(self.size * self.value))
      pygame.gfxdraw.box(self.screen, bar, none_color)
      pygame.gfxdraw.box(self.screen, g_bar, self.color)
      self.screen.blit(text, (self.x + (text.get_rect().centerx //2 ) - self.size, self.y + int(self.size * (1 - self.value))))

  def set_max(self, m):
    if m > 360: self.maxim = 360
    if m < 0: self.maxim = 0
    self.maxim = m

class ButtonONOFF:
  WIDTH = 100
  HEIGHT = 40

  def __init__(self, screen, (x, y), color = COLOR, callback = None):
    self.value = 0
    self.x = x
    self.y = y
    self.color = color
    self.screen = screen
    self.bt_bg =  pygame.Rect(self.x, self.y, ButtonONOFF.WIDTH, ButtonONOFF.HEIGHT)
    self.callback = callback
    self.flag = False

  def draw(self):
    color_pos = BLACK, (none_color[0] - 40, none_color[1] - 40, none_color[2] - 40)
    
    font = pygame.font.SysFont(None, 20)
 
    on = font.render('OFF', True, color_pos[self.flag])
    off = font.render('ON', True, color_pos[self.flag - 1])

    
    pygame.gfxdraw.box(self.screen, self.bt_bg, none_color)

    bt = pygame.Rect(self.x + self.value, self.y, (ButtonONOFF.WIDTH // 2), ButtonONOFF.HEIGHT)
    pygame.gfxdraw.box(self.screen, bt, self.color)

    bt_fill = pygame.Rect(self.x, self.y, ButtonONOFF.WIDTH, ButtonONOFF.HEIGHT)
    pygame.gfxdraw.rectangle(self.screen, bt_fill, BLACK)
    pygame.gfxdraw.vline(self.screen, self.x + (ButtonONOFF.WIDTH // 2), self.y, self.y + ButtonONOFF.HEIGHT, BLACK)    
    
    self.screen.blit(on, (self.x - 10 + ButtonONOFF.WIDTH // 4, self.y - 5 + ButtonONOFF.HEIGHT // 2))
    self.screen.blit(off, (self.x + 10 + ButtonONOFF.WIDTH // 2, self.y - 5 + ButtonONOFF.HEIGHT // 2))
  
  def click(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:      
      m_x, m_y = event.pos
      if self.bt_bg.collidepoint(m_x, m_y):
        self.flag = not self.flag
        if self.callback: self.callback(self.flag)
        self.value = self.value + (ButtonONOFF.WIDTH // 2)
        if self.value >= ButtonONOFF.WIDTH:
          self.value = 0
  
  def get(self):
    return self.flag

class Slide:
  def __init__(self, screen, (x, y), size = 250, color = COLOR, callback=None):
    self.screen = screen
    self.x = x
    self.y = y
    self.color = color
    self.callback = callback
    self.on_click = False
    self.mouse_pos = x
    self.size = size
    self.pos = float(self.mouse_pos - self.x) / self.size
    self.slide = pygame.Rect(self.x - 10, self.y - 10, self.size + 20, 20)

  def get_pos(self):
    self.pos = float(self.mouse_pos - self.x) / self.size
    if self.pos < 0: self.pos = 0
    if self.pos > 1: self.pos = 1
    return self.pos
  
  def set_pos(self, pos):
    if pos <= 1 and pos >= 0: 
      self.pos = pos
      self.mouse_pos = self.x + int(pos * self.size)

  def draw(self, position = None):
    if position <> None: self.set_pos(position)
    font = pygame.font.SysFont(None, 15)
    text = font.render('{:.1f}%'.format(self.get_pos()*100), True, none_color)
    self.screen.blit(text, (self.mouse_pos + 5 - text.get_rect().centerx, self.y - 20))
    pygame.gfxdraw.hline(self.screen, self.x, self.x + self.size, self.y, none_color)
    pygame.gfxdraw.hline(self.screen, self.x, self.mouse_pos, self.y, self.color)
    pygame.draw.circle(self.screen, self.color, (self.mouse_pos + 1, self.y + 1), 9)
    pygame.gfxdraw.aacircle(self.screen, self.mouse_pos, self.y, 10, (10, 10 ,10))
    if self.on_click:
      self.mouse_pos = pygame.mouse.get_pos()[0]
      self.get_pos()
      if self.mouse_pos > (self.x + self.size):
        self.mouse_pos = (self.x + self.size)
      elif self.mouse_pos < self.x:
        self.mouse_pos = self.x

  def click(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      m_x, m_y = event.pos
      if self.slide.collidepoint(m_x, m_y):
        self.on_click = True
        if self.callback: self.callback(not self.on_click, self.pos)
    if event.type == pygame.MOUSEBUTTONUP:
      if self.on_click:
        self.on_click = False
        if self.callback: self.callback(not self.on_click, self.pos)

class Lamp:
  def __init__(self, screen, (x, y), name="unknow", color = COLOR):
    self.screen = screen
    self.x, self.y = x, y
    self.name = name
    self.color = color
    self.state = False

  def draw(self):
    font = pygame.font.SysFont(None, 25)
    text = font.render(self.name, True, none_color)
    rect = text.get_rect()
    rect.top = rect.top + self.y
    rect.left = rect.left + self.x + 30
    rect.width += 15 - 4
    rect.height += 15 - 4
    dashdraw.roundrect(self.screen, rect, color = BLACK, rounded = 2)
    self.screen.blit(text, (self.x + 35, self.y + 5))  
    rect = pygame.Rect(self.x, self.y, 30, 30)
    rect_lamp = pygame.Rect(self.x + 3, self.y + 3, 24, 14)
    dashdraw.roundrect(self.screen, rect, color = none_color, rounded = 2)
    if self.state:
      color = self.color
    else:
      color = GRAY
    dashdraw.roundrect(self.screen, rect_lamp, color = color, rounded=2)

  def set_state(self, state):
    self.state = state