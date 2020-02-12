import os, sys, pygame

from scenegame import *
from level import *
from keymgr import *
from tools import *


def main():
	pygame.mixer.pre_init(22050, -16, 2, 64)
	# print("mixer:", pygame.mixer.get_num_channels())
	pygame.init()

	size = width, height = 24 * 13 * 2, 24 * 13 * 2
	canvas = pygame.display.set_mode(size, flags=pygame.RESIZABLE)
	scene = SceneGame(canvas)
	key = KeyMgr()

	clock = pygame.time.Clock()
	while True:
		clock.tick(60)
		key.update()
		if key.isEscDown():
			break

		TimerMgr.update()

		scene.update()
		scene.draw(canvas)

		pygame.display.flip()

	pygame.mixer.stop()
	print("bye.")


main()
