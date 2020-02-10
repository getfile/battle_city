import os, sys, pygame

import tools


# 效果基类
class Effect:
	pics = None

	# 初始化实例对象
	def __init__(self, scene):
		self.frames = []  #播放动画集
		self.frameGap = 3
		self.scene = scene

		if self.pics == None:
			self.pics = []
			self.pics.append(tools.getSubPic(pygame.Rect(256, 88, 8, 8), 6))  #黑块0
			self.pics.append(tools.getSubPic(pygame.Rect(256, 96, 16, 16), 3))  #星光1
			self.pics.append(tools.getSubPic(pygame.Rect(272, 96, 16, 16), 3))
			self.pics.append(tools.getSubPic(pygame.Rect(288, 96, 16, 16), 3))
			self.pics.append(tools.getSubPic(pygame.Rect(304, 96, 16, 16), 3))
			self.pics.append(tools.getSubPic(pygame.Rect(256, 144, 16, 16), 3))  #电弧5
			self.pics.append(tools.getSubPic(pygame.Rect(272, 144, 16, 16), 3))
			self.pics.append(tools.getSubPic(pygame.Rect(256, 128, 16, 16), 3))  #爆炸7
			self.pics.append(tools.getSubPic(pygame.Rect(272, 128, 16, 16), 3))
			self.pics.append(tools.getSubPic(pygame.Rect(288, 128, 16, 16), 3))
			self.pics.append(tools.getSubPic(pygame.Rect(304, 128, 32, 32), 3))  #大爆炸10
			self.pics.append(tools.getSubPic(pygame.Rect(336, 128, 32, 32), 3))

	# 初始化cache对象(特效中心坐标, 效果结束后的回调)
	def init(self, cx, cy, callback=None):
		self.callback = callback
		self.isCache = False  #是否空闲对象
		self.playIdx = 0
		self.cx = cx  #图像中心位置
		self.cy = cy
		# self.frames = [7, 9, 8, 7]

	def update(self):
		if self.isCache: return
		self.playIdx += 1
		if self.playIdx >= len(self.frames) * self.frameGap:
			self.scene.delEffect(self)
			self.isCache = True
			if self.callback: self.callback()

	def draw(self, canvas):
		if self.isCache: return
		idx = int(self.playIdx / self.frameGap)
		idx = self.frames[idx]
		rect = self.pics[idx].get_rect()
		rect.centerx = self.cx
		rect.centery = self.cy
		canvas.blit(self.pics[idx], (rect.x, rect.y))


# ai坦克出生效果
class EffectBorn(Effect):
	def __init__(self, scene):
		super().__init__(scene)
		self.frames = [1, 1, 2, 3, 4, 4, 3, 2, 1, 1, 2, 3, 4, 4, 3, 2, 1, 1, 2, 3, 4, 4, 3, 2, 1, 1]

	def update(self):
		super().update()
		# self.cx, self.cy = self.scene.getTankPos()


# 爆炸效果(坦克爆炸))
class EffectBomb(Effect):
	def __init__(self, scene):
		super().__init__(scene)
		self.frames = [7, 9, 11, 11, 10, 9, 9, 8, 7]
		sound = pygame.mixer.Sound("resources/sound/explosion_1.ogg")
		sound.play()

	def update(self):
		super().update()
		# self.cx, self.cy = self.scene.getTankPos()


# 无敌效果
class EffectArmor(Effect):
	def __init__(self, scene):
		super().__init__(scene)
		self.frames = [5, 6, 5, 6, 5, 6, 5, 6]

	def update(self):
		super().update()
		self.cx, self.cy = self.scene.getTankPos()


# 爆炸效果(子弹爆炸)
class EffectBlast(Effect):
	def __init__(self, scene):
		super().__init__(scene)
		self.frames = [7, 9, 8, 7]
		sound = pygame.mixer.Sound("resources/sound/explosion_2.ogg")
		sound.play()


# 堡垒效果(保护大本营)
class EffectFort(Effect):
	def __init__(self, scene):
		super().__init__(scene)
