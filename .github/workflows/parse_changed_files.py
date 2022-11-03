import argparse
import re
from pathlib import Path
import sys
from typing import List

PLUGIN_DIRS = ['benchmarks', 'data', 'models', 'metrics']


def get_changed_files() -> List[str]:

	changed_files = sys.argv[2]
	changed_files_list = changed_files.split()

	plugin_files_changed = []
	non_plugin_files_changed = []

	for f in changed_files_list:
		if not any(plugin_dir in f for plugin_dir in PLUGIN_DIRS):
			non_plugin_files_changed.append(f)
		else:
			plugin_files_changed.append(f)

	return plugin_files_changed, non_plugin_files_changed


def is_plugin_only():

	plugin_files_changed, non_plugin_files_changed = get_changed_files()

	if len(non_plugin_files_changed) > 0:
		print("false")
	else:
		print("true")


def _get_registered_plugins(plugin_type: str, plugin_dirs: List[str]) -> List[str]:
	""" 
	Searches all `plugin_type` __init.py__ files for registered plugins.
	Returns list of identifiers for each registered plugin. 
	"""
	registered_plugins = []

	for plugin_dirname in plugin_dirs:
		plugin_dirpath = Path(f'brainscore_language/{plugin_type}/{plugin_dirname}')
		init_file = plugin_dirpath / "__init__.py"
		with open(init_file) as f:
			registry_name = plugin_type.strip(
				's') + '_registry'  # remove plural and determine variable name, e.g. "models" -> "model_registry"
			plugin_registrations = [line for line in f if f"{registry_name}["
									in line.replace('\"', '\'')]
			for line in plugin_registrations:
				result = re.search(f'{registry_name}\[.*\]', line)
				identifier = result.group(0)[len(registry_name)+2:-2]
				registered_plugins.append(identifier)

	return registered_plugins


def create_plugins_dict():

	plugin_files_changed, non_plugin_files_changed = get_changed_files()

	plugins_dict = {"run_score": "false",
					"models_and_benchmarks": {}}

	scoring_plugins = ("models", "benchmarks")
	scoring_plugin_paths = tuple([f'brainscore_language/{plugin_type}/' for plugin_type in scoring_plugins])
	model_and_benchmark_files = [fname for fname in plugin_files_changed if fname.startswith(scoring_plugin_paths)]
	if len(model_and_benchmark_files) > 0:
		plugins_dict["run_score"] = "true"
		for plugin_type in scoring_plugins:
			plugin_dirs = set([fname.split('/')[2] for fname in model_and_benchmark_files if f'/{plugin_type}/' in fname])
			plugins_to_score = _get_registered_plugins(plugin_type, plugin_dirs)
			plugins_dict["models_and_benchmarks"][plugin_type] = ' '.join(plugins_to_score)

	print(plugins_dict)


if __name__ == '__main__':

	function = getattr(sys.modules[__name__], sys.argv[1])
	function()
