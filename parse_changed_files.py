import sys

PLUGIN_DIRS = ['benchmarks', 'data', 'models', 'metrics']

changed_files = sys.argv[1]
changed_files_list = changed_files.split()

plugin_files_changed = []
non_plugin_files_changed = []

for f in changed_files_list:
	if not any(plugin_dir in f for plugin_dir in PLUGIN_DIRS):
		non_plugin_files_changed.append(f)
	else:
		plugin_files_changed.append(f)

if len(non_plugin_files_changed) > 0:
	print("false")
else:
	print("true")