#from distutils.core import setup, Extension
from setuptools import setup, Extension

def main():
    setup(
        py_modules=["functiontrace"],
        ext_modules=[
            Extension("_functiontrace", ["_functiontrace.c", "mpack/mpack.c"])
        ]
    )

if __name__ == "__main__":
    main()
