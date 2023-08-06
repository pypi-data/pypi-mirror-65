import json

from mpp.src.utils import constants as cst


def write_installer(mpp_config):
    """
    Writes the PyInstaller spec file and the NSIS file

    Args:
        mpp_config (dict): project parameters
    """

    # Rewrite the specs file
    with open(f"installer/installer.spec", "w") as f:
        f.write(cst.pattern_spec % mpp_config)
    # Rewrite the nsis file
    with open(f"installer/installer.nsi", "w") as f:
        f.write(cst.pattern_nsis % mpp_config)



def write_mpp_config(mpp_config):
    """
    Writes the project's configuration file

    Args:
        mpp_config (dict): project parameters
    """

    # Write the config file
    with open(".mpp_config", "w") as f:
        json.dump(mpp_config, f, indent=4)
