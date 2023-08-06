import pygame, sys
import pygame.gfxdraw
import math

def roundrect(screen, rect, color, rounded=5):
  pygame.draw.circle(screen, color, (rect.topleft[0] + rounded, rect.topleft[1] + rounded), rounded)
  pygame.draw.circle(screen, color, (rect.topright[0] - rounded, rect.topright[1] + rounded), rounded)
  pygame.draw.circle(screen, color, (rect.bottomleft[0] + rounded, rect.bottomleft[1] - rounded), rounded)
  pygame.draw.circle(screen, color, (rect.bottomright[0] - rounded, rect.bottomright[1] - rounded), rounded)
  w = int(rect.width - 2 * rounded)
  h = int(rect.height - 2 * rounded)
  if w < 0: w = 0
  if h < 0: h = 0
  rect_h = pygame.Rect(rect.left, rect.top + rounded, rect.width,  h)
  pygame.draw.rect(screen, color, rect_h)

  rect_w =  pygame.Rect(rect.left + rounded, rect.top, w,  rect.height)
  pygame.draw.rect(screen, color, rect_w)

def arc(screen, x, y, r, t, start, end, color):
  for rad in range(r - t, r + 1):
    pygame.gfxdraw.arc(screen, x, y, rad, start, end, color)

def circle(screen, x, y, r, t, color):
  for rad in range(r - t, r + 1):
    pygame.gfxdraw.aacircle(screen, x, y, rad, color)

def triangle(screen, base, height, center, color, degrees = 0):
  degrees = degrees + 90
  angle = [math.radians(degrees + 90), math.radians(degrees), math.radians(degrees - 90)]
  r = [(base // 2), height, (base // 2)]
  points = []
  
  for i in range(0, len(angle)):
    points.append((center[0] + int(r[i] * math.cos(angle[i])), center[1] + int(r[i] * math.sin(angle[i]))))
  pygame.draw.polygon(screen, color, points)