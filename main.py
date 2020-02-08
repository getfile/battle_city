import os, sys, pygame

from scene import *
from level import *
from keymgr import *


def main():
	pygame.mixer.pre_init(22050, -16, 2, 64)
	# print("mixer:", pygame.mixer.get_num_channels())
	pygame.init()

	size = width, height = 24 * 13 * 2, 24 * 13 * 2
	canvas = pygame.display.set_mode(size, flags=pygame.RESIZABLE)
	scene = Scene(canvas)
	key = KeyMgr()

	clock = pygame.time.Clock()
	while True:
		clock.tick(60)

		key.update()
		if key.isEscDown():
			break

		scene.update()
		scene.draw(canvas)

		pygame.display.flip()

	pygame.mixer.stop()
	print("bye.")


main()
