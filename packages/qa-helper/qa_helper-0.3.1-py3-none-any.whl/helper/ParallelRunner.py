import json
import os
import shutil
import sys
from distutils.dir_util import copy_tree
from os.path import join
from pathlib import Path
import pandas as pandas

from Resources.helper.BaseActions import BaseActions


class ParallelRunner:
    def __init__(self, test_suite, test_case=None, excel_file=None,
                 args_list=None):
        self.project_root = str(BaseActions.get_project_root())
        sys.path.insert(0, self.project_root)
        self.parent_dir = join(self.project_root, 'ArgFiles')
        Path(self.parent_dir).mkdir(parents=True, exist_ok=True)
        self.command = None
        self.args_list = []
        self.test_case = test_case
        self.test_suite = join(self.project_root, test_suite)
        if excel_file:
            self.args_list.extend(self.convert_excel_to_json(excel_file))
        if args_list:
            self.args_list.extend(args_list)
        if not self.args_list:
            raise Exception('you should set excel_file or args_list')

        self.command_generator()

    def command_generator(self):
        counter = 1
        args_str = ' --processes {} '.format(len(self.args_list))
        for args in self.args_list:
            if 'usage' in args and not args['usage']:
                continue
            file_name = join(self.parent_dir, 'args{}.txt'.format(str(counter)))
            browser_data_dir = self.create_browser_data(counter)
            # arguments = ' --include Run{}\n'.format(counter)
            arguments = ' -v {}:{}\n'.format('data_dir', browser_data_dir)
            for key in args:
                if args[key]:
                    arguments = arguments + ' -v {}:{}\n'.format(key, args[key])
            with open(file_name, 'w+') as file:
                file.write(arguments)
            args_str = args_str + ' --argumentfile{} {} '.format(str(counter), file_name)
            counter += 1
        if self.test_case:
            args_str = args_str + ' -t {} '.format(self.test_case)
        self.command = 'pabot {} {}'.format(args_str, self.test_suite)
        print(self.command)

    def run(self):
        os.system(self.command)

    @staticmethod
    def convert_excel_to_json(execl_file, sheet_name='Sheet1', orient='records'):
        excel_data_df = pandas.read_excel(execl_file, sheet_name=sheet_name)
        result = excel_data_df.to_json(orient=orient).replace('\\n', '')
        return json.loads(result)

    def create_browser_data(self, number):
        src_dir = join(self.project_root, 'selenium')
        browser_data_dir = join(self.project_root, 'selenium{}'.format(str(number)))
        if os.path.exists(browser_data_dir) and os.path.isdir(browser_data_dir):
            shutil.rmtree(browser_data_dir)
        Path(browser_data_dir).mkdir(parents=True, exist_ok=True)
        os.system('cp -r {}/ {}/'.format(src_dir, browser_data_dir))
        # copy_tree(src_dir, browser_data_dir)
        return browser_data_dir
