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

from pathlib import Path
import xml.etree.ElementTree as ET

from pybuilder.core import init, task

import pybuilder_pycharm_workspace.constants as const
import pybuilder_pycharm_workspace.messages as msg
from pybuilder_pycharm_workspace.errors import MissingPropertyError, NoPyCharmConfigDirError
from pybuilder_pycharm_workspace.helpers import fill_and_write_template, underscore
from pybuilder_pycharm_workspace.resources import templates as templates


@init
def initialise_plugin(project):
	"""
	Sets project defaults.

	:param pybuilder.core.Project project: PyBuilder project instance
	:return: None
	"""
	const.IML_FILENAME = const.IML_FILENAME.format(project_name=project.name)
	project.set_property_if_unset('pycharm_workspace_main_version', '2019')


@task(description=msg.TASK_DESCRIPTION_GENERATE_PYCHARM_WORKSPACE)
def generate_pycharm_workspace(project, logger):
	"""
	Main plugin task.

	It creates the ``.idea`` directory for the project and tells PyCharm the interpreter it should use with the
	current project (``.\\venv`` in project's directory by default).

	:param pybuilder.core.Project project: PyBuilder project instance
	:param pybuilder.core.Logger logger: PyBuilder logger instance
	:return: None
	"""
	logger.info(msg.WORKSPACE_START)

	if not project.get_property('pycharm_workspace_project_path'):
		raise MissingPropertyError('pycharm_workspace_project_path')

	add_project_interpreter(project, logger)
	add_project_idea_directory(project, logger)
	logger.info(msg.WORKSPACE_FINISH)


def add_project_interpreter(project, logger):
	"""
	Function in charge of adding project's virtual environment to PyCharm config.

	It checks the ``jdk.table.xml`` file for the existence of a previously configured interpreter with the same name.
	If it doesn't exist, this function adds the interpreter for PyCharm for the virtual environment belonging to the
	project. In case it finds one, this will be replaced by the new one.

	:param pybuilder.core.Project project: PyBuilder project instance
	:param pybuilder.core.Logger logger: PyBuilder logger instance
	:return: None
	:raises NoPyCharmConfigDirError: If the plugin can't find PyCharm config directory
	"""
	logger.info(msg.INTERPRETER_START)

	for directory in [".PyCharm", ".PyCharmCE"]:
		pycharm_config_path = list(Path.home().glob(f"{directory}{project.get_property('pycharm_workspace_main_version')}*"))[-1:]
		if len(pycharm_config_path):
			break
	if not len(pycharm_config_path):
		raise NoPyCharmConfigDirError
	pycharm_config_path = pycharm_config_path[0]
	logger.debug(msg.INTERPRETER_PYCHARM_LATEST.format(pycharm_config_name=pycharm_config_path.name))
	pycharm_config_path = pycharm_config_path / 'config' / 'options'
	logger.debug(msg.INTERPRETER_PYCHARM_LATEST_PATH.format(pycharm_config_path=pycharm_config_path))

	project_interpreter = templates.INTERPRETER.format(
		project_name=project.get_property('pycharm_workspace_project_path').name,
		project_path=str(project.get_property('pycharm_workspace_project_path')).replace('\\\\', '\\'))
	project_interpreter = ET.fromstring(project_interpreter)
	interpreter_name = project_interpreter.find('name').attrib['value']
	logger.debug(msg.INTERPRETER_NEW_NAME.format(interpreter_name=interpreter_name))
	project.set_property('pycharm_workspace_project_interpreter_name', interpreter_name)

	interpreters_file_path = str(pycharm_config_path / 'jdk.table.xml')
	interpreters_file = ET.parse(interpreters_file_path)
	interpreters_table = interpreters_file.getroot().find(".//component[@name='ProjectJdkTable']")
	old_project_interpreter = interpreters_table.find(f".//name[@value='{interpreter_name}']..")
	if old_project_interpreter is not None:
		logger.info(msg.INTERPRETER_FOUND)
		interpreters_table.remove(old_project_interpreter)
	interpreters_table.append(project_interpreter)
	interpreters_file.write(interpreters_file_path)

	logger.debug(msg.INTERPRETER_FILE_OVERWRITTEN.format(interpreters_file_path=interpreters_file_path))


def add_project_idea_directory(project, logger):
	"""
	Function in charge of adding PyCharm's ``.idea`` directory for the project.

	This function should be always executed before launching ``add_project_interpreter``. It creates the directory and
	includes the minimum necessary files on it filling the templates included in the plugin with the information of
	the current project. These files are:

	* IML file with project name defining project structure (as source folder etc.)
	* ``modules.xml`` file with a reference to IML file
	* ``misc.xml`` file with a reference to the interpreter configured by ``add_project_interpreter`` function
	* ``workspace.xml`` file with run manager configurations to ease different PyBuilder buildings:

		* Build with development environment configuration
		* Build with development environment configuration and no testing
		* Only run tests
		* Build with production environment configuration

	:param pybuilder.core.Project project: PyBuilder project instance
	:param pybuilder.core.Logger logger: PyBuilder logger instance
	:return: None
	"""
	logger.info(msg.WORKSPACE_CREATING_IDEA_DIRECTORY)
	pycharm_idea_directory = project.get_property('pycharm_workspace_project_path') / '.idea'
	pycharm_idea_directory.mkdir(exist_ok=True)

	logger.debug(msg.WORKSPACE_CREATING_FILE.format(file_name=const.IML_FILENAME))
	unit_tests = templates.IML_SOURCEFOLDER_TEMPLATE.format(
		directory=project.get_property('dir_source_unittest_python')) if project.get_property('dir_source_unittest_python') else ''
	integration_tests = templates.IML_SOURCEFOLDER_TEMPLATE.format(
		directory=project.get_property('dir_source_integrationtest_python')) if project.get_property('dir_source_integrationtest_python') else ''
	fill_and_write_template(templates.IML_FILE, pycharm_idea_directory / const.IML_FILENAME,
	                        **{ 'source_dir': (Path('src') / underscore(project.name)).as_posix(),
                                'unit_tests': unit_tests,
	                            'integration_tests': integration_tests,
								'project_interpreter_name': project.get_property('pycharm_workspace_project_interpreter_name'),
	                            'output_directory': project.get_property('dir_target') })

	logger.debug(msg.WORKSPACE_CREATING_FILE.format(file_name=const.MODULES_FILENAME))
	fill_and_write_template(templates.MODULES_FILE, pycharm_idea_directory / const.MODULES_FILENAME,
	                        **{ 'project_file_name': const.IML_FILENAME })

	logger.debug(msg.WORKSPACE_CREATING_FILE.format(file_name=const.MISC_FILENAME))
	fill_and_write_template(templates.MISC_FILE, pycharm_idea_directory / const.MISC_FILENAME,
                            **{ 'project_interpreter_name': project.get_property('pycharm_workspace_project_interpreter_name') })

	logger.debug(msg.WORKSPACE_CREATING_FILE.format(file_name=const.WORKSPACE_FILENAME))
	fill_and_write_template(templates.WORKSPACE_FILE, pycharm_idea_directory / const.WORKSPACE_FILENAME,
	                        **{ 'project_name': project.name })
