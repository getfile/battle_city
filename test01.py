import math
from enum import Enum, unique

l = []
for i in range(1, 101, 2):
	l.append(i)
print(l)

l = [math.sqrt(i) for i in range(1, 101, 2)]

# print(l)


# @unique
class TankState(Enum):
	PreAlive = 1
	Alive = 2
	Die = 1


print(TankState.Alive)
print(TankState.Alive.name)
print(TankState.Alive.value)
print([i.name for i in TankState])
