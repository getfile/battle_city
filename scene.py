import sys, pygame

from level import *
from tank import *
from bullet import *
from effect import *
from ui import *


# 场景: 主界面场景, 游戏场景, 统计场景
class Scene:
	def __init__(self, surf):
		self.level = Level(surf)
		self.level.mapParseJson("GameMy/resources/level/stage-17.json")
		self.level.mapDraw()
		self.tankMe = Tank(self)  #玩家坦克
		self.tankCo = Tank(self)  #协作坦克
		self.tankAIs = []  #敌方坦克集: 兼缓存池用
		self.bullets = []  #炮弹集: 兼缓存池用(包括正使用的和空闲待用的)
		self.effects = []  #效果集 兼缓存池用
		self.ui = UI()

	# 初始化某关卡数值及资源
	def initLevel(self, level):
		pass

	def moveOnSnow(self, rect):
		return self.level.isOnSnow(rect)

	def newTankMe(self, rect):
		pass

	def newTankAI(self):
		pass

	def delTankAI(self, tank):
		pass

	def getTankPos(self):
		return self.tankMe.rect.centerx, self.tankMe.rect.centery

	# 发射炮弹(坦克id, 炮弹坐标, 炮弹方向)
	def newBullet(self, tank, cx, cy):
		bullet = None
		for item in self.bullets:  #寻找空闲的对象
			if item.state == 0:
				bullet = item
				break
		if bullet == None:
			self.bullets.append(Bullet())
			bullet = self.bullets[-1]
		bullet.init(self, tank, cx, cy)
		# print("bullet num:", len(self.bullets))

	# 销毁炮弹(炮弹id, 坦克id)
	def delBullet(self, bullet):
		self.tankMe.bulletBomb()
		self.level.bulletBomb(bullet.level, bullet.rect)

	# 添加效果(效果坐标, 效果类型)
	def newEffect(self, cx, cy, EffectCls):
		effect = None
		for item in self.effects:
			if item.isCache and isinstance(item, EffectCls):
				effect = item
				break
		if effect == None:
			self.effects.append(EffectCls(self))
			effect = self.effects[-1]
		effect.init(cx, cy)
		# print("effect num:", len(self.effects))

	# 删除效果
	def delEffect(self, effect):
		pass

	# 坦克移动碰撞检测, 返回是否有碰撞产生
	def moveCollision(self, rect):
		return self.level.isBlockingMove(rect)

	# 炮弹碰撞检测, 返回是否有碰撞产生
	def flyCollision(self, rect):
		return self.level.isBlockingFly(rect)

	def update(self):
		self.tankMe.update()
		for item in self.bullets:
			item.update()
		for item in self.effects:
			item.update()

	def draw(self, canvas):
		self.level.draw(canvas)
		self.tankMe.draw(canvas)

		for item in self.bullets:
			item.draw(canvas)
		for item in self.effects:
			item.draw(canvas)

		self.level.drawTop(canvas)
		self.ui.drawFrame(canvas)