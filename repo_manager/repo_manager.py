import json
import os
import sys
from shutil import rmtree


class RepoError(Exception):
    """
    Unique exception class for the repository manager.
    """
    pass


class RepoManager:
    def __init__(self, repo_name, config_path=""):
        """
        The constructor open the configuration file, import the git package, open or clone the
        specified git repository in the input parameter.

        :param repo_name: The name of the repository which defined in the config file.
        :param config_path: The json configuration file path. If empty the default config file
        is 'config.json' in the same directory with the module.
        """
        self.repoName = repo_name
        if not config_path:
            self.configurationFileName = "config.json"
            self.configurationFilePath = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                         self.configurationFileName))
        else:
            self.configurationFilePath = config_path
        self.configuration = {}
        self.load_config(self.configurationFilePath, self.repoName)

        try:
            self.git = __import__("git")
        except ModuleNotFoundError:
            raise Exception("Error while loading git package.") from None

        try:
            self.repoPath = os.path.abspath(os.path.join(os.path.dirname(__file__), self.configuration["path"]))
            self.repoUrl = self.configuration["url"]
            self.repoVersion = self.configuration["version"]
        except KeyError as e:
            raise RepoError("Key: '{}' is not defined for '{}' in configuration file: '{}'."
                            .format(e.args[0], self.repoName, self.configurationFilePath))

        if not os.path.exists(self.repoPath):
            try:
                self.repoHandler = self.git.Repo.clone_from(self.repoUrl, self.repoPath, branch='master')
            except self.git.exc.GitCommandError:
                raise RepoError("Error while cloning the repository. Check internet connection.")
        else:
            if self.check_is_repo(self.repoPath):
                self.repoHandler = self.git.Repo(self.repoPath)
            else:
                rmtree(self.repoPath)
                try:
                    self.repoHandler = self.git.Repo.clone_from(self.repoUrl, self.repoPath, branch='master')
                except self.git.exc.GitCommandError:
                    raise RepoError("Error while cloning the repository. Check internet connection.")
        sys.path.append(self.repoPath)

    def load_config(self, config_file_path, repo_name):
        """
        This function loads a json file from the specified path

        :param repo_name: This parameter specifies the name of the repository from the config file.
        :param config_file_path: This parameter determines the config file path.
        """
        try:
            with open(config_file_path) as conf_file:
                self.configuration = json.load(conf_file)[repo_name]
        except FileNotFoundError:
            raise RepoError("Configuration file '{}' is not found.".format(config_file_path)) from None
        except json.decoder.JSONDecodeError as e:
            raise RepoError("Configuration file '{}' format is not supported. {}"
                            .format(config_file_path, e)) from None
        except KeyError as e:
            raise RepoError("Repository name: '{}' was not found in configuration file: '{}'."
                            .format(e.args[0], self.configurationFilePath)) from None

    def check_is_repo(self, path):
        """
        This function check the input path is it an existing git repository.

        :param path: The input git repository path.
        :return: True is it is or False if it is not a valid git repository
        """
        try:
            self.git.Repo(path)
        except self.git.exc.InvalidGitRepositoryError:
            return False
        else:
            return True

    def pull_changes(self):
        """
        This function runs the git pull command to fetch all new changes

        :return: Tuple which first element is a bool what represents if the updating was success True or False
        The second element is an string with the error message.
        """
        try:
            self.repoHandler.remotes.origin.fetch()
        except self.git.exc.GitCommandError as e:
            return False, "Error while running command: '{}'.".format(e.args[0])
        else:
            return True, ""

    def checkout(self):
        """
        This function checks out the the specified git repository version or branch
        which is defined in configuration file.

        :return: Tuple (bool, string) The bool True if the function success otherwise it is False.
        If there is any error occur the string parameter will contain it
        """
        ret_val, message = self.pull_changes()
        if not ret_val:
            return ret_val, message
        try:
            self.repoHandler.git.checkout(self.repoVersion)
        except self.git.exc.GitCommandError as e:
            return False, "Error while running command: '{}'.".format(e.args[0])
        else:
            return True, ""
