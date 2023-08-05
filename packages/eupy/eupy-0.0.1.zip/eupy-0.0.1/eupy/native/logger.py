#!/usr/bin/env python
import logging

"""
Wrapper class over logging.Logger to automate formatting and other jobs
"""
class Logger:

	def __init__(self, name, level = logging.INFO):
		self._configLogger(name, level)
		self.debug("Logger initialized")
		return

	def _configLogger(self, name, level):
		# create logger
		self._logger = logging.getLogger(name)
		self._logger.setLevel(level)

		# create console handler and set level to debug
		ch = logging.StreamHandler()
		ch.setLevel(level)

		# create formatter
		formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

		# add formatter to ch
		ch.setFormatter(formatter)

		# add ch to logger
		if not self._logger.handlers:
			self._logger.addHandler(ch)
			self._logger.propagate = False
			
		self.debug("logger.Logger._configLogger()")
		return

	@property
	def handlers(self):
		return self._logger.handlers

	@property
	def logger(self):
		return self._logger
	
	@property
	def level(self):
		return logging.getLevelName(self._logger.level)
	
	"""
	Main logging functions
	"""
	def debug(self, message):
		self._logger.debug(message)

	def info(self, message):
		self._logger.info(message)

	def warning(self, message):
		self._logger.warning(message)

	def warn(self, message):
		self._logger.warn(message)

	def error(self, message):
		self._logger.error(message)
	
	def critical(self, message):
		self._logger.critical(message)

	def shutdown(self):
		self.debug("eupy.native.logger.Logger.shutdown()")
		logging.shutdown()
		return

	def getLogger(self, name):
		return self._logger

_logger = None

def initLogger(name, lvl):
	if lvl:
		l = logging.DEBUG
	else:
		l = logging.INFO
	global _logger
	_logger = Logger(name, level = l)
	_logger.debug("eupy.native.logger.initLogger()")

	return _logger

def getLogger():
	global _logger
	if _logger == None:
		raise NameError("Logger has not been initialized!")
	else:
		_logger.debug("eupy.native.logger.getLogger()")
		return _logger

def initOrGetLogger():
	global _logger
	if _logger == None:
		_logger = Logger("Logger")
		_logger.warning("Logger has not been explicitly initialized")
		_logger.debug("eupy.native.logger.initOrGetLogger()")
		return _logger
	else:
		_logger.debug("eupy.native.logger.initOrGetLogger()")
		return _logger
