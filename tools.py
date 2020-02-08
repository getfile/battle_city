import pygame

bigPic = pygame.image.load("GameMy/resources/Sprites.png")


# 从图像中获取某区域图像, 并缩放到指定尺寸
def getSubPic(rect, scale):
	pic = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
	pic.blit(bigPic, (-rect.x, -rect.y))
	pic = pygame.transform.scale(pic, (int(rect.w * scale), int(rect.h * scale)))
	return pic
