# -*- coding: UTF-8 -*-
import os
import time
import os
import json

ROOT = os.getcwd()

path = 'Attribute'

file_dirs = os.walk(path)

test_files = []
file_names = []

for root, dirs, files in file_dirs:
    for file in files:
        test_files.append(os.path.join(ROOT, root, file))
        file_names.append(file)
        '''print(f"test_files:{os.path.join(ROOT, root, file)}")
        print(f"file_names:{file}")
        print()'''

for file in test_files:
    with open(file, 'r') as json_file:  # 从 JSON 文件中读取数据
        data = json.load(json_file)
        # data = json.loads(json.dumps(data, indent=4, sort_keys=True))
        # data = json.loads(json.dumps(data))
        print(type(data))
        print(data)  # 打印读取的数据
