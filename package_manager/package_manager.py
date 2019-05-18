import json
import os
import sys
import re
from subprocess import Popen, PIPE


class UpdaterError(Exception):
    pass


class Updater:
    def __init__(self, config_path=""):
        """
        The constructor loads the config file, which can be defined by parameter, if it is empty
        it will load automatically the 'config.json' file in the package root folder
        """
        if not config_path:
            self.configurationFileName = "config.json"
            self.configurationFilePath = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                         self.configurationFileName))
        else:
            self.configurationFilePath = config_path
        self.configuration = {}
        self.load_config(self.configurationFilePath)

    def load_config(self, config_file_path):
        """
        This function loads a json file from the specified path
        :param config_file_path: This parameter determines the config file path.
        """
        try:
            with open(config_file_path) as conf_file:
                self.configuration = json.load(conf_file)
        except FileNotFoundError:
            raise UpdaterError("Configuration file '{}' is not found.".format(config_file_path)) from None
        except json.decoder.JSONDecodeError as e:
            raise UpdaterError("Configuration file '{}' format is not supported. {}"
                               .format(config_file_path, e)) from None

    def get_installed_versions(self):
        """
        This function calls the pip show command for every specified package from the
        config file. Reads their versions.

        :return: Dictionary which contains the installed packages ant its versions.
        If the configuration file is not contains any packages. the return dict will be empty.
        """
        installed_dict = {}
        if "packages" not in self.configuration:
            return installed_dict

        for package in self.configuration["packages"]:
            command = [sys.executable, "-m", "pip", "show", package]
            call_obj = Popen(command, stderr=PIPE, stdout=PIPE)
            out_str = call_obj.stdout.read().decode()
            if len(out_str) == 0:
                installed_dict[package] = None
            else:
                find = re.search("Version: ([0-9;.]*)", out_str)
                if find:
                    installed_dict[package] = find.group(1)
        return installed_dict

    def run_update(self):
        """
        This function run updates for pip and every packages which are defined in the configuration file.
        The pip will be upgraded to the latest version the other packages to the specified versions.

        Note: This function does not handle proxy for pip.

        :return: Tuple with two element the first is True if the updating finished successfully or not
        updated because already installed. Otherwise False if the packages are not defined in the
        configuration or the updating fails.
        The second element is a string which is empty n case of True, but if the first element is False
        it contains the specified error message.
        """
        if "packages" not in self.configuration:
            return False, "Packages is not defined in configuration file"

        command = [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
        call_obj = Popen(command, stdout=PIPE, stderr=PIPE)
        call_obj.communicate()
        if call_obj.returncode != 0:
            return False, "Error while running pip upgrade"

        for package in self.configuration["packages"]:
            if self.configuration["packages"][package] == "":
                command = [sys.executable, "-m", "pip", "install", "--user", package]
            else:
                command = [sys.executable, "-m", "pip", "install", "--user", package+"=="+self.configuration["packages"][package]]

            call_obj = Popen(command, stdout=PIPE, stderr=PIPE)
            call_obj.communicate()
            if call_obj.returncode != 0:
                return False, "Error while running command: '{}'.".format(" ".join(command))
        return True, ""
