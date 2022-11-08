import ast
import sys

###

import os
import subprocess
from typing import Dict, Union, List

# from brainscore_core.submission.endpoints import process_github_submission

JENKINS_BASE = "braintree.mit.edu:8080"
USER = os.environ['JENKINS_USR']
JENKINS_TOKEN = os.environ['JENKINS_TOKEN']
JOB_PATH = "dev_run_benchmarks"

def process_github_submission(plugin_info: Dict[str, Union[List[str], str]]):
	"""
	Triggered when changes are merged to the GitHub repository, if those changes affect benchmarks or models.
	Starts parallel runs to score models on benchmarks (`run_scoring`).
	"""
	model_list = plugin_info['models'].split()
	benchmark_list = plugin_info['benchmarks'].split()

	models = model_list if len(model_list) > 0 else ['all']
	benchmarks = benchmark_list if len(benchmark_list) > 0 else ['all']
	for model in models:
		for benchmark in benchmarks:
			url = f'{JENKINS_BASE}/job/{JOB_PATH}/buildWithParameters?models={model}benchmarks={benchmark}&token={JENKINS_TOKEN}'
			response = subprocess.run(f"curl -X POST -u {USER}:{JENKINS_TOKEN} {url}", shell=True)


if __name__ == '__main__':
	function = getattr(sys.modules[__name__], sys.argv[1])
	args_dict = ast.literal_eval(sys.argv[2])
	function(args_dict)
