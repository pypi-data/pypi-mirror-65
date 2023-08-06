import logging
import json

from zygoat.components import Component, FileComponent
from zygoat.constants import Projects
from zygoat.utils.files import use_dir
from zygoat.utils.shell import run

from . import resources

log = logging.getLogger()

server_file = "next-server.js"


class ServerFile(FileComponent):
    resource_pkg = resources
    base_path = Projects.FRONTEND
    filename = server_file
    overwrite = False


class PackageConfig(Component):
    def create(self):
        with use_dir(Projects.FRONTEND):
            log.info("Adding custom commands to package.json")
            data = {}

            with open("package.json") as package_file:
                data = json.load(package_file)

            data["scripts"][
                "start"
            ] = f"npm run build && NODE_ENV=production node {server_file}"
            data["scripts"]["dev"] = f"node {server_file}"

            log.info("Writing out custom commands")
            with open("package.json", "w") as package_file:
                json.dump(data, package_file)


class Dependencies(Component):
    def create(self):
        with use_dir(Projects.FRONTEND):
            log.info("Installing custom server dependencies")
            run(["yarn", "add", "express", "express-http-proxy"])


class CustomServer(Component):
    def create(self):
        pass


custom_server = CustomServer(sub_components=[Dependencies(), ServerFile(), PackageConfig()])
