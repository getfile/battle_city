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

	def update(self):
		# print(self.keys)
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYUP: self.keys[event.key] = False
			if event.type == pygame.KEYDOWN: self.keys[event.key] = True

	def isEscDown(self):
		if 27 not in self.keys: return False
		return self.keys[27]

	# 发射炮弹
	def isKeyJ(self):
		if 106 not in self.keys: return False
		return self.keys[106]

	# 发射炮弹
	def isKeyJnum(self):
		if 261 not in self.keys: return False
		return self.keys[261]

# 第一套方向键

	def isKeyW(self):
		if 119 not in self.keys: return False
		return self.keys[119]

	def isKeyS(self):
		if 115 not in self.keys: return False
		return self.keys[115]

	def isKeyA(self):
		if 97 not in self.keys: return False
		return self.keys[97]

	def isKeyD(self):
		if 100 not in self.keys: return False
		return self.keys[100]


# 第二套方向键

	def isKeyWnum(self):
		if 264 not in self.keys: return False
		return self.keys[264]

	def isKeySnum(self):
		if 258 not in self.keys: return False
		return self.keys[258]

	def isKeyAnum(self):
		if 260 not in self.keys: return False
		return self.keys[260]

	def isKeyDnum(self):
		if 262 not in self.keys: return False
		return self.keys[262]
