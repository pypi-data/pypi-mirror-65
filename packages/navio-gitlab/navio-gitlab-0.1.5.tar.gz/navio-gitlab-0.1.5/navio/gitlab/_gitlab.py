import os
import requests
from datetime import datetime, timedelta
import gitlab


class Gitlab():

    def __init__(self, api_url, **kwargs):
        self.gitlab = gitlab.Gitlab(api_url, kwargs)

    def is_gitlab(self):
        if os.environ.get('CI', 'false') == 'true':
            return True
        else:
            return False

    def is_pull_request(self):
        if self.is_gitlab() and os.environ.get('CI_MERGE_REQUEST_ID', None) is not None:
            return True
        else:
            return False

    def branch(self):
        if self.is_gitlab():
            return os.environ.get('CI_COMMIT_BRANCH')
        else:
            return 'master'

    def commit_hash(self):
        return os.environ.get('CI_COMMIT_SHA', '0' * 30)

    def short_commit_hash(self):
        return os.environ.get('CI_COMMIT_SHA', '0' * 30)[:7]

    def tag(self):
        return os.environ.get('CI_COMMIT_TAG', None)

    def is_tag(self):
        if os.environ.get('CI_COMMIT_TAG', False):
            return True
        else:
            return False

    def home_dir(self):
        return os.environ.get('HOME', '/dev/null')

    def build_dir(self):
        return os.environ.get('CI_BUILDS_DIR', '/dev/null')

    def build_number(self):
        prj = self.gitlab.projects.get(os.environ['CI_PROJECT_ID'])

        var = None
        try:
            var = prj.variables.get('BUILD_NUMBER')
        except gitlab.exceptions.GitlabGetError as e:
            if e.response_code == 404:
                prj.variables.create({'key': 'BUILD_NUMBER', 'value': '0'})
                return
        var.value = var.value + 1
        var.save()

        return var.value
