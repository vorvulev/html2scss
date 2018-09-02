import sublime
import sublime_plugin

from html2scss.rules_parser import *

class Html2scss(sublime_plugin.TextCommand):
	def run(self, edit, all_attrs = False):
		region = self.view.sel()[0]
		if (region.size() == 0):
			region = sublime.Region(0, self.view.size());

		html = self.view.substr(region)

		parser = ScssRulesParser()
		rules = parser.feed(html, all_attrs)
		if (rules):
			sublime.set_clipboard(rules)
			sublime.active_window().status_message('scss rules copied!')
