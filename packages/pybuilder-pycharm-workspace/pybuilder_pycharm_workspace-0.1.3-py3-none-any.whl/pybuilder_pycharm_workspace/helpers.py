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

import re

from pybuilder_pycharm_workspace.errors import WritingFileError


def fill_and_write_template(template, output_path, **fields):
	"""
	Fills a template with some values and writes the result in a specific location.

	:param str template: Text to format
	:param str output_path: Path where the new file will be saved
	:param dict[str, str] fields: Collection of template's fields with the new values to write
	:return: None
	:raises WritingFileError: If there was an error while trying to write the file
	"""
	try:
		project_metadata = template.strip().format(**fields)
		with open(output_path, 'w') as project_file:
			project_file.write(project_metadata)
	except:
		raise WritingFileError(template, output_path)


def underscore(word):
	"""
	``underscore()`` function taken from ``inflection`` library.

	More information:
		https://inflection.readthedocs.io/en/latest/#inflection.underscore

	:param str word: Text to process
	:return: Underscored word with no hyphens and lowercased.
	:rtype: str
	"""
	word = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", word)
	word = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", word)
	word = word.replace('-', '_')
	return word.lower()
