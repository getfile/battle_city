import sys
import clang.cindex
from clang.cindex import Config
Config.set_library_path("D:/msys64/mingw64/bin")


def showToken(node):
	ts = node.get_tokens()
	for t in ts:
		print(t.spelling)


index = clang.cindex.Index.create()
tu = index.parse("test.cpp")
showToken(tu.cursor)


def find_typerefs(node, typename):
	""" Find all references to the type named 'typename'
	"""
	if node.kind.is_reference():
		ref_node = node.get_definition()
		#print ref_node.spelling
		if ref_node.spelling == typename:
			print('Found %s [line=%s, col=%s]' % (typename, node.location.line, node.location.column))
	# # Recurse for children of this node
	for c in node.get_children():
		find_typerefs(c, typename)


index = clang.cindex.Index.create()
tu = index.parse("test.cpp")
find_typerefs(tu.cursor, "Man")
