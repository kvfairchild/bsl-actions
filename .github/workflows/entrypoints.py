import sys

from brainscore_core.submission import process_github_submission


if __name__ == '__main__':
    function = getattr(sys.modules[__name__], sys.argv[1])
    function(sys.argv[2])
