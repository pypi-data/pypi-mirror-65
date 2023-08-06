import os

from Resources.helper.Utils import get_project_root
from Resources.testrail import *


class TestRailApi:
    def __init__(self, host='https://snapptestqa.testrail.io/', username='mohammad.yousefzadeh@snapp.cab',
                 password='Mohammad1992'):
        self.client = APIClient(host)
        self.client.user = username
        self.client.password = password
        self.root = str(get_project_root())
        status = {'passed': 1, 'blocked': 2, 'untested': 3, 'retest': 4, 'failed': 5}

    def get_project_with_name(self, project_name='Snapp Products'):
        projects = self.client.send_get('get_projects')
        for project in projects:
            if project['name'] == project_name:
                return project

    def get_run_object_with_name(self, run_name, project_name='Snapp Products'):
        project = self.get_project_with_name(project_name)
        runs = self.client.send_get('get_runs/{}'.format(project['id']))
        for run in runs:
            if run['name'] == run_name:
                return run

    def get_tests_of_run_test(self, run_name, project_name='Snapp Products'):
        run_id = self.get_run_object_with_name(run_name, project_name)['id']
        return self.client.send_get('get_tests/{}'.format(run_id))

    def get_tests_list_of_run_tests(self, run_test_name):
        tests = self.get_tests_of_run_test(run_name=run_test_name)
        return self.get_tests_list(tests)

    @staticmethod
    def get_tests_list(tests):
        result = []
        for test in tests:
            result.append(test['case_id'])
        return result

    def command_generator(self, run_test_name):
        tests = self.get_tests_of_run_test(run_test_name)
        commands = []
        for test in tests:
            test_id = 'c{}'.format(test['case_id'])
            commands.append(
                {'id': test['case_id'], 'command': 'python3 -m robot --include {} {}'.format(test_id, self.root)})
        return commands

    def update_test_case_status(self, run_name, test_case_id, status_id):
        run_id = self.get_run_object_with_name(run_name)['id']
        test_case_id = str(test_case_id).lstrip('c')

        data = {'status_id': status_id}
        self.client.send_post('add_result_for_case/{}/{}'.format(run_id, test_case_id), data=data)

    def run(self, run_name, update_status=True):
        tests = self.command_generator(run_name)
        for test in tests:
            print('running: {}'.format(test['command']))
            status = os.system(test['command'])
            if update_status:
                if status:
                    self.update_test_case_status(run_name, test['id'], 5)
                else:
                    self.update_test_case_status(run_name, test['id'], 1)

# example:
# a = TestRailApi()
# a.run('for test2')
