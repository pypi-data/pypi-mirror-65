


from jk_flexdata import *







class FlexDataSelector(object):

	def __init__(self, path:str):
		assert isinstance(path, str)
		assert path
		assert path[0] == "|"
		self.pathParts = []
		for item in path[1:].split("|"):
			try:
				n = int(item)
				self.pathParts.append(n)
			except:
				self.pathParts.append(item)
	#

	def __recursiveSelect(self, pathParts:list, currentElement):
		if not pathParts:
			# we're at the end of a path => we return this item.
			yield currentElement

		# now let's have a look at the next item
		currentPathPart = pathParts[0]

		if currentPathPart == "*":
			# we search for multiple nodes in a list
			if isinstance(currentElement, list):
				# yes, this is a list
				for item in currentElement:
					yield from self.__recursiveSelect(pathParts[1:], item)
			else:
				# no, this is not a list => ignore this element
				pass

		elif isinstance(currentPathPart, int):
			# current path part is an integer => expect a list and select list element
			if isinstance(currentElement, list):
				# yes, this is a list
				if (currentPathPart >= 0) and (currentPathPart < len(currentElement)):
					yield from self.__recursiveSelect(pathParts[1:], currentElement[currentPathPart])
			else:
				# no, this is not a list => ignore this element
				pass

		elif isinstance(currentPathPart, str):
			# current path part is a str => expect a regular tree node and select correct item
			if isinstance(currentElement, FlexObject):
				# yes, this is a FlexObject
				# we can descend
				v = currentElement[currentPathPart]
				if currentPathPart in currentElement:
					yield from self.__recursiveSelect(pathParts[1:], currentElement[pathParts[0]])
			else:
				# no, this is not a FlexObject => ignore this element
				pass

		else:
			raise Exception()
	#

	def getAll(self, dataTree:FlexObject):
		yield from self.__recursiveSelect(self.pathParts, dataTree)
	#

	def getOne(self, dataTree:FlexObject):
		for result in self.__recursiveSelect(self.pathParts, dataTree):
			return result
		return None
	#

#





