import sys, random, pygame
from enum import Enum

import tools
import keymgr
import effect
import scenegame


# 坦克
# 坦克非移动方向必须对齐到26*26的单元内
class BaseTank:
	pics = None

	def __init__(self, scene):
		if self.pics == None:
			self.pics = [[[0 for i in range(2)] for i in range(4)] for i in range(8)]
			for a in range(8):
				for b in range(4):
					dir = b
					if b == 1 or b == 2: dir = 3 - b
					self.pics[a][dir][0] = tools.getSubPic(pygame.Rect(128 + b * 32, a * 16, 16, 16), 3)
					self.pics[a][dir][1] = tools.getSubPic(pygame.Rect(128 + b * 32 + 16, a * 16, 16, 16), 3)

		self.scene = scene
		self.colorPic = pygame.Surface((48, 48))
		self.colorPic.set_colorkey(pygame.Color(0, 0, 0))

	def init(self):
		self.id = 0
		self.isCache = False
		self.rect = pygame.Rect(0, 0, 48, 48)
		self.level = 0
		self.hp = 1  #生命值
		self.color = pygame.Color(0, 255, 0)  #坦克颜色

		self.moving = 0  #是否正在移动
		self.ani = 0  #履带动画状态

		self.dire = 0  #当前方向
		self.speed = 2  #最大移动速度
		self.vx = self.vy = 0  #当前速度
		self.vxNew = self.vyNew = 0  #输入的动力

		self.bulletSpeed = 8  #炮弹速度
		self.bulletNum = 1  #能同时存在的最大炮弹数量
		self.bulletCount = 0  #当前已经发射的炮弹数量
		self.bulletGap = 20  #炮弹发射之间的时间间隔(帧数)
		self.bulletFrame = 0  #当前发射后的倒计时

		self.fireNew = False  #是否开火

	# 炮弹爆炸销毁
	def bulletBomb(self):
		self.bulletCount -= 1

	# 计算输入(用户, ai, 网络)
	def _input(self):
		pass

	# 计算地形对速度的影响
	def _updateTerrain(self):
		if self.scene.moveOnSnow(self.rect):
			self.vx *= 0.95
			self.vy *= 0.95
		else:
			self.vx = self.vy = 0

	# 计算动力对速度的影响
	def _updatePower(self):
		self.vx += self.vxNew
		self.vy += self.vyNew

	# 计算约束
	def _updateBound(self):
		# 速度约束
		maxspeed = self.speed
		if self.scene.moveOnSnow(self.rect):
			maxspeed = self.speed * 0.8
		self.vx = min(max(self.vx, -maxspeed), maxspeed)
		self.vy = min(max(self.vy, -maxspeed), maxspeed)

		oldx = self.rect.x
		oldy = self.rect.y
		self.rect.x += int(self.vx)
		self.rect.y += int(self.vy)

		# 转向约束
		if int(self.dire / 2) == 0: oldx = self.rect.x = round(self.rect.x / 24) * 24
		else: oldy = self.rect.y = round(self.rect.y / 24) * 24
		# 障碍约束
		if self.scene.moveCollision(self):
			self.rect.x = oldx
			self.rect.y = oldy

	# 计算炮弹的发射
	def _updateBullet(self):
		self.bulletFrame += 1
		if self.bulletFrame < self.bulletGap: return
		if self.bulletCount == self.bulletNum: return
		if not self.fireNew: return
		cx = cy = 0
		if self.dire == 0:
			cx = self.rect.centerx
			cy = self.rect.top
		elif self.dire == 1:
			cx = self.rect.centerx
			cy = self.rect.bottom
		elif self.dire == 2:
			cx = self.rect.left
			cy = self.rect.centery
		else:
			cx = self.rect.right
			cy = self.rect.centery
		self.scene.newBullet(self, cx, cy)
		# self.scene.newEffect(self.rect.centerx, self.rect.centery, effect.EffectBomb)
		self.bulletCount += 1
		self.bulletFrame = 0

	def update(self):
		self._input()
		self._updateTerrain()
		self._updatePower()
		self._updateBound()
		self._updateBullet()

	def draw(self, canvas):
		if self.isCache: return
		if self.moving: self.ani += 1
		else: self.ani = 0
		i = int(self.ani / 3) % 2
		# canvas.blit(self.pics[self.dire][i], (self.rect.x, self.rect.y))
		self.colorPic.fill(pygame.Color(0, 0, 0))
		self.colorPic.blit(self.pics[self.level][self.dire][i], (0, 0))
		self.colorPic.fill(self.color, special_flags=pygame.BLEND_MULT)
		canvas.blit(self.colorPic, self.rect.topleft)

	def destory(self):
		pass


class TankEmpty(BaseTank):
	def __init__(self, scene):
		self.init()
		self.isGod = False
		pass

	def update(self):
		pass

	def draw(self, canvas):
		pass


class TankMe(BaseTank):
	def __init__(self, scene):
		super().__init__(scene)
		self.init(0, 0)

	def init(self, px, py):
		super().init()
		self.level = 0  #等级(吃'星'会提高等级, 等级越高, 威力越大)
		# 				 (0级:单发, 1级:单发加速, 2级:双发加速, 3级:双发加速+消铁)
		self.rect.x = px
		self.rect.y = py
		self.dire = 0

		self.isGod = False  #是否盔甲保护

	# 升级
	def levelUp(self):
		if self.level == 3: return
		self.level += 1
		if self.level == 1: self.bulletSpeed += 2
		if self.level == 2: self.bulletNum += 1

	def setGod(self, result):
		self.isGod = result

	def _input(self):
		self.moving = True
		if keymgr.KeyMgr().isKeyW() or keymgr.KeyMgr().isKeyWnum():
			self.dire = 0
			self.vxNew = 0
			self.vyNew = -self.speed
		elif keymgr.KeyMgr().isKeyS() or keymgr.KeyMgr().isKeySnum():
			self.dire = 1
			self.vxNew = 0
			self.vyNew = self.speed
		elif keymgr.KeyMgr().isKeyA() or keymgr.KeyMgr().isKeyAnum():
			self.dire = 2
			self.vxNew = -self.speed
			self.vyNew = 0
		elif keymgr.KeyMgr().isKeyD() or keymgr.KeyMgr().isKeyDnum():
			self.dire = 3
			self.vxNew = self.speed
			self.vyNew = 0
		else:
			self.vxNew = self.vyNew = 0
			self.moving = False

		self.fireNew = (keymgr.KeyMgr().isKeyJ() or keymgr.KeyMgr().isKeyJnum())

	def update(self):
		if self.isCache: return
		super().update()

	def destory(self):
		self.scene.newEffect(self.rect.centerx, self.rect.centery, effect.EffectBomb)
		self.isCache = True
		scenegame.TankBorn(self.scene, True)


class TankAi(BaseTank):
	def __init__(self, scene):
		super().__init__(scene)
		self.isFreeze = False  #是否被冻结

	# 等级和起点坐标(左上角像素坐标)
	def init(self, level=0, px=0, py=0):
		super().init()
		c = level * 63
		self.color = pygame.Color(c, 255, 255 - c)
		self.level = level + 4  #0basic, 1fast, 2power, 3armor
		# 						Basic	#普通坦克(100, 1, slow1, slow6)
		# 						Fast	#快速坦克(200, 1, fast3, normal8)
		# 						Power	#火力坦克(300, 1, normal2, fast10)
		# 						Armor	#重甲坦克(400, 4, normal2, normal8)
		if level == 0:
			self.speed = 2
			self.bulletSpeed = 6
		if level == 1: self.speed = 4
		if level == 2: self.bulletSpeed = 10
		if level == 3: self.hp = 4
		self.bulletNum = 1
		self.direAi = 0
		self.distAi = 0
		self.rect.x = px
		self.rect.y = py
		self.dire = 1
		self._thinking()

	def _input(self):
		self.moving = True
		if self.direAi == 0:
			self.dire = 0
			self.vxNew = 0
			self.vyNew = -self.speed
		elif self.direAi == 1:
			self.dire = 1
			self.vxNew = 0
			self.vyNew = self.speed
		elif self.direAi == 2:
			self.dire = 2
			self.vxNew = -self.speed
			self.vyNew = 0
		elif self.direAi == 3:
			self.dire = 3
			self.vxNew = self.speed
			self.vyNew = 0
		else:
			self.vxNew = self.vyNew = 0
			self.moving = False

	def update(self):
		if self.isCache: return
		if self.isFreeze: return
		self.distAi -= 1
		if self.distAi <= 0: self._thinking()
		super().update()

	# 思考
	def _thinking(self):
		if random.random() > 0.6: self.direAi = 1
		else: self.direAi = random.randint(-1, 3)

		self.distAi = random.randint(12, 50)
		self.fireNew = True if random.random() > 0.5 else False

	# 被击毁
	def destory(self):
		self.scene.newEffect(self.rect.centerx, self.rect.centery, effect.EffectBomb)
		self.isCache = True
		scenegame.TankBorn(self.scene, False)
