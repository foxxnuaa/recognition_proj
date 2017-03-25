# coding: utf-8
from BaseController import *
from lib.ScantronAnalyzeCV import *
from util.ErrorCode import *
import cv2
import numpy as np
import urllib2 as url

class ScantronRecogController(BaseController):
	def execute(self):
		self.checkParams()
		if not self.cardUrl:
			img = self.processUpFile("card")
		else:
			# 从其他地方获取图片
			res = url.urlopen(self.cardUrl)
			img = res.read()
		img = cv2.imdecode(np.fromstring(img, np.uint8), cv2.IMREAD_COLOR)# IMREAD_GRAYSCALE
		details = {}
		details["area"] = self.area
		details["questionCount"] = self.col
		details["answerCount"] = self.row
		details["groupCount"] = self.groupCount
		self.setResult(self.recog(img, details).T.tolist(), STATUS_OK)

	def checkParams(self):
		area = self.getArg("area", "")
		if area.strip():
			self.area = self.jsonLoad(area)
		else:
			self.area = None
		col = self.getIntArg("col")
		row = self.getIntArg("row")
		self.groupCount = max(1, self.getIntArg("groupCount"))
		if col == -1:
			raise ErrorStatusException("col must be a positive number", STATUS_PARAM_ERROR)
		if row == -1:
			raise ErrorStatusException("row must be a positive number", STATUS_PARAM_ERROR)
		self.col = col
		self.row = row
		if not self.fileExist("card"):
			self.cardUrl = self.getStrArg("card")
		else:
			self.cardUrl = None

	def recog(self, img, details):
		return readCard(img, details)