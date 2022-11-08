import ast
import sys

###

import os
import subprocess
from typing import Dict, Union, List

# from brainscore_core.submission.endpoints import process_github_submission

JENKINS_BASE: "braintree.mit.edu:8080"
USER: os.environ['JENKINS_USR']
JENKINS_TOKEN = os.environ['JENKINS_TOKEN']
JOB_PATH: "dev_run_benchmarks"

def process_github_submission(plugin_info: Dict[str, Union[List[str], str]]):
    """
    Triggered when changes are merged to the GitHub repository, if those changes affect benchmarks or models.
    Starts parallel runs to score models on benchmarks (`run_scoring`).
    """
    models = List(models) if len(List(models)) > 0 else ['all']
    benchmarks = List(benchmarks) if len(List(benchmarks)) > 0 else ['all']
    for model in models:
        for benchmark in benchmarks:
            url = f'{JENKINS_BASE}/job/{JOB_PATH}/buildWithParameters?models={model}benchmarks={benchmark}&token={JENKINS_TOKEN}'
            response = subprocess.run(f"curl -X POST -u {USER}:{JENKINS_TOKEN} {url}")


if __name__ == '__main__':
    function = getattr(sys.modules[__name__], sys.argv[1])
    print(sys.argv[2])
    args_dict = ast.literal_eval(sys.argv[2])
    function(args_dict)
