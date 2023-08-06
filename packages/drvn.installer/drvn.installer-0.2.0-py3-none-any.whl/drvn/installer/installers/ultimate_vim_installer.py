import sys
import logging

import drvn.installer._utils as utils

def install(is_install_drvn_configs):
	logging.info("Installing ultimate_vim ...")
	_install_prerequisites()
	_install_ultimate_vim()
	_install_extra_plugins()
	if is_install_drvn_configs:
		_install_drvn_configs()

def _install_prerequsites():
	utils.try_cmd("sudo apt-get install -y cmake")

	python = _get_current_python_interpreter()
	utils.try_cmd(f"{python} -m pip install python-language-server")
	utils.try_cmd(f"{python} -m pip install mypy")

def _install_ultimate_vim():
	utils.try_cmd("git clone --depth=1 " + "https://github.com/amix/vimrc.git ~/.vim_runtime")
	utils.try_cmd("sh ~/.vim_runtime/install_awesome_vimrc.sh")

def _install_extra_plugins():
    utils.try_cmd(
        "cd ~/.vim_runtime/my_plugins && "
        + "git clone https://github.com/ycm-core/YouCompleteMe.git && "
        + "cd YouCompleteMe && "
        + "git submodule update --init --recursive"
    )
    utils.try_cmd(
        "cd ~/.vim_runtime/my_plugins/YouCompleteMe && "
        + "./install.py --clang-completer"
    )

def _install_drvn_configs():
	pass # TODO: implement

def _get_current_python_interpreter():
	major = sys.version_info.major
	minor = sys.version_info.minor
	return f"python{major}.{minor}"