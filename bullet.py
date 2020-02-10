import os, sys, pygame

import tools
import effect


# 炮弹
class Bullet:
	pics = None

	def __init__(self):
		if self.pics != None: return
		self.pics = []
		self.pics.append(tools.getSubPic(pygame.Rect(321, 100, 8, 8), 3))
		self.pics.append(tools.getSubPic(pygame.Rect(337, 100, 8, 8), 3))
		self.pics.append(tools.getSubPic(pygame.Rect(328, 100, 8, 8), 3))
		self.pics.append(tools.getSubPic(pygame.Rect(344, 100, 8, 8), 3))

	def init(self, scene, tank, cx, cy):
		self.id = 0
		self.isCache = False  #0空闲(缓存用),1使用
		self.tank = tank  #发射炮弹的坦克id
		self.scene = scene
		self.rect = pygame.Rect(0, 0, 24, 24)
		self.level = tank.level  #炮弹等级(也是坦克等级)
		self.speed = tank.bulletSpeed  #移动速度(必须要比坦克的速度快, 但不能超过小块的宽度)
		self.dx = 0  #移动矢量
		self.dy = 0
		self.dire = tank.dire  #移动方向
		if self.dire == 0: self.dy = -1
		if self.dire == 1: self.dy = 1
		if self.dire == 2: self.dx = -1
		if self.dire == 3: self.dx = 1
		self.cx = cx  #中心位置
		self.cy = cy

	def update(self):
		if self.isCache: return
		self.cx += self.dx * self.speed
		self.cy += self.dy * self.speed
		self.rect.x = self.cx - 12
		self.rect.y = self.cy - 12
		if self.scene.flyCollision(self.rect):
			self.scene.newEffect(self.cx, self.cy, effect.EffectBlast)
			self.scene.delBullet(self)
			self.isCache = True

	def draw(self, canvas):
		if self.isCache: return
		canvas.blit(self.pics[self.dire], (self.rect.x, self.rect.y))
