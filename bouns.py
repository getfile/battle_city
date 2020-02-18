import os, sys, json, random, pygame

import tools
import effect


# 奖励物品
class Bouns:
	pics = None

	def __init__(self, scene):
		if self.pics is None:
			self.pics = []
			self.pics.append(tools.getSubPic(pygame.Rect(256, 112, 16, 16), 3))  #钢盔0
			self.pics.append(tools.getSubPic(pygame.Rect(272, 112, 16, 16), 3))  #定时1
			self.pics.append(tools.getSubPic(pygame.Rect(288, 112, 16, 16), 3))  #铲子2
			self.pics.append(tools.getSubPic(pygame.Rect(304, 112, 16, 16), 3))  #五星3
			self.pics.append(tools.getSubPic(pygame.Rect(320, 112, 16, 16), 3))  #手雷4
			self.pics.append(tools.getSubPic(pygame.Rect(336, 112, 16, 16), 3))  #坦克5
			ckey = pygame.Color(0, 66, 74)
			rect = pygame.Rect(0, 0, 48, 48)
			for i in range(6):
				self.pics[i] = tools.getPicByColorkey(self.pics[i], rect, ckey)

		self.isCache = True
		self.id = 0
		self.rect = pygame.Rect(0, 0, 48, 48)
		self.scene = scene

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

	def beHit(self):
		if self.id == 0:
			self.scene.newEffect(0, 0, effect.EffectArmor)
		if self.id == 1:
			self.scene.newEffect(0, 0, effect.EffectFreeze)
		if self.id == 2:
			self.scene.newEffect(0, 0, effect.EffectFort)
		if self.id == 3:
			self.scene.tankMe.levelUp()
		if self.id == 4:
			self.scene.killAllTankAi()
		if self.id == 5:
			self.scene.addOneLife()
