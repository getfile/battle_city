import sys, pygame


# 按键管理, 包括鼠标
class KeyMgr(object):
	__inst = None
	__init = False

	def __new__(cls):
		if cls.__inst == None:
			cls.__inst = object.__new__(cls)
		return cls.__inst

	def __init__(self):
		if KeyMgr.__init: return
		KeyMgr.__init = True

		self.keys = {}
		self.toggles = {}
		for i in range(300):
			self.keys[i] = False

	def update(self):
		# print(self.keys)
		self.toggles.clear()
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN:
				self.keys[event.key] = True
			if event.type == pygame.KEYUP:
				if self.keys[event.key]: self.toggles[event.key] = True
				self.keys[event.key] = False

	def isEscDown(self):
		return self.keys[27]

	def isBackspace(self):
		return self.toggles.get(8, False)

	# 发射炮弹
	def isKeyJ(self):
		return self.keys[106]

	# 发射炮弹
	def isKeyJnum(self):
		return self.keys[261]

# 第一套方向键

	def isKeyW(self):
		return self.keys[119]

	def isKeyS(self):
		return self.keys[115]

	def isKeyA(self):
		return self.keys[97]

	def isKeyD(self):
		return self.keys[100]


# 第二套方向键

	def isKeyWnum(self):
		return self.keys[264]

	def isKeySnum(self):
		return self.keys[258]

	def isKeyAnum(self):
		return self.keys[260]

	def isKeyDnum(self):
		return self.keys[262]
