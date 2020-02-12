import sys, pygame

from level import *
from tank import *
from bullet import *
from effect import *
from ui import *
from tools import *


class TankBorn:
	def __init__(self, scene, isMe=False):
		self.scene = scene
		self.isMe = isMe

		self.level, self.px, self.py = self.scene.level.bornTank(isMe)
		if self.level is None: return

		self.scene.newEffect(self.px + 24, self.py + 24, EffectBorn, self.born)
		# TimerMgr.newTimer(self.born)

	def born(self):
		if self.isMe:
			self.scene.newTankMe(self.px, self.py)
		else:
			self.scene.newTankAI(self.level, self.px, self.py)


# 游戏界面
class SceneGame:
	def __init__(self, surf):
		self.level = Level(surf)
		self.level.mapLoad(31)  # 1-35
		self.level.mapDraw()
		self.tankMe = TankEmpty(self)
		self.tankAIs = []  #敌方坦克集: 兼缓存池用
		self.bullets = []  #炮弹集: 兼缓存池用(包括正使用的和空闲待用的)
		self.effects = []  #效果集 兼缓存池用
		self.ui = UI()

		self.levelStart()
		# self.levelTest()

	def levelTest(self):
		self.tankMe = TankMe(self)  #玩家坦克
		self.tankCo = TankMe(self)  #协作坦克
		for i in range(12):
			tankAi = TankAi(self)
			tankAi.init(random.randint(0, 3))
			tankAi.rect.topleft = (i * 48 + 48, 0)
			self.tankAIs.append(tankAi)
		pass

	# 初始化某关卡数值及资源
	def levelStart(self):
		TankBorn(self, True)
		TankBorn(self, False)
		TankBorn(self, False)
		TankBorn(self, False)

	def moveOnSnow(self, rect):
		return self.level.isOnSnow(rect)

	# ME坦克重生
	def newTankMe(self, px, py):
		self.tankMe = TankMe(self)
		self.tankMe.init(px, py)
		print("first")

	# AI坦克重生
	def newTankAI(self, level, px, py):
		tank = None
		for item in self.tankAIs:
			if item.isCache:
				tank = item
				break
		if tank is None:
			tank = TankAi(self)
			self.tankAIs.append(tank)
		tank.init(level, px, py)

	def delTankAI(self, tank):
		pass

	# 获取玩家坦克的位置
	def getTankPos(self):
		return self.tankMe.rect.centerx, self.tankMe.rect.centery

	# 发射炮弹(坦克id, 炮弹坐标, 炮弹方向)
	def newBullet(self, tank, cx, cy):
		bullet = None
		for item in self.bullets:  #寻找空闲的对象
			if item.isCache:
				bullet = item
				break
		if bullet == None:
			self.bullets.append(Bullet())
			bullet = self.bullets[-1]
		bullet.init(self, tank, cx, cy)
		# print("bullet num:", len(self.bullets))

	# 销毁炮弹(炮弹id, 坦克id)
	def delBullet(self, bullet):
		if not bullet.tank.isCache: bullet.tank.bulletBomb()
		self.level.bulletBomb(bullet.level, bullet.rect)

	# 添加效果(效果中心坐标, 效果类型)
	def newEffect(self, cx, cy, EffectCls, callback=None):
		effect = None
		for item in self.effects:
			if item.isCache and isinstance(item, EffectCls):
				effect = item
				break
		if effect == None:
			self.effects.append(EffectCls(self))
			effect = self.effects[-1]
		effect.init(cx, cy, callback)
		# print("effect num:", len(self.effects))

	# 删除效果
	def delEffect(self, effect):
		pass

	# 坦克移动碰撞检测, 返回是否有碰撞产生
	def moveCollision(self, tank):
		if self.level.isBlockingMove(tank.rect): return True
		for t in self.tankAIs:
			if t.isCache: continue
			if tank == t: continue
			if tank.rect.colliderect(t.rect): return True
		if tank == self.tankMe: return False
		if tank.rect.colliderect(self.tankMe.rect): return True
		return False

	# 炮弹碰撞检测, 返回是否有碰撞产生
	def flyCollision(self, bullet):
		if self.level.isBlockingFly(bullet.rectTest):
			return True
		for b in self.bullets:
			if b.isCache: continue
			if bullet is b: continue
			if bullet.rectTest.colliderect(b.rectTest):
				b.destory()
				return True
		for t in self.tankAIs:
			if t.isCache: continue
			if bullet.tank is t: continue
			if type(bullet.tank) == type(t): continue
			if bullet.rectTest.colliderect(t.rect):
				t.destory()
				return True

		if type(bullet.tank) == TankAi:
			if self.tankMe.isCache: return False
			if bullet.rectTest.colliderect(self.tankMe.rect):
				self.tankMe.destory()
				return True

		return False

	def update(self):
		self.tankMe.update()

		for item in self.tankAIs:
			item.update()
		for item in self.bullets:
			item.update()
		for item in self.effects:
			item.update()

	def draw(self, canvas):
		self.level.draw(canvas)
		self.tankMe.draw(canvas)

		for item in self.tankAIs:
			item.draw(canvas)
		for item in self.bullets:
			item.draw(canvas)
		for item in self.effects:
			item.draw(canvas)

		self.level.drawTop(canvas)
		self.ui.drawFrame(canvas)