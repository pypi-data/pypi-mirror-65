import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile

import mpp.src.utils.constants as cst


def shell_exec_as_user():
    """
    Download ShellExecAsUser.dll for NSIS:
    https://nsis.sourceforge.io/mediawiki/images/c/c7/ShellExecAsUser.zip

    Returns:
        str: patht to the downloaded file
    """

    def get_zip_name(url):
        return url.split("/")[-1]

    def get_dll_name(url):
        url, _ = os.path.splitext(url)
        return f"{url}.dll"


    # URL and file names
    url = cst.link_shellexecasuser
    zipname = get_zip_name(url)
    dllname = get_dll_name(zipname)
    dl_output = os.path.dirname(cst.path_dll_shellexecasuser)

    # Temporary download directory
    dir_path = tempfile.mkdtemp()
    dl_path = os.path.join(dir_path, zipname)

    # Download the file and unzip it
    try:
        with urllib.request.urlopen(url) as response:
            with open(dl_path, "wb") as output:
                shutil.copyfileobj(response, output)
        with zipfile.ZipFile(dl_path) as zf:
            zf.extract(dllname, dl_output)
    except urllib.error.URLError as err:
        sys.exit("No internet connection.")

    return cst.path_dll_shellexecasuser
