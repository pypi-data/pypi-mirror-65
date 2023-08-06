import sys
import subprocess

from azureml.designer.core.model.constants import ModelSpecConstants, DEV_OPS_EXTRA_INDEX_URL_PREFIX
from azureml.studio.core.logger import get_logger
from azureml.studio.core.package_info import PACKAGE_NAME
from azureml.studio.core.utils.yamlutils import dump_to_yaml_file

logger = get_logger(__name__)

PYTHON_VERSION = "{major}.{minor}.{micro}".format(major=sys.version_info.major,
                                                  minor=sys.version_info.minor,
                                                  micro=sys.version_info.micro)


def _run_install_cmds(cmds, command_name):
    logger.info(" ".join(cmds))
    result = subprocess.run(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if result.returncode == 0:
        logger.info(f"Finished to install {command_name} dependencies.")
    else:
        logger.warning(f"Failed to install {command_name} dependencies, returncode={result.returncode}.")
    logger.debug(f"stdout: {result.stdout}")
    if result.stderr:
        logger.warning(f"stderr: {result.stderr}")


def _get_current_pip_package_version_dict() -> dict:
    """Run pip freeze and return a dict of {package_name: version}"""

    result = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            universal_newlines=True)
    content = result.stdout
    # In format package_name==version
    lines = content.strip().split('\n')
    version_dict = {row[0]: row[1] for row in [line.split('==') for line in lines]}
    return version_dict


def _regulate_core_version_in_pip_install_list(pip_dependencies_to_install, current_pip_package_version_dict) -> list:
    """Inject current azureml-designer-core into pip dependencies and remove existing core dependency if exists
    to prevent alteration
    """
    if not pip_dependencies_to_install:
        return []
    if PACKAGE_NAME not in current_pip_package_version_dict:
        logger.warning(f"{PACKAGE_NAME} doesn't exist in current environment, skip core version fixing.")
        return pip_dependencies_to_install.copy()
    else:
        version_str = current_pip_package_version_dict[PACKAGE_NAME]
        injection = f"{PACKAGE_NAME}=={version_str}"
        # For test env where package is from DevOps feed and postxxx suffix exists
        if 'post' in current_pip_package_version_dict[PACKAGE_NAME]:
            dev_ops_extra_index_url_provided = False
            for line in pip_dependencies_to_install:
                if line.startswith(DEV_OPS_EXTRA_INDEX_URL_PREFIX):
                    dev_ops_extra_index_url_provided = True
                    break
            if not dev_ops_extra_index_url_provided:
                logger.warning(f"DevOps extra-index-url not provided, skip core version fixing in test env.")
                return pip_dependencies_to_install.copy()

        logger.info(f"Injected {injection} into pip dependency and removed original "
                    f"azureml-designer-core dependency if exists.")
        return [dep for dep in pip_dependencies_to_install if not dep.startswith(PACKAGE_NAME)] + [injection]


# Temporary workaround to reconstruct the python environment in training phase.
# Should deprecate when Module team support reading the conda.yaml in Model Folder and build image according to that
class RemoteDependencyManager(object):

    def __init__(
        self,
        additional_conda_channels: list = None,
        additional_conda_deps: list = None,
        additional_pip_deps: list = None
    ):
        self.conda_channels = ["defaults"] + (additional_conda_channels or [])
        self.conda_dependencies = [f"python={PYTHON_VERSION}"] + (additional_conda_deps or [])
        self.pip_dependencies = additional_pip_deps or []

    def save(self, artifact_path, overwrite_if_exists=True):
        conda_env = {
            "name": ModelSpecConstants.CONDA_ENV_NAME,
            "channels": self.conda_channels,
            "dependencies": self.conda_dependencies + [{"pip": self.pip_dependencies}]
        }
        conda_file_path = artifact_path / ModelSpecConstants.CONDA_FILE_NAME
        if conda_file_path.exists() and not overwrite_if_exists:
            raise FileExistsError(f"Target path {conda_file_path} exists. "
                                  f"Set overwrite_if_exists=True if you want to overwrite it.")
        dump_to_yaml_file(conda_env, conda_file_path)
        logger.info(f"Saved conda to {conda_file_path}")

    def load(self, conda: dict):
        if isinstance(conda["channels"], list):
            self.conda_channels = conda["channels"]
        else:
            self.conda_channels = [conda["channels"]]

        for entry in conda["dependencies"]:
            if isinstance(entry, dict) and "pip" in entry:
                self.pip_dependencies = entry["pip"]
            # TODO: Use regex for precision
            elif entry.startswith(("python=", "python>", "python<")):
                pass
            else:
                self.conda_dependencies.append(entry)
        logger.debug(f"conda_channels = {', '.join(self.conda_channels)}")
        logger.debug(f"conda_dependencies = {', '.join(self.conda_dependencies)}")
        logger.debug(f"pip_dependencies = {', '.join(self.pip_dependencies)}")

    def install(self):
        if not self.conda_dependencies:
            logger.info("No conda dependencies to install")
        else:
            conda_cmds = ["conda", "install", "-y"]
            for channel in self.conda_channels:
                conda_cmds += ["-c", channel]
            conda_cmds += self.conda_dependencies
            _run_install_cmds(conda_cmds, command_name="conda")

        if not self.pip_dependencies:
            logger.info("No pip dependencies to install")
        else:
            current_pip_package_version_dict = _get_current_pip_package_version_dict()
            regulated_pip_dependencies = _regulate_core_version_in_pip_install_list(
                self.pip_dependencies, current_pip_package_version_dict)
            if regulated_pip_dependencies:
                pip_cmds = ["pip", "install"] + regulated_pip_dependencies
                _run_install_cmds(pip_cmds, "pip")

        result = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True)
        logger.debug(f"pip freeze result:\n{result.stdout}")
