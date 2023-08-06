from setuptools import setup, find_packages, Extension
import sysconfig
import platform

_DEBUG = False

extra_compile_args = sysconfig.get_config_var('CFLAGS')
if extra_compile_args is None:
    extra_compile_args = list()
else:
    extra_compile_args = extra_compile_args.split()

if platform.system() == "Windows":
    extra_compile_args += ["/MP", "/Wall"]
    if _DEBUG:
        extra_compile_args += ["/Zi"]
    else:
        extra_compile_args += ["/O2"]
else:
    extra_compile_args += ["-Wall"]
    if _DEBUG:
        extra_compile_args += ["-g", "-Og"]
    else:
        extra_compile_args += ["-O3"]

print("Extra compile args:", extra_compile_args)

minibox_ext = Extension("persty.minibox",
                        ["persty/minibox.c"],
                        extra_compile_args=extra_compile_args)
util_ext = Extension("persty.c_util",
                     ["persty/c_util.c"],
                     extra_compile_args=extra_compile_args)

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = "persty",
    version = "1.0.0",
    author="Gabriele Beltramo",
    author_email="gabri.beltramo@gmail.com",
    description = "Implementation of Minibox and Delauany edges algorithms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages = find_packages(exclude=['*test']),
    ext_modules = [minibox_ext, util_ext],
    url="https://github.com/gbeltramo/persty",
    license='GPLv3',
    install_requires=['numpy'],
    keywords='topology data analysis, minibox graph, delaunay graph'
)
