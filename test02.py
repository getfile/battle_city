try:
	import sys
	import sdfsdf
except BaseException as err:
	print("couldn't load module. %s" % (err))
	sys.exit(2)

try:
	fh = open("GameMy/test02.py", "r")
	fh.read()
except BaseException:
	print("产生错误")
except IOError:
	print("Error: 没有找到文件或读取文件失败")
except UnicodeDecodeError:
	print("Error: 编码错误")
else:
	print("文件打开成功")
	fh.close()
