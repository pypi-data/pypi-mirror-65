#   -*- coding: utf-8 -*-
#   Copyright 2020 Diego Barrantes
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import pybuilder_pycharm_workspace.messages as msg


class MissingPropertyError(Exception):
	def __init__(self, property, message=None):
		"""
		This exception is raised when a property value is missing.

		:param str or None message: Custom exception message
		"""
		super().__init__(message if message else msg.MISSING_PROPERTY_ERROR.format(property=property))


class NoPyCharmConfigDirError(Exception):
	def __init__(self, message=None):
		"""
		This exception is raised when the plugin can't find PyCharm configuration directory.

		:param str or None message: Custom exception message
		"""
		super().__init__(message if message else msg.NO_PYCHARM_CONFIG_DIR_ERROR)


class WritingFileError(Exception):
	def __init__(self, file_path, directory, message=None):
		"""
		This exception is raised when the plugin is trying to write one of the configuration files to disk.

		:param str or None message: Custom exception message
		"""
		super().__init__(message if message else msg.WRITING_FILE_ERROR.format(file=file_path, directory=directory))
