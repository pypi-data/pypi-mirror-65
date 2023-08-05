#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .common import _seemsValidText
from telegram_util import matchKey

SHORT_ARTICLE = ['每日书摘']

def _seemsValidRawArticle(soup, text_limit = 500):
	if not _seemsValidText(soup, limit = text_limit):
		return False
	return not not soup.find('img')

def _getInnerArticle_(soup, domain):	
	applicators = [
		lambda x: x.find("article"),
		lambda x: x.find("div", {"id" : "js_content"}),
		lambda x: x.find("div", class_ = "story-body__inner"),
		lambda x: x.find("div", class_ = "answercell"),
		lambda x: x.find("div", class_ = "post-text"),
		lambda x: x.find("div", {"id" : "bodyContent"}),
		lambda x: x.find("div", {"id" : "content_JS"}),
		lambda x: x.find("div", class_ = "main-post"),
		lambda x: x.find("div", class_ = "article"),
		lambda x: x.find("div", class_ = "field-name-body"),
		lambda x: x.find("div", class_ = "content"),
		lambda x: x.find("div", class_ = "u-content"),
		lambda x: x.find("div", class_ = "news_txt"),
	]
	domain_specific_applicators = {
		'matters': lambda x: x.find("div", class_ = "u-content"),
		'douban': lambda x: x.find("div", {"id" : "link-report"}),
		'douban.com/note': lambda x: x.find("div", class_ = "note"),
	}
	is_short = matchKey(soup.text, SHORT_ARTICLE)
	text_limit = 150 if is_short else 500
	for applicator in applicators:
		candidate = applicator(soup)
		if _seemsValidRawArticle(candidate, text_limit = text_limit):
			soup = candidate
	for d, applicator in domain_specific_applicators.items():
		if d in domain:
			candidate = applicator(soup)
			if candidate:
				soup = candidate
	return soup

def _getInnerArticle(soup, domain):
	all_content = str(soup)
	inner = _getInnerArticle_(soup, domain)
	index = all_content.find(str(inner))
	if index == -1:
		return inner, None
	return inner, all_content[:index]