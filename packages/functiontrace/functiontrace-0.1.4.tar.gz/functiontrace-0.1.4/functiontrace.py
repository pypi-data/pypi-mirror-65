import argparse
import os
import shutil
import sys
import tempfile
import _functiontrace

PYTHON_TEMPLATE = """#!/bin/sh

# The location of this wrapper, which must be in the path.
FUNCTIONTRACE_WRAPPER_PATH=$(dirname $(which {python}))

# Remove the wrapper directory from PATH, allowing us to find the real Python.
PATH=$(echo "$PATH" | sed -e "s#$FUNCTIONTRACE_WRAPPER_PATH:##")

exec $(which {python}) -m functiontrace "$@"
"""

def setup_dependencies():
    # We need the functiontrace-server installed and locatable in order to
    # trace anything.
    if shutil.which("functiontrace-server") is None:
        print("Unable to find `functiontrace-server` in the current $PATH.", file=sys.stderr)
        print("See https://functiontrace.com#installation for installation instructions.", file=sys.stderr)
        sys.exit(1)

    # Generate a temp directory to store our wrappers in.  We'll temporarily
    # add this directory to our path.
    tempdir = tempfile.mkdtemp(prefix="py-functiontrace")
    os.environ["PATH"] = tempdir + os.pathsep + os.environ["PATH"]

    # Generate wrappers for the various Python versions we support to ensure
    # they're included in our PATH.
    wrap_pythons = ["python", "python3", "python3.6", "python3.7", "python3.8"]
    for python in wrap_pythons:
        with open(os.path.join(tempdir, python), "w") as f:
            f.write(PYTHON_TEMPLATE.format(python=python))
            os.chmod(f.name, 0o755)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trace a script's execution.")
    parser.add_argument('--trace-memory', action="store_true", help="""Trace
                        memory allocations/frees when enabled.  This may add
                        tracing overhead, so is disabled by default.""")
    parser.add_argument('--output_dir', type=str, default=os.getcwd(),
                        help="The directory to output trace files to")
    parser.add_argument("script", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if len(args.script) == 0:
        print("Can't profile without a target")
        parser.print_help()
        sys.exit(1)

    # Ignore ourselves, keeping sys.argv looking reasonable as the child script
    # will expect it to be sane.
    sys.argv[:] = args.script

    # Read in the script to be executed and compile their code.
    # NOTE: This looks pretty questionable, but it's effectively equivalent to
    # what cProfile is doing, so it can't be that bad.
    # TODO: I think this breaks __file__, which various scripts actually use.
    sys.path.insert(0, os.path.dirname(sys.argv[0]))
    with open(sys.argv[0], 'rb') as fp:
        code = compile(fp.read(), sys.argv[0], 'exec')

    # Ensure we're setup to be able to run.
    setup_dependencies()

    # Setup our tracing environment, including configuring tracing features.
    if args.trace_memory:
        _functiontrace.config_tracememory()
    _functiontrace.begin_tracing(args.output_dir)

    # Run their code now that we're tracing.
    exec(code)
else:
    # We've been imported for some reason.  Make sure we're setup to work
    # properly, then begin tracing.
    setup_dependencies()
    _functiontrace.begin_tracing(os.getcwd())
