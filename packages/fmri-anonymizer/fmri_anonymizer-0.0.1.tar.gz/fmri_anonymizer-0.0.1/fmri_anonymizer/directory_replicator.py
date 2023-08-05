import logging
import os

logger = logging.getLogger(__name__)


def replicate_structure(input_path, output_path):
    """
    This function creates a replica of the folder structure under input_path, and then copies that structure under
    the output_path folder.
    :param input_path: Source folder structure.
    :param output_path: Target folder to copy source folder structure.
    :return: It returns a hash-map with the input_path sub-folder and its equivalent location under output_path.
    """
    dir_mapper = dict()
    for dir_path, dir_name, file_names in os.walk(input_path):
        new_structure = os.path.join(output_path, dir_path[len(input_path) + 1:])
        if not os.path.isdir(new_structure):
            os.mkdir(new_structure)
            logger.info(f'Path created: {new_structure}')
            if dir_path not in dir_mapper:
                dir_mapper[dir_path] = new_structure
        else:
            logger.error(f'Already existing folder.')
    return dir_mapper
