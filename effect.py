import os, sys, pygame

import tools


# 效果基类
class Effect:
	pics = None

	# 初始化实例对象
	def __init__(self, scene):
		self.frames = []  #播放动画集
		self.frameGap = 3  #每帧显示次数
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

	def destory(self):
		self.isCache = True


# 坦克出生效果
class EffectBorn(Effect):
	def __init__(self, scene):
		super().__init__(scene)
		self.frames = [1, 1, 2, 3, 4, 4, 3, 2, 1, 1, 2, 3, 4, 4, 3, 2, 1, 1, 2, 3, 4, 4, 3, 2, 1, 1]

	def update(self):
		super().update()


# 爆炸效果(坦克,堡垒))
class EffectBomb(Effect):
	def __init__(self, scene):
		super().__init__(scene)
		self.frames = [7, 9, 11, 11, 10, 9, 9, 8, 7]
		sound = pygame.mixer.Sound("resources/sound/explosion_1.ogg")
		sound.play()

	def update(self):
		super().update()


# 无敌效果
class EffectArmor(Effect):
	def __init__(self, scene):
		super().__init__(scene)
		self.frames = [5, 6]

	def init(self, cx, cy, callback):
		self.isCache = False  #是否空闲对象
		self.delay = 600
		self.playIdx = 0
		self.cx = self.cy = 0
		self.callback = None
		self.scene.tankMe.setGod(True)

	def update(self):
		if self.isCache: return
		self.cx, self.cy = self.scene.getTankPos()
		self.playIdx += 1
		if self.playIdx >= len(self.frames) * self.frameGap: self.playIdx = 0
		self.delay -= 1
		if self.delay > 0: return

		self.isCache = True
		if self.callback: self.callback()
		self.scene.delEffect(self)
		self.scene.tankMe.setGod(False)


# 爆炸效果(子弹)
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

	def init(self, cx, cy, callback=None):
		self.isCache = False
		self.scene.level.setFortBlock(True)
		self.delay = 600

	def update(self):
		if self.isCache: return
		self.delay -= 1
		if self.delay > 0: return

		self.scene.level.setFortBlock(False)
		self.isCache = True

	def draw(self, canvas):
		pass


# 冻结ai坦克效果(一定时间内所有坦克都会被冻结)
class EffectFreeze(Effect):
	def init(self, cx, cy, callback=None):
		self.isCache = False
		self.delay = 600
		for item in self.scene.tankAIs:
			item.isFreeze = True

	def update(self):
		if self.isCache: return
		self.delay -= 1
		if self.delay > 0: return

		for item in self.scene.tankAIs:
			item.isFreeze = False
		self.isCache = True

	def draw(self, canvas):
		pass