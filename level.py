import os, sys, json, pygame

import tools


# 奖励
class Bouns:
	def __init__(self):
		pass


# 地图元素: 0空地, 1砖墙(16*16), 2河流, 3雪地, 4树林, 5铁墙(4*4), 6堡垒
# 每个元素能分解成16个小元素
class Item:
	def __init__(self):
		self.id = 0


# 关卡
# 由13*13个大元素组成
class Level:
	def __init__(self, surf):
		self.bound = surf.get_rect()
		self.background = surf.copy()
		self.treeGround = surf.copy()
		self.treeGround.set_colorkey(pygame.Color(0, 0, 0))
		self.col = 26  # 小元素的数量(x方向)
		self.row = 26
		self.map = []  #关卡元素集
		self.map = [[0 for i in range(self.col)] for i in range(self.row)]
		self.itemIds = {'X': 0, 'B': 1, 'R': 2, 'S': 3, 'F': 4, 'T': 5, 'E': 6}  #json中元素字符 映射为id
		self.itemPic = []  #元素图例集
		self.itemWid = 24
		self.itemHei = 24
		self._initRes()

	def _initRes(self):
		self.itemPic.append(tools.getSubPic(pygame.Rect(280, 72, 8, 8), 3))  #空地
		self.itemPic.append(tools.getSubPic(pygame.Rect(256, 64, 8, 8), 3))  #砖块
		self.itemPic.append(tools.getSubPic(pygame.Rect(264, 80, 8, 8), 3))  #河流
		self.itemPic.append(tools.getSubPic(pygame.Rect(272, 72, 8, 8), 3))  #雪地
		self.itemPic.append(tools.getSubPic(pygame.Rect(264, 72, 8, 8), 3))  #森林
		self.itemPic.append(tools.getSubPic(pygame.Rect(256, 72, 8, 8), 3))  #钢块
		self.itemPic.append(tools.getSubPic(pygame.Rect(304, 32, 16, 16), 3))  #堡垒
		self.itemPic.append(tools.getSubPic(pygame.Rect(272, 80, 8, 8), 3))  #河流2(河流动画用)

	def isOnSnow(self, rect):
		if not self.bound.contains(rect): return False
		l = int(rect.left / 24)
		t = int(rect.top / 24)
		r = int((rect.right - 1) / 24)
		b = int((rect.bottom - 1) / 24)
		all = 0
		if self.map[l][t] == 3: all += 1
		if self.map[l][b] == 3: all += 1
		if self.map[r][t] == 3: all += 1
		if self.map[r][b] == 3: all += 1
		return all > 2

	# 解析关卡文件(json格式)
	# 坦克类型: basic| fast| power| armor
	# 地形类型: 空地0 X| 砖块1 B<n>| 河流2 R| 雪地3 S| 森林4 F| 钢块5 T<n>| 堡垒6 E
	def mapParseJson(self, jsonFile):
		f = open(jsonFile, 'rb')
		txt = f.read()
		f.close()
		j = json.loads(txt)
		mapData = j['map']
		x, y = 0, 0
		for line in mapData:
			for i in range(0, 39, 3):
				item = line[i:i + 3]
				self._fillItems(x, y, item)
				x += 1
			x = 0
			y += 1
		# print(self.map)

	def _fillItems(self, x, y, item):
		x *= 2
		y *= 2
		itemId = self.itemIds[(item[0])]
		if item[0] == 'B' or item[0] == 'T':
			itemPattern = int(item[1], 16)
			self.map[x][y] = itemId * (1 if itemPattern & 0b1 else 0)
			self.map[x + 1][y] = itemId * (1 if itemPattern >> 1 & 0b1 else 0)
			self.map[x][y + 1] = itemId * (1 if itemPattern >> 2 & 0b1 else 0)
			self.map[x + 1][y + 1] = itemId * (1 if itemPattern >> 3 & 0b1 else 0)
		else:
			self.map[x][y] = self.map[x + 1][y] = self.map[x][y + 1] = self.map[x + 1][y + 1] = itemId

	def mapDraw(self):
		for x in range(0, 26):
			for y in range(0, 26):
				id = self.map[x][y]
				if id == 6: continue
				if id == 4: self.treeGround.blit(self.itemPic[id], (x * self.itemWid, y * self.itemHei))
				else: self.background.blit(self.itemPic[id], (x * self.itemWid, y * self.itemHei))
		self.background.blit(self.itemPic[6], (12 * self.itemWid, 24 * self.itemHei))

	# 销毁障碍
	def _killBlock(self, level, xx, yy):
		id = self.map[xx][yy]
		if id == 1 or (id == 5 and level == 3):
			self.map[xx][yy] = 0
			self.background.blit(self.itemPic[0], (xx * self.itemWid, yy * self.itemHei))

	# 子弹爆炸时,是否有障碍要销毁
	def bulletBomb(self, level, rect):
		if not self.bound.contains(rect): return
		l = int(rect.left / 24)
		t = int(rect.top / 24)
		r = int((rect.right - 1) / 24)
		b = int((rect.bottom - 1) / 24)
		self._killBlock(level, l, t)
		self._killBlock(level, l, b)
		self._killBlock(level, r, t)
		self._killBlock(level, r, b)

	# 指定的块是否是障碍
	def _isFlyBlock(self, xx, yy):
		id = self.map[xx][yy]
		return (id == 1 or id == 5 or id == 6)

	# 飞越时指定的矩形是否碰到障碍
	def isBlockingFly(self, rect):
		if not self.bound.contains(rect): return True
		x = int(rect.x / 24)
		y = int(rect.y / 24)
		r = int((rect.right - 1) / 24)
		b = int((rect.bottom - 1) / 24)
		if self._isFlyBlock(x, y): return True
		elif self._isFlyBlock(r, y): return True
		elif self._isFlyBlock(x, b): return True
		elif self._isFlyBlock(r, b): return True
		return False

	# 指定的块是否是障碍
	def _isMoveBlock(self, xx, yy):
		id = self.map[xx][yy]
		return (id == 1 or id == 2 or id == 5 or id == 6)

	# 移动时指定的矩形是否碰到障碍
	def isBlockingMove(self, rect):
		if not self.bound.contains(rect): return True
		x = int(rect.x / 24)
		y = int(rect.y / 24)
		r = int((rect.right - 1) / 24)
		b = int((rect.bottom - 1) / 24)
		if self._isMoveBlock(x, y): return True
		elif self._isMoveBlock(r, y): return True
		elif self._isMoveBlock(x, b): return True
		elif self._isMoveBlock(r, b): return True
		return False

	# 绘制遮挡坦克的对象(可优化)
	def drawTop(self, canvas):
		canvas.blit(self.treeGround, (0, 0))

	def draw(self, canvas):
		canvas.blit(self.background, (0, 0))
