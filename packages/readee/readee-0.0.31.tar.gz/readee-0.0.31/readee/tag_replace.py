#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .common import _copyB, fact

def _tagReplace(soup, args = {}):
	wrap_with_i = [
		soup.find_all("div"),
		soup.find_all("span"),
		soup.find_all("p"),
	]
	for l in wrap_with_i:
		for item in l:
			attrs = str(item.attrs)
			attrs = attrs.replace(": ", ":")
			if 'font-style:italic' in attrs:
				wrapper = fact().new_tag("i")
				wrapper.append(_copyB(item))
				item.replace_with(wrapper)
	wrap_with_p = [
		soup.find_all("div", class_="article-paragraph"),
		soup.find_all("section"),
		[x for x in soup.children if isinstance(x, str)],
	]
	for l in wrap_with_p:
		for item in l:
			wrapper = fact().new_tag("p")
			wrapper.append(_copyB(item))
			item.replace_with(wrapper)
	if args.get('list_replace'):
		to_remove_tags = [
			soup.find_all("li"),
			soup.find_all("ul")
		]
		for l in to_remove_tags:
			for item in l:
				item.name = p
	return soup