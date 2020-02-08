import sys, pygame
import pygame.display as pgDispaly
import pygame.surface as pgSurface
import pygame.draw as pgDraw
import pygame.event as pgEvent

pygame.init()

size = width, height = 480, 480
speed = [1, 1]
black = 0, 0, 0

surface = pgDispaly.set_mode(size, flags=pygame.RESIZABLE)

# ball = pygame.image.load("pikachu.jpg")
ball = pygame.image.load("Game5/images/scene/brick.png")
ballrect = ball.get_rect()
ballrect.width = 48

quit = False
keys = {}

# print(pygame.version)

while 1:
	if quit: break

	for event in pgEvent.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYUP:
			keys[event.key] = False
			if event.key == 27:
				quit = True
		if event.type == pygame.KEYDOWN:
			keys[event.key] = True

	print(keys)

	ballrect = ballrect.move(speed)
	if ballrect.left < 0 or ballrect.right > width:
		speed[0] = -speed[0]
	if ballrect.top < 0 or ballrect.bottom > height:
		speed[1] = -speed[1]

	red = pygame.Color(255, 0, 0)
	green = pygame.Color(0, 255, 0)

	surface.fill(black)  #填充背景
	for xx in range(0, 480, 50):
		for yy in range(0, 480, 50):
			# pgDraw.rect(surface, green, pygame.Rect(xx, yy, 3, 3))
			pgDraw.circle(surface, green, (xx, yy), 10)

	surface.blit(ball, ballrect)  #绘制图片
	pgDraw.line(surface, red, (0, 0), ballrect.center, 10)  #绘制矢量

	pgDispaly.flip()  #更新内容
