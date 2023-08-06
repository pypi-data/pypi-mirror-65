# -*- encoding: utf-8 -*-
import requests

from suite_py.lib.config import Config
from suite_py.lib.singleton import Singleton
from suite_py.lib.handler import git_handler as git


config = Config()


class CaptainHook(metaclass=Singleton):
    _baseurl = None
    _timeout = None

    def __init__(self):
        self._baseurl = config.load()["user"]["captainhook_url"]
        self._timeout = config.load()["user"]["captainhook_timeout"]

    def lock_project(self, project, env):
        data = {
            "project": project,
            "status": "locked",
            "user": git.get_username(),
            "environment": env,
        }
        return self.send_post_request("/projects/manage-lock", data)

    def unlock_project(self, project, env):
        data = {
            "project": project,
            "status": "unlocked",
            "user": git.get_username(),
            "environment": env,
        }
        return self.send_post_request("/projects/manage-lock", data)

    def status(self, project, env):
        return self.send_get_request(
            f"/projects/check?project={project}&environment={env}"
        )

    def get_users_list(self):
        return self.send_get_request("/users/all")

    def send_post_request(self, endpoint, data):
        return requests.post(
            f"{self._baseurl}{endpoint}", data=data, timeout=self._timeout
        )

    def send_get_request(self, endpoint):
        return requests.get(f"{self._baseurl}{endpoint}", timeout=(2, self._timeout))

    def set_timeout(self, timeout):
        self._timeout = timeout
