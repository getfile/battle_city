import os, sys, pygame


class UI:
	def __init__(self):
		self.font = pygame.font.Font("resources/namco.ttf", 10)
		self.frame = 0

	def drawFrame(self, canvas, left, died):
		self.frame += 1
		# text = self.font.render("frame:" + str(self.frame), True, (255, 255, 0))
		# text = self.font.render("PLAYER STAGE LIST GALLERY\n 1980", True, (255, 255, 0))
		text = self.font.render(str(left) + " : " + str(died), True, (255, 0, 0))
		textRect = text.get_rect()
		textRect.topright = [620, 5]
		canvas.blit(text, textRect)
