import os, sys, json, random, pygame

import tools


# 奖励物品
class Bouns:
	pics = None

	def __init__(self):
		if self.pics is None:
			self.pics = []
			self.pics.append(tools.getSubPic(pygame.Rect(256, 112, 16, 16), 3))  #钢盔
			self.pics.append(tools.getSubPic(pygame.Rect(272, 112, 16, 16), 3))  #定时
			self.pics.append(tools.getSubPic(pygame.Rect(288, 112, 16, 16), 3))  #铲子
			self.pics.append(tools.getSubPic(pygame.Rect(304, 112, 16, 16), 3))  #五星
			self.pics.append(tools.getSubPic(pygame.Rect(320, 112, 16, 16), 3))  #手雷
			self.pics.append(tools.getSubPic(pygame.Rect(336, 112, 16, 16), 3))  #坦克
			ckey = pygame.Color(0, 66, 74)
			rect = pygame.Rect(0, 0, 48, 48)
			for i in range(6):
				self.pics[i] = tools.getPicByColorkey(self.pics[i], rect, ckey)

		self.isCache = True
		self.id = 0
		self.rect = pygame.Rect(0, 0, 48, 48)

	def init(self, px, py):
		self.isCache = False
		self.id = random.randint(0, 5)
		self.rect.x = px
		self.rect.y = py

	def update(self):
		pass

	def draw(self, canvas):
		if self.isCache: return
		canvas.blit(self.pics[self.id], self.rect.topleft)

	def destory(self):
		self.isCache = True
