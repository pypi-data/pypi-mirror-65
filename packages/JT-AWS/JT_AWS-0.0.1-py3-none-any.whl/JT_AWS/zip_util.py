import os
import zipfile


def ZipFolder(folder_path: str):
    """
    Compresses an entire folder into a zip archive of the same lambda_name

    :param folder_path: Path to the folder to be compressed
    :return: The path to the generated zip file
    """
    zip_file_path = "{}.zip".format(folder_path.strip('/\\'))
    zip_file = zipfile.ZipFile(zip_file_path, mode='w+', compression=zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(folder_path):
        for file in file_names:
            file_path = '\\'.join([dir_path, file])
            zip_path = '/'.join(file_path.split('\\')[1:])
            zip_file.write(file_path, arcname=zip_path)
    zip_file.close()
    return zip_file_path


def AddFile(file_path: str, zip_path: str):
    """
    Adds a single file to the root directory of a zip file.

    :param file_path: Path to the file to be added.
    :param zip_path: Path to the zip file to be added to.
    :return:
    """
    with zipfile.ZipFile(zip_path, mode='a') as zip_file:
        file_name = os.path.basename(file_path)
        zip_file.write(file_path, arcname=file_name)