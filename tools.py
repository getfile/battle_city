import pygame

bigPic = pygame.image.load("resources/Sprites.png")


# 可缓存对象
class Cacheable:
	def __init__(self):
		self.isCache = False  #是否是缓存对象


# 定时器
class Timer:
	# time为帧数,60帧为1秒
	def init(self, callback, time=60, loop=1):
		self.isCache = False
		self.tickv = time
		self.tick = time
		self.loop = loop
		self.callback = callback

	def update(self):
		if self.isCache: return

		self.tick -= 1
		if self.tick > 0: return
		if self.callback: self.callback()

		self.loop -= 1
		self.tick = self.tickv
		if self.loop > 0: return

		self.isCache = True


class TimerMgr:
	timers = []
	isPause = False

	@classmethod
	def clearTimer(cls):
		cls.timers.clear()

	@classmethod
	def pause(cls):
		cls.isPause = True

	@classmethod
	def resume(cls):
		cls.isPause = False

	@classmethod
	def newTimer(cls, callback, time=60, loop=1):
		timer = None
		for item in cls.timers:
			if item.isCache:
				timer = item
				break
		if timer == None:
			timer = Timer()
			cls.timers.append(timer)
		timer.init(callback, time, loop)

	@classmethod
	def update(cls):
		if cls.isPause: return
		for item in cls.timers:
			if item.isCache: continue
			item.update()
		# print("timers num:", len(cls.timers))


# 从图像中获取某区域透明图像, 并缩放到指定尺寸
def getSubPic(rect, scale):
	pic = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
	pic.blit(bigPic, (-rect.x, -rect.y))
	pic = pygame.transform.scale(pic, (int(rect.w * scale), int(rect.h * scale)))
	return pic


# 透明图像转换成colorkey图像
def getPicByColorkey(pic, rect, ckey):
	newpic = pygame.Surface((rect.w, rect.h))
	newpic.blit(pic, rect.topleft)
	newpic.set_colorkey(ckey)
	return newpic