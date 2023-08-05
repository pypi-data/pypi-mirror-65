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

TASK_DESCRIPTION_GENERATE_PYCHARM_WORKSPACE = "Generates PyCharm workspace files fo the current project"

INTERPRETER_START = "Creating new Python interpreter for project's virtualenv"
INTERPRETER_PYCHARM_LATEST = "Latest PyCharm config directory detected: {pycharm_config_name}"
INTERPRETER_PYCHARM_LATEST_PATH = "PyCharm config directory detected: '{pycharm_config_path}'"
INTERPRETER_NEW_NAME = "New Python interpreter name: '{interpreter_name}'"
INTERPRETER_FOUND = "A Python interpreter found with the same name (replacing it)"
INTERPRETER_FILE_OVERWRITTEN = "'{interpreters_file_path}' file overwritten"

WORKSPACE_START = "Generating PyCharm project files"
WORKSPACE_CREATING_IDEA_DIRECTORY = "Creating new .idea directory"
WORKSPACE_CREATING_FILE = "Creating new {file_name} file in PyCharm .idea directory"
WORKSPACE_FINISH = "PyCharm workspace created"

MISSING_PROPERTY_ERROR = "Plugin property '{property}' not set in build.py file"
NO_PYCHARM_CONFIG_DIR_ERROR = "No PyCharm configuration directory found in user system path. Please launch PyCharm for the first time"
WRITING_FILE_ERROR = "There was an error trying to write '{file}' into {directory} directory"
