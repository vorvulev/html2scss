
import copy
from html.parser import HTMLParser

from html2scss import *
from html2scss.rules_parser import *

class ScssRulesParser(HTMLParser):
	scope = []

	def feed(self, data, all_attrs = False):
		self.scope = []
		Element.all_attrs = all_attrs

		super().feed(data)

		return isinstance(self.scope, Element) \
			and self.scope.group().rules() \
			or None;

	def handle_starttag(self, tag, attrs):
		if (attrs):
			self.scope.append(Element(attrs))

	def handle_endtag(self, tag):
		if (type(self.scope) is list):
			if (len(self.scope) > 1):
				elem = self.scope.pop()
				self.scope[-1].addChild(elem)
			else:
				elem = Element()
				elem.childs = [self.scope.pop()]
				self.scope = elem

class Element:
	all_attrs = False

	def __init__(self, attrs = [], is_mod = False):
		self.is_mod = is_mod
		self.childs = []
		self.attrs = []
		self.classes = None

		for attr in attrs:
			if (attr[0] != 'href' \
				and (
					self.all_attrs \
					or attr[0] in ['id', 'class']
				)
			):
				_class = getattr(
					rules_parser,
					'Attr' + attr[0].title(),
					Attr
				)
				attr = _class(attr)
				self.attrs.append(attr)

				if (isinstance(attr, AttrClass)):
					self.classes = self.attrs[-1]

		self.attrs.sort(key=lambda attr: attr.prior)
		if (not self.classes):
			self.classes = AttrClass()

	def addChild(self, elem):
		self.childs.append(elem)

	def group(self):
		patterns = {}
		is_mod = False

		for elem in self.childs:
			if (elem.is_mod):
				is_mod = True
			for cls in elem.classes.values:
				patterns.setdefault(cls, {
					'c': 0,
					'pos': self.childs.index(elem)
				})['c'] += 1

		for cls, info in sorted(
			patterns.items(),
			key = lambda item: item[1]['c'],
			reverse = True
		):
			if (info['c'] > 1):
				group = Element([('class', cls)], is_mod)

				for elem in self.childs:
					if (elem.classes.values.count(cls)):
						group.childs.append(elem)
						for _cls in elem.classes.values:
							if (patterns[_cls]):
								patterns[_cls]['c'] -= 1

				self.childs.insert(info['pos'], group)
				for k, elem in enumerate(group.childs):
					self.childs.remove(elem)
					group.childs[k] -= group
					group.childs[k].is_mod = True

				# self.childs.append(group)

		for elem in self.childs:
			elem.group()

		return self

	def rules(self, lvl = 0):
		str = ''

		selector = self.selector()
		if (len(selector)):
			str += '\n\n' + '\t' * lvl \
				+ selector + ' {'

		str += ''.join([
			elem.rules(lvl + 1 * bool(len(selector)))
				for elem in self.childs
		])

		if (len(selector)):
			str += '\n' + '\t' * lvl + '}'

		return str

	def selector(self):
		selector = ''.join([attr.selector() for attr in self.attrs])
		if (len(selector) and self.is_mod):
			selector = '&' + selector

		return selector

	def __repr__(self):
		return str(id(self)) + ': ' + self.selector()

	def __isub__(e1, e2):
		return e1 - e2

	def __sub__(e1, e2):
		result = copy.deepcopy(e1)

		if (result.classes and e2.classes):
			i = result.attrs.index(result.classes)
			result.classes -= e2.classes
			result.attrs[i] = result.classes

		return result

class Attribute:
	prior = 3

	def selector(self):
		pass

class Attr(Attribute):
	def __init__(self, config):
		self.name = config[0]
		self.value = config[1] or ''

	def selector(self):
		return '[' + self.name \
			+ ('="' + self.value + '"'
				if (len(self.value))
				else ''
			) + ']'

	def __eq__(a1, a2):
		return a1.name == a2.name \
			and a1.value == a2.value

class MultiValuesAttr(Attribute):
	prefix = ''

	def __init__(self, config = ['', '']):
		self.values = (config[1] or '').split(' ')

	def selector(self):
		return ''.join([self.prefix + val for val in self.values])

	def __repr__(self):
		return str(id(self)) + ': ' + self.selector()

	def __isub__(c1, c2):
		return c1 - c2

	def __sub__(c1, c2):
		result = copy.deepcopy(c1)

		for val in c2.values:
			if val in result.values:
				result.values.remove(val)

		return result

	def __eq__(c1, c2):
		return c1.values == c2.values

class AttrClass(MultiValuesAttr):
	prior = 2
	prefix = '.'

class AttrId(MultiValuesAttr):
	prior = 1
	prefix = '#'
