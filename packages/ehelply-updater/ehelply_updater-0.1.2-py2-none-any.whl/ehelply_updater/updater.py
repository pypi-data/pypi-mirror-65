from ehelply_logger.Logger import Logger

from pydantic import BaseModel
from typing import List, Union
from datetime import datetime
from pathlib import Path
import shutil
import json
import requests


class Config(BaseModel):
    api_base_url: str  # Where the service template API can be found
    update_dir: str  # The root directory of the microservice
    package_file: str  # The ehelply-package.json file which contains version and updating information for the microservice
    access_key: str  # Access key identifies this microservice to the updater service
    secret_key: str  # Secret key gives a secret passkey to the updater service to validate that this is a valid service


class Version(BaseModel):
    version: str = "0.0.0"
    release_date: str = ""
    upgrade_instructions: List[str] = []
    release_notes: List[str] = []


class VersionsFile(BaseModel):
    versions: List[str]
    version_meta: dict


class UpdateInfo(BaseModel):
    primary: Version = Version()
    previous: List[Version] = []


class Package(BaseModel):
    version: str


class FileMeta(BaseModel):
    name: str
    path: str


class UpdateFiles(BaseModel):
    """
    List of created and removed files for an update
    """
    created: List[FileMeta] = []
    removed: List[FileMeta] = []


class File(FileMeta):
    content: str = ""


class Updater:
    def __init__(self, config: Config, logger: Logger = None) -> None:
        self.config: Config = config
        self.package: dict = {}
        self.headers: dict = {
            "X-AccessKey": config.access_key,
            "X-SecretKey": config.secret_key,
        }
        self.setup()
        self.logger: Logger = logger
        if not self.logger:
            self.logger = Logger()

    def setup(self):
        """
        Setup the updater utility
        :return:
        """
        with open(self.config.package_file, 'r') as file:
            self.package.update(json.load(file))

    def save_updated_package(self, update_information: UpdateInfo):
        self.package['template_version'] = update_information.primary.version

        with open(self.config.package_file, 'w') as file:
            json.dump(self.package, file)

    def is_update_required(self) -> bool:
        """
        Check with the service template service for whether an update exists

        Expected Response:
        {
            "required": bool
        }
        :return:
        """
        response = requests.get(
            self.config.api_base_url + "/versions/" + self.package['template_version'] + "/updates",
            headers=self.headers)

        if response.status_code == 200:
            return response.json()['required']

        raise Exception("Unable to determine whether an update is required")

    def get_update_information(self, desired_version: str = "latest") -> UpdateInfo:
        """
        Gets information about the update from the server
        :return:
        """
        response = requests.get(
            self.config.api_base_url + "/versions/" + self.package['template_version'] + "/updates/" + desired_version,
            headers=self.headers)

        if response.status_code == 200:
            return UpdateInfo(**response.json())

        raise Exception("Unable to get update information")

        # return Updates(updates=[
        #     Update(version="2.0.0", changelog=["Added a thing", "Removed a thing"]),
        #     Update(version="1.9.0", changelog=["Did a cool thing", "Did a different cool thing"]),
        # ])

    def get_file_list(self, desired_version: str = "latest") -> UpdateFiles:
        """
        Returns a list of files that need to be updated
        :return:
        """

        response = requests.get(self.config.api_base_url + "/versions/" + self.package[
            'template_version'] + "/updates/" + desired_version + "/files",
                                headers=self.headers)

        if response.status_code == 200:
            return UpdateFiles(**response.json())

        raise Exception("Unable to retrieve an update file list")

        # return FileMetas(files=[
        #     FileMeta(uuid="test", name="my_backup_test.txt", path="tests"),
        #     FileMeta(uuid="test", name="another_test.txt", path="tests/nested")
        # ])

    def get_updated_file(self, file: FileMeta, desired_version: str = "latest") -> File:
        """
        Retrieves the contents of an updated file from the server
        :return:
        """
        response = requests.get(self.config.api_base_url + "/versions/" + self.package[
            'template_version'] + "/updates/" + desired_version + "/files/" + file.name,
                                params={"path": file.path},
                                headers=self.headers)

        if response.status_code == 200:
            return File(**response.json())

        raise Exception("Unable to retrieve updated file")

        # return File(
        #     name="my_update_test.txt",
        #     path="tests/service",
        #     uuid="test",
        #     content="I am the new epic content of this file"
        # )

    def save_updated_file(self, file: File):
        """
        Updates the file in the microservice
        :return:
        """
        folder_path = Path(self.config.update_dir).resolve().joinpath(file.path)
        folder_path.mkdir(parents=True, exist_ok=True)
        file_path = folder_path.joinpath(file.name)
        with open(str(file_path), 'w') as io_file:
            io_file.write(file.content)

    def delete_file(self, file_meta: FileMeta):
        try:
            Path(self.config.update_dir).resolve().joinpath(file_meta.path).joinpath(file_meta.name).unlink()
        except:
            # File not found
            pass

    def backup(self, location, file: FileMeta):
        """
        Backup the microserivces current service template files
        :return:
        """
        original = Path(self.config.update_dir).resolve().joinpath(file.path).joinpath(file.name)
        backup = Path(location).joinpath(file.path)
        backup.mkdir(parents=True, exist_ok=True)
        backup = backup.joinpath(file.name)
        shutil.copy(original, backup)

    def create_backup_readme(self, location, update_information: UpdateInfo):
        update_information_str: str = ""

        update_information_str += """* {version}
""".format(version=update_information.primary.version)
        for changelog_item in update_information.primary.release_notes:
            update_information_str += """   * {item}
""".format(item=changelog_item)

        for update in update_information.previous:
            update_information_str += """* {version}
""".format(version=update.version)
            for changelog_item in update.release_notes:
                update_information_str += """   * {item}
""".format(item=changelog_item)

        readme: str = """# Service Template Backup
This is a backup which was autogenerated by updating the service template.
You are free to remove this backup if it is of no use to you. 

## Update Information
{update_information}""".format(update_information=update_information_str)

        with open(str(location.joinpath("readme.md")), 'w') as file:
            file.write(readme)

    def pp_upgrade_info(self, upgrade: UpdateInfo):
        """
        Pretty prints upgrade info
        :param upgrade:
        :return:
        """
        newest_version: str = upgrade.primary.version
        skipped_versions: List[str] = []
        release_notes: List[str] = []
        upgrade_instructions: List[str] = []

        for previous in upgrade.previous:
            skipped_versions.append(previous.version)
            release_notes += previous.release_notes
            upgrade_instructions += previous.upgrade_instructions

        release_notes += upgrade.primary.release_notes
        upgrade_instructions += upgrade.primary.upgrade_instructions

        print("Newest version: " + newest_version)
        print("Skipped versions: " + str(skipped_versions))

        print()
        print("Release Notes:")
        for note in release_notes:
            print("  * " + note)

        print()
        print("Upgrade Instructions:")
        for instruction in upgrade_instructions:
            print("  * " + instruction)

    def preview(self) -> Union[bool, UpdateInfo]:
        """
        Determine whether an update is required and get information about it
        :return:
        """
        if self.is_update_required():
            return self.get_update_information()
        else:
            return False

    def update(self) -> Union[bool, UpdateInfo]:
        """
        Preform an update on the microservice with the given configuration
        :return:
        """
        if self.is_update_required():
            # Get update information
            update_information: UpdateInfo = self.get_update_information()

            # Setup backup location
            backup_location = Path(self.config.update_dir).resolve().joinpath(
                datetime.utcnow().strftime("%Y%m%d-%H%M%S-utc.service-template.bak/"))
            backup_location.mkdir()

            self.create_backup_readme(backup_location, update_information)

            for file_meta in self.get_file_list().created:
                # Get typing information
                file_meta: FileMeta = file_meta

                api_file_meta: FileMeta = FileMeta(
                    name=file_meta.name,
                    path=file_meta.path,
                )

                # print(Path(Path(file_meta.path)))
                # print(len(Path(file_meta.path).parents))
                #
                # print(Path(Path(file_meta.path).parents[0]))

                if len(Path(file_meta.path).parents) == 1:
                    file_meta.path = str(Path(file_meta.path))
                else:
                    known_version_prefix: Path = Path(
                        Path(file_meta.path).parents[len(Path(file_meta.path).parents) - 2])
                    file_meta.path = str(Path(file_meta.path).relative_to(known_version_prefix))

                # Backup original version
                try:
                    self.backup(location=backup_location, file=file_meta)
                except:
                    self.logger.debug("Cannot backup file as it does not exist: " + file_meta.name)

                # Retrieve updated file from the server
                file: File = self.get_updated_file(api_file_meta)

                if len(Path(file.path).parents) == 1:
                    known_version_prefix: Path = Path(file.path)
                else:
                    known_version_prefix: Path = Path(Path(file.path).parents[len(Path(file.path).parents) - 2])
                file.path = str(Path(file.path).relative_to(known_version_prefix))

                # Save the updated file
                self.save_updated_file(file)

            for file_meta in self.get_file_list().removed:
                # Get typing information
                file_meta: FileMeta = file_meta

                # api_file_meta: FileMeta = FileMeta(
                #     name=file_meta.name,
                #     path=file_meta.path,
                # )

                # known_version_prefix: Path = Path(Path(file_meta.path).parents[len(Path(file_meta.path).parents) - 2])
                # file_meta.path = str(Path(file_meta.path).relative_to(known_version_prefix))

                # Backup original version
                try:
                    self.backup(location=backup_location, file=file_meta)
                except:
                    self.logger.debug("Cannot backup file as it does not exist: " + file_meta.name)

                # Retrieve updated file from the server
                # file: File = self.get_updated_file(api_file_meta)
                #
                # known_version_prefix: Path = Path(Path(file.path).parents[len(Path(file.path).parents) - 2])
                # file.path = str(Path(file.path).relative_to(known_version_prefix))

                # Save the updated file
                self.delete_file(file_meta)

            self.save_updated_package(update_information)

            # Return with update information
            return update_information
        else:
            return False
