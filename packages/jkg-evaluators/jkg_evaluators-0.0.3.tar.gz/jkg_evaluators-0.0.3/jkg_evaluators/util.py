import os
import zipfile
from typing import Optional


def zipdir_walk(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def get_code_nb_cell(
    code="", metadata=None, outputs=None, execution_count=None
):
    return {
        "cell_type": "code",
        "source": [code],
        "metadata": metadata or {},
        "outputs": outputs or [],
        "execution_count": execution_count,
    }


def get_md_nb_cell(md="", metadata=None):
    return {
        "cell_type": "markdown",
        "source": [md],
        "metadata": metadata or {},
    }


def zip_dir(
    zip_dir_path: str, dir_to_zip: str, zip_file_name: Optional[str] = None
):
    zip_file_path = os.path.join(zip_dir_path, "{}.zip".format(zip_file_name))
    zipf = zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED)
    zipdir_walk(dir_to_zip, zipf)
    zipf.close()
