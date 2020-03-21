#-*-coding:utf-8-*-

import pyaudio
import wave
import sys
import struct
import pygame
import math

SIZE = (320,240)
DOTCOLOR  = (0,255,0)
GRIDCOLOR  = (40,40,0)
BGCOLOR = (0,0,0) #branco
FPS = 25

wav = 'oscillofun-wave.wav'
wf = wave.open(r'oscillofun-wave.wav', 'rb')
READ_LENGTH = (int)(wf.getframerate()/FPS)

pygame.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Oscillofun XY-Demo Osciloscope Emulator')
pygame.mouse.set_visible(0)
grid = pygame.Surface(SIZE)
grid = grid.convert_alpha()
grid.set_alpha(128)
grid.fill(BGCOLOR)

for x in range(10):
    pygame.draw.line(grid, GRIDCOLOR, (x*SIZE[0]/10,0), (x*SIZE[0]/10,SIZE[0]))

for y in range(10):
    pygame.draw.line(grid, GRIDCOLOR, (0 , y*SIZE[1]/10), (SIZE[0] , y*SIZE[1]/10))

pygame.draw.line(grid, GRIDCOLOR, (SIZE[0]/2,0), (SIZE[0]/2,SIZE[0]), 3)
pygame.draw.line(grid, GRIDCOLOR, (0 , SIZE[1]/2), (SIZE[0] , SIZE[1]/2), 3)

for x in range(100):
    pygame.draw.line(grid, GRIDCOLOR, (x*SIZE[0]/100,SIZE[1]/2-3), (x*SIZE[0]/100,SIZE[1]/2+3))

for y in range(100):
    pygame.draw.line(grid, GRIDCOLOR, (SIZE[0]/2 - 3, y*SIZE[1]/100), (SIZE[0]/2 + 3, y*SIZE[1]/100))

surface = pygame.Surface(screen.get_size())

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# 读取数据
frames = wf.readframes(READ_LENGTH)

# 播放  
while frames != '':
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit()
	
	surface.fill(BGCOLOR)
	surface.blit(grid, grid.get_rect())				
	stream.write(frames)
	for i in range(0,READ_LENGTH,1):
		r = struct.unpack('hh', frames[i*4:i*4+4])
		x = int(r[1]*SIZE[0]/65536) + int((SIZE[1])/2)
		y = int(-r[0]*SIZE[1]/65536) + int(SIZE[1]/2+(SIZE[0]-SIZE[1])/2)
		surface.set_at((y,x), DOTCOLOR)

	screen.blit(surface, surface.get_rect())
	pygame.display.flip()

	frames = wf.readframes(READ_LENGTH)

# 停止数据流  
stream.stop_stream()
stream.close()

# 关闭 PyAudio  
p.terminate()  