import sys, pygame

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
		self.state = 0  #0缓存, 出生, 生存, 死亡
		self.id = 0
		self.rect = pygame.Rect(0, 0, 48, 48)
		self.color = pygame.Color(0, 255, 0)  #坦克颜色

		self.onSnow = False
		self.px = self.py = 0  #左上角坐标
		self.dire = 0  #当前方向
		self.speed = 2  #移动速度

		self.moving = 0  #是否正在移动
		self.ani = 0  #履带动画状态

		self.bulletSpeed = 8  #炮弹速度
		self.bulletNum = 2  #能同时存在的最大炮弹数量
		self.bulletCount = 0  #当前已经发射的炮弹数量

	def draw(self, canvas):
		if self.moving: self.ani += 1
		else: self.ani = 0
		i = int(self.ani / 3) % 2
		# canvas.blit(self.pics[self.dire][i], (self.rect.x, self.rect.y))
		self.colorPic.fill(pygame.Color(0, 0, 0))
		self.colorPic.blit(self.pics[self.dire][i], (0, 0))
		self.colorPic.fill(self.color, special_flags=pygame.BLEND_MULT)
		canvas.blit(self.colorPic, self.rect.topleft)


class Tank(BaseTank):
	def __init__(self, scene):
		super().__init__(scene)
		self.init()

	def init(self):
		super().init()
		self.level = 3  #等级(吃'星'会提高等级, 等级越高, 威力越大)
		# 				 (0级:单发, 1级:单发加速, 2级:双发加速, 3级:双发加速+消铁)
		self.bulletGap = 20  #炮弹发射之间的时间间隔(帧数)
		self.bulletFrame = 0  #当前发射后的时间计数

	# 升级
	def levelUp(self):
		if self.level == 3: return
		self.level += 1
		if self.level == 1: self.bulletSpeed += 2
		if self.level == 2: self.bulletNum += 1

	# 炮弹爆炸销毁
	def bulletBomb(self):
		self.bulletCount -= 1

	# 发射炮弹
	def updateFire(self):
		self.bulletFrame += 1
		if self.bulletCount == self.bulletNum: return
		if self.bulletFrame < self.bulletGap: return
		if not (keymgr.KeyMgr().isKeyJ() or keymgr.KeyMgr().isKeyJnum()): return
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

	# 移动坦克
	def update(self):
		if self.onSnow:
			self.px = self.px * 0.96  #打滑系数
			self.py = self.py * 0.96
		else:
			self.px = self.py = 0

		# print(self.px, self.py)

		newDire = self.dire
		self.moving = 1
		if keymgr.KeyMgr().isKeyW() or keymgr.KeyMgr().isKeyWnum():
			newDire = 0
			self.px = 0
			self.py = -self.speed
		elif keymgr.KeyMgr().isKeyS() or keymgr.KeyMgr().isKeySnum():
			newDire = 1
			self.px = 0
			self.py = self.speed
		elif keymgr.KeyMgr().isKeyA() or keymgr.KeyMgr().isKeyAnum():
			newDire = 2
			self.py = 0
			self.px = -self.speed
		elif keymgr.KeyMgr().isKeyD() or keymgr.KeyMgr().isKeyDnum():
			newDire = 3
			self.py = 0
			self.px = self.speed
		else:
			self.moving = 0

		oldx = self.rect.x
		oldy = self.rect.y
		if self.scene.moveOnSnow(self.rect):  #在雪地上
			if self.moving:
				self.rect.x += int(self.px * 0.5)  #减速效果
				self.rect.y += int(self.py * 0.5)
			else:
				self.rect.x += int(self.px)  #打滑效果
				self.rect.y += int(self.py)
			self.onSnow = True
		else:
			self.rect.x += self.px
			self.rect.y += self.py
			self.onSnow = False

		if int(newDire / 2) != int(self.dire / 2):  # 如果有转向, 校准转向位置
			if int(newDire / 2) == 0: self.rect.x = round(self.rect.x / 24) * 24
			else: self.rect.y = round(self.rect.y / 24) * 24
		elif self.scene.moveCollision(self.rect):  #碰到障碍
			self.rect.x = oldx
			self.rect.y = oldy

		self.dire = newDire
		self.updateFire()

	# # 移动坦克
	# def update(self):
	# 	self.moving = 1
	# 	self.px = self.py = 0
	# 	newDire = self.dire
	# 	if keymgr.KeyMgr().isKeyW() or keymgr.KeyMgr().isKeyWnum():
	# 		newDire = 0
	# 		self.py = -self.speed
	# 	elif keymgr.KeyMgr().isKeyS() or keymgr.KeyMgr().isKeySnum():
	# 		newDire = 1
	# 		self.py = self.speed
	# 	elif keymgr.KeyMgr().isKeyA() or keymgr.KeyMgr().isKeyAnum():
	# 		newDire = 2
	# 		self.px = -self.speed
	# 	elif keymgr.KeyMgr().isKeyD() or keymgr.KeyMgr().isKeyDnum():
	# 		newDire = 3
	# 		self.px = self.speed
	# 	else:
	# 		self.moving = 0

	# 	# 如果有转向, 校准转向位置
	# 	if int(newDire / 2) != int(self.dire / 2):
	# 		if int(newDire / 2) == 0: self.rect.x = round(self.rect.x / 24) * 24
	# 		else: self.rect.y = round(self.rect.y / 24) * 24
	# 	else:
	# 		self.rect.x += self.px
	# 		self.rect.y += self.py
	# 		if self.scene.moveCollision(self.rect):  #碰到障碍
	# 			self.rect.x -= self.px
	# 			self.rect.y -= self.py

	# 	self.dire = newDire
	# 	self.updateFire()
