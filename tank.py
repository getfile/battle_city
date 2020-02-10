import sys, random, pygame
from enum import Enum

import tools
import keymgr
import effect


# 坦克
# 坦克非移动方向必须对齐到26*26的单元内
class BaseTank:
	pics = None

	def __init__(self, scene):
		if self.pics == None:
			self.pics = [[0 for i in range(2)] for i in range(4)]
			self.pics[0][0] = tools.getSubPic(pygame.Rect(128, 112, 16, 16), 3)
			self.pics[0][1] = tools.getSubPic(pygame.Rect(128 + 16, 112, 16, 16), 3)
			self.pics[1][0] = tools.getSubPic(pygame.Rect(128 + 64, 112, 16, 16), 3)
			self.pics[1][1] = tools.getSubPic(pygame.Rect(128 + 80, 112, 16, 16), 3)
			self.pics[2][0] = tools.getSubPic(pygame.Rect(128 + 32, 112, 16, 16), 3)
			self.pics[2][1] = tools.getSubPic(pygame.Rect(128 + 48, 112, 16, 16), 3)
			self.pics[3][0] = tools.getSubPic(pygame.Rect(128 + 96, 112, 16, 16), 3)
			self.pics[3][1] = tools.getSubPic(pygame.Rect(128 + 112, 112, 16, 16), 3)

		self.scene = scene
		self.colorPic = pygame.Surface((48, 48))
		self.colorPic.set_colorkey(pygame.Color(0, 0, 0))

	def init(self):
		self.id = 0
		self.isCache = False
		self.rect = pygame.Rect(0, 0, 48, 48)
		self.level = 0
		self.color = pygame.Color(0, 255, 0)  #坦克颜色

		self.moving = 0  #是否正在移动
		self.ani = 0  #履带动画状态

		self.dire = 0  #当前方向
		self.speed = 2  #最大移动速度
		self.vx = self.vy = 0  #当前速度
		self.vxNew = self.vyNew = 0  #输入的动力

		self.bulletSpeed = 8  #炮弹速度
		self.bulletNum = 2  #能同时存在的最大炮弹数量
		self.bulletCount = 0  #当前已经发射的炮弹数量
		self.bulletGap = 20  #炮弹发射之间的时间间隔(帧数)
		self.bulletFrame = 0  #当前发射后的倒计时

		self.fireNew = False  #是否开火

	# 炮弹爆炸销毁
	def bulletBomb(self):
		self.bulletCount -= 1

	def draw(self, canvas):
		if self.isCache: return
		if self.moving: self.ani += 1
		else: self.ani = 0
		i = int(self.ani / 3) % 2
		# canvas.blit(self.pics[self.dire][i], (self.rect.x, self.rect.y))
		self.colorPic.fill(pygame.Color(0, 0, 0))
		self.colorPic.blit(self.pics[self.dire][i], (0, 0))
		self.colorPic.fill(self.color, special_flags=pygame.BLEND_MULT)
		canvas.blit(self.colorPic, self.rect.topleft)

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


class TankMe(BaseTank):
	def __init__(self, scene):
		super().__init__(scene)
		self.init()

	def init(self):
		super().init()
		self.level = 3  #等级(吃'星'会提高等级, 等级越高, 威力越大)
		# 				 (0级:单发, 1级:单发加速, 2级:双发加速, 3级:双发加速+消铁)

	# 升级
	def levelUp(self):
		if self.level == 3: return
		self.level += 1
		if self.level == 1: self.bulletSpeed += 2
		if self.level == 2: self.bulletNum += 1

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


class TankState(Enum):
	Cache = 0
	Born = 1
	PreAlive = 2
	Alive = 3
	Die = 4
	Thinking = 5


class TankAi(BaseTank):
	def __init__(self, scene):
		super().__init__(scene)

	def init(self):
		super().init()
		self.color = pygame.Color(100, 100, 100)
		self.level = 1
		self.bulletNum = 1
		self.stateAi = TankState.Born  #缓存, 出生, 生存, 死亡
		self.direAi = 0
		self.distAi = 0
		self._thinking()

	def draw(self, canvas):
		# if self.stateAi.value <= TankState.Born.value: return
		super().draw(canvas)

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
		self.distAi -= 1
		if self.distAi <= 0: self._thinking()
		super().update()
		# print(self.vx, self.vy)

	# 思考
	def _thinking(self):
		self.direAi = random.randint(-1, 3)
		self.distAi = random.randint(2, 100)
		self.fireNew = True if random.random() > 0.5 else False
		# print("ai fire:", self.fireNew)

	def destory(self):
		self.scene.newEffect(self.rect.centerx, self.rect.centery, effect.EffectBomb)
		self.isCache = True
