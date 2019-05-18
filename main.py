from package_manager import Updater
from repo_manager import RepoManager
import logging
import os


class Loader:
    def __init__(self):
        self.__init_logger()

        # Update the framework dependent python packages
        self.fwPackageManager = Updater()
        update_ret, update_message = self.fwPackageManager.run_update()
        if update_ret:
            self.logger.info("Packages updated successfully.")
        else:
            self.logger.error("Error while updating packages. {}".format(update_message))

        # Update the configuration git repository
        self.confRepoHandler = RepoManager("configuration")
        ret_val, message = self.confRepoHandler.checkout()
        if not ret_val:
            self.logger.error(message)
        else:
            self.logger.info("Configuration repository is up to date")

        # Update the system dependent python packages
        self.sysPackageManager = Updater(os.path.abspath(os.path.join(
            os.path.dirname(__file__), "configuration/update_manager.json")))
        update_ret, update_message = self.sysPackageManager.run_update()
        if update_ret:
            self.logger.info("Packages updated successfully.")
        else:
            self.logger.error("Error while updating packages. {}".format(update_message))

        # Update the application repository
        self.appRepoHandler = RepoManager("application", os.path.abspath(
            os.path.join(os.path.dirname(__file__), "configuration/repo_manager.json")))
        ret_val, message = self.appRepoHandler.checkout()
        if not ret_val:
            self.logger.error(message)
        else:
            self.logger.info("Application repository is up to date")

    def __init_logger(self):
        self.logger = logging.getLogger("RPICarLogger")
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('main.log')
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)


def main():
    Loader()


if __name__ == "__main__":
    main()
