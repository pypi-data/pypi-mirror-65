INTERPRETER = """
<jdk version="2">
  <name value="Python ({project_name})" />
  <type value="Python SDK" />
  <homePath value="{project_path}\\venv\Scripts\python.exe" />
  <roots>
    <classPath>
      <root type="composite">
        <root url="file://$USER_HOME$/PycharmProjects/{project_name}/venv" type="simple" />
        <root url="file://$USER_HOME$/PycharmProjects/{project_name}/venv/Lib/site-packages" type="simple" />
      </root>
    </classPath>
    <sourcePath>
      <root type="composite" />
    </sourcePath>
  </roots>
  <additional ASSOCIATED_PROJECT_PATH="$USER_HOME$/PycharmProjects/{project_name}" />
</jdk>
"""

IML_FILE = """
<?xml version="1.0" encoding="UTF-8"?>
<module type="PYTHON_MODULE" version="4">
  <component name="NewModuleRootManager">
    <content url="file://$MODULE_DIR$">
      <sourceFolder url="file://$MODULE_DIR$/{source_dir}" isTestSource="false" />{unit_tests}{integration_tests}
      <excludeFolder url="file://$MODULE_DIR$/.idea" />
      <excludeFolder url="file://$MODULE_DIR$/.pybuilder" />
      <excludeFolder url="file://$MODULE_DIR$/target/dist" />
      <excludeFolder url="file://$MODULE_DIR$/venv" />
    </content>
    <orderEntry type="jdk" jdkName="{project_interpreter_name}" jdkType="Python SDK" />
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
  <component name="TestRunnerService">
    <option name="projectConfiguration" value="Unittests" />
    <option name="PROJECT_TEST_RUNNER" value="Unittests" />
  </component>
</module>"""
IML_SOURCEFOLDER_TEMPLATE = """
      <sourceFolder url="file://$MODULE_DIR$/{directory}" isTestSource="true" />"""

MODULES_FILE = """
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectModuleManager">
    <modules>
      <module fileurl="file://$PROJECT_DIR$/.idea/{project_file_name}" filepath="$PROJECT_DIR$/.idea/{project_file_name}" />
    </modules>
  </component>
</project>"""

MISC_FILE = """
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectRootManager" version="2" project-jdk-name="{project_interpreter_name}" project-jdk-type="Python SDK" />
</project>"""

WORKSPACE_FILE = """
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="PropertiesComponent">
    <property name="RunOnceActivity.ShowReadmeOnStart" value="true" />
    <property name="WebServerToolWindowFactoryState" value="false" />
    <property name="last_opened_file_path" value="$PROJECT_DIR$/build.py" />
    <property name="settings.editor.selected.configurable" value="com.jetbrains.python.configuration.PyActiveSdkModuleConfigurable" />
  </component>
  <component name="RunManager" selected="Python.run tests">
    <configuration name="build (develop no-tests)" type="PythonConfigurationType" factoryName="Python">
      <module name="{project_name}" />
      <option name="INTERPRETER_OPTIONS" value="" />
      <option name="PARENT_ENVS" value="true" />
      <envs>
        <env name="PYTHONUNBUFFERED" value="1" />
      </envs>
      <option name="SDK_HOME" value="" />
      <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$" />
      <option name="IS_MODULE_SDK" value="true" />
      <option name="ADD_CONTENT_ROOTS" value="true" />
      <option name="ADD_SOURCE_ROOTS" value="true" />
      <EXTENSION ID="PythonCoverageRunConfigurationExtension" runner="coverage.py" />
      <option name="SCRIPT_NAME" value="$PROJECT_DIR$/build.py" />
      <option name="PARAMETERS" value="pycharm_builder publish --environment=develop --exclude=run_unit_tests --exclude=run_integration_tests" />
      <option name="SHOW_COMMAND_LINE" value="false" />
      <option name="EMULATE_TERMINAL" value="false" />
      <option name="MODULE_MODE" value="false" />
      <option name="REDIRECT_INPUT" value="false" />
      <option name="INPUT_FILE" value="" />
      <method v="2" />
    </configuration>
    <configuration name="build (develop)" type="PythonConfigurationType" factoryName="Python">
      <module name="{project_name}" />
      <option name="INTERPRETER_OPTIONS" value="" />
      <option name="PARENT_ENVS" value="true" />
      <envs>
        <env name="PYTHONUNBUFFERED" value="1" />
      </envs>
      <option name="SDK_HOME" value="" />
      <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$" />
      <option name="IS_MODULE_SDK" value="true" />
      <option name="ADD_CONTENT_ROOTS" value="true" />
      <option name="ADD_SOURCE_ROOTS" value="true" />
      <EXTENSION ID="PythonCoverageRunConfigurationExtension" runner="coverage.py" />
      <option name="SCRIPT_NAME" value="$PROJECT_DIR$/build.py" />
      <option name="PARAMETERS" value="pycharm_builder publish --environment=develop" />
      <option name="SHOW_COMMAND_LINE" value="false" />
      <option name="EMULATE_TERMINAL" value="false" />
      <option name="MODULE_MODE" value="false" />
      <option name="REDIRECT_INPUT" value="false" />
      <option name="INPUT_FILE" value="" />
      <method v="2" />
    </configuration>
    <configuration name="run tests (PyBuilder)" type="PythonConfigurationType" factoryName="Python">
      <module name="{project_name}" />
      <option name="INTERPRETER_OPTIONS" value="" />
      <option name="PARENT_ENVS" value="true" />
      <envs>
        <env name="PYTHONUNBUFFERED" value="1" />
      </envs>
      <option name="SDK_HOME" value="" />
      <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$" />
      <option name="IS_MODULE_SDK" value="true" />
      <option name="ADD_CONTENT_ROOTS" value="true" />
      <option name="ADD_SOURCE_ROOTS" value="true" />
      <EXTENSION ID="PythonCoverageRunConfigurationExtension" runner="coverage.py" />
      <option name="SCRIPT_NAME" value="$PROJECT_DIR$/build.py" />
      <option name="PARAMETERS" value="pycharm_builder run_unit_tests run_integration_tests --environment=develop" />
      <option name="SHOW_COMMAND_LINE" value="false" />
      <option name="EMULATE_TERMINAL" value="false" />
      <option name="MODULE_MODE" value="false" />
      <option name="REDIRECT_INPUT" value="false" />
      <option name="INPUT_FILE" value="" />
      <method v="2" />
    </configuration>
    <configuration name="build (production)" type="PythonConfigurationType" factoryName="Python">
      <module name="{project_name}" />
      <option name="INTERPRETER_OPTIONS" value="" />
      <option name="PARENT_ENVS" value="true" />
      <envs>
        <env name="PYTHONUNBUFFERED" value="1" />
      </envs>
      <option name="SDK_HOME" value="" />
      <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$" />
      <option name="IS_MODULE_SDK" value="true" />
      <option name="ADD_CONTENT_ROOTS" value="true" />
      <option name="ADD_SOURCE_ROOTS" value="true" />
      <EXTENSION ID="PythonCoverageRunConfigurationExtension" runner="coverage.py" />
      <option name="SCRIPT_NAME" value="$PROJECT_DIR$/build.py" />
      <option name="PARAMETERS" value="pycharm_builder publish --environment=production" />
      <option name="SHOW_COMMAND_LINE" value="false" />
      <option name="EMULATE_TERMINAL" value="false" />
      <option name="MODULE_MODE" value="false" />
      <option name="REDIRECT_INPUT" value="false" />
      <option name="INPUT_FILE" value="" />
      <method v="2" />
    </configuration>
    <configuration name="Unittests in {project_name}/tests" type="tests" factoryName="Unittests" nameIsGenerated="true">
      <module name="{project_name}" />
      <option name="INTERPRETER_OPTIONS" value="" />
      <option name="PARENT_ENVS" value="true" />
      <option name="SDK_HOME" value="" />
      <option name="WORKING_DIRECTORY" value="" />
      <option name="IS_MODULE_SDK" value="true" />
      <option name="ADD_CONTENT_ROOTS" value="true" />
      <option name="ADD_SOURCE_ROOTS" value="true" />
      <EXTENSION ID="PythonCoverageRunConfigurationExtension" runner="coverage.py" />
      <option name="_new_pattern" value="&quot;test_*.py&quot;" />
      <option name="_new_additionalArguments" value="&quot;&quot;" />
      <option name="_new_target" value="&quot;$PROJECT_DIR$/tests&quot;" />
      <option name="_new_targetType" value="&quot;PATH&quot;" />
      <method v="2" />
    </configuration>
    <list>
      <item itemvalue="Python.build (develop)" />
      <item itemvalue="Python.build (develop no-tests)" />
      <item itemvalue="Python.run tests (PyBuilder)" />
      <item itemvalue="Python.build (production)" />
      <item itemvalue="Python tests.Unittests in {project_name}/tests" />
    </list>
  </component>
</project>"""
