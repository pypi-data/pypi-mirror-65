import logging

from deid.dicom import get_identifiers, get_files, replace_identifiers
from deid.config import DeidRecipe

logger = logging.getLogger(__name__)


def de_identifier(input_folder, recipe_file, output_folder):
    """
    This function takes a list of files under the input folder, and by using DEID it scrubs the metadata to delete any
    PHI data. For more information go to:
    https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html
    :param input_folder: Folder that contains a list of dcm/nii files.
    :param recipe_file: File that contains all the recipe to de-identify specific type of files with respect to certain
    tag headers.
    :param output_folder: Folder under which all the files found under the input folder will be saved.
    :return: It returns a list of all of the files that had been de-identified successfully.
    """
    logger.info(f'-------------------------------------------- New De-identification Batch -----------------------'
                f'---------------------')
    logger.info(f'Input Path: {input_folder}')
    logger.info(f'Output Path: {output_folder}')
    recipe = DeidRecipe(deid=recipe_file)
    base_files = get_files(input_folder)
    brain_files = sorted(list(base_files))
    logger.info(f'Number of files found to de-identify: {len(brain_files)}')
    ids = get_identifiers(brain_files)
    updated_ids = dict()
    count = 0
    for image, fields in ids.items():
        fields['id'] = 'caoslab_filter'
        fields['source_id'] = "caoslab-image-%s" % count
        updated_ids[image] = fields
        count += 1

    cleaned_files_1 = replace_identifiers(dicom_files=brain_files,
                                          deid=recipe,
                                          ids=updated_ids,
                                          output_folder=output_folder,
                                          overwrite=True)

    logger.info(f'Total files cleaned in: {len(cleaned_files_1)}')
    percentage_correct = len(cleaned_files_1) / len(brain_files) * 100
    return cleaned_files_1, percentage_correct
