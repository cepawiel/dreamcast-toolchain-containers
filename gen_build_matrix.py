#!/usr/bin/python3

import json
import copy
import subprocess

f = open('builds.json')
input_data = json.load(f)
f.close()

output_data = []

for repo_config in input_data:
    repo = repo_config['kos']['url']
    branch = repo_config['kos']['branch']
    # get sha of most recient commit
    sha = subprocess.check_output(['git','ls-remote', repo, branch]).decode().split()[0]
    
    repo_config['kos']['sha'] = sha
    for toolchain in repo_config['toolchains']:
        tmp = copy.deepcopy(repo_config)

        tmp.pop('toolchains')
        tmp['toolchain'] = toolchain
        
        output_data.append(tmp)

print(json.dumps(output_data))
