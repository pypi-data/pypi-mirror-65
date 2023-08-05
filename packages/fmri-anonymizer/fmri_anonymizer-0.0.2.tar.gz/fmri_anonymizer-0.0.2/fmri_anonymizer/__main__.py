import argparse
import traceback

import dicom2nifti
import logging
import os
import pydeface.utils as pdu
import time

from ttictoc import TicToc
from fmri_anonymizer.directory_replicator import replicate_structure
from fmri_anonymizer.file_searcher import walk_through
from fmri_anonymizer.deidentifier import de_identifier

__author__ = "Hugo Angulo"
__copyright__ = "Copyright 2020, CaosLab"
__credits__ = ["Hugo Angulo"]
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Hugo Angulo"
__email__ = "hugoanda@andrew.cmu.edu"
__status__ = "Production"


def str2bool(arg):
    if isinstance(arg, bool):
        return arg
    if arg.lower() in ('YES', 'Yes', 'yes', 'Y', 'y', 'TRUE', 'True', 'true', 'T', 't', '1', ''):
        return True
    elif arg.lower in ('NO', 'No', 'no', 'N', 'n', 'FALSE', 'False', 'false', 'F', 'f', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value not recognized.')


def get_parser():
    """
    This is the parser for the arguments coming from STDIN. It parses all the input.
    :return: parser
    """

    docstr = ("""Example:
                 python -m fmri_anonymizer -i <root_input_path> -d <flag_for_dicoms> -n <flag_for_nifti> 
                 -a <flag_for_anonymization> -f <flag_for_defacing> -o <output_path>""")
    epilog = (f"This is a wrapper project created to de-identify DICOM and NIFTI files. Also, (if you want) it can \n"
              f"perform defacing on the MRI data.\n"
              f"It uses the best-effort approach. So, don't take for granted that all the files had been \n"
              f"de-identified and/or defaced. Please verify some of the files that were problematic or were detected \n"
              f"as an error during the process. You will find the log file with all of this information \n"
              f"in your current working directory. \n"
              f"Powered by: CAOsLab @ CMU \n"
              f"Author: {__author__} \n"
              f"Email: {__email__}")
    parser = argparse.ArgumentParser(prog='fmri_anonymizer', description=docstr, epilog=epilog, allow_abbrev=False,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('-i', '--input', type=str, help='Path where all the DICOM files can be found.',
                        required=True)
    parser.add_argument('-d', '--dicom', type=str2bool, nargs='?', help='Flag to enable DICOM files discovery.',
                        const=True, default=True, required=True)
    parser.add_argument('-n', '--nifti', type=str2bool, nargs='?', help='Flag to enable NIFTI files discovery',
                        const=True, default=False, required=False)
    parser.add_argument('-a', '--anonymize', type=str2bool, nargs='?', help='Flag to enable PHI metadata scrubbing.',
                        const=True, default=True, required=True)
    parser.add_argument('-f', '--deface', type=str2bool, nargs='?', help='Flag to enable defacing on MRI data',
                        const=True, default=False, required=False)
    parser.add_argument('-o', '--output', type=str, help='Folder to put the converted files.',
                        required=True)
    return parser


def main(argv=None):
    # This section adds logging capabilities to this script.
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - PID[%(process)d] - [%(levelname)s]: %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_log = "fmri_anonymizer" + time.strftime("%Y-%m-%d__%H_%M_%S") + ".log"
    file_handler = logging.FileHandler(file_log)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    dicom_formats = ['.dcm', '.ima', '.IMA']
    nifti_formats = ['nii', 'nii.gz']
    t = TicToc()
    t.tic()
    parser = get_parser()
    args = parser.parse_args(argv)
    input_path = args.input
    output_path = args.output
    dcm_flag = args.dicom
    nii_flag = args.nifti
    deid_flag = args.anonymize
    deface_flag = args.deface
    dcm_files = list()
    nii_files = list()

    # Defining some variables
    current_path = os.path.abspath(os.path.dirname(__file__))

    if not dcm_flag and not nii_flag:
        logger.info(f'You have not enabled DICOM and/or NIFTI files recognition. You have to enable one of them.')
        return None
    if not os.path.isdir(input_path):
        logger.info(f'The input folder does not exists. Please try again with the proper root folder.')
        return None
    if not deid_flag and not deface_flag:
        logger.info(f'You have not enabled the de-identification nor the defacing.\n Process finished!')
        return None
    logger.info(f'Starting the process...')
    logger.info(f'Creating a replica folder structure of the input in the output path...')
    # This has to create a replica of the input in the output
    directory_map = replicate_structure(input_path=input_path, output_path=output_path)

    # We have to look for dicom and or nifti files
    if dcm_flag:
        logger.info(f'Searching DICOM files...')
        dcm_files = walk_through(input_path, '.dcm', '.ima', '.IMA')
        logger.info(f'Total dicom files discovered: {len(dcm_files)}')

    if nii_flag:
        logger.info(f'Searching NIFTI files...')
        nii_files = walk_through(input_path, 'nii', 'nii.gz')
        logger.info(f'Total NIFTI files discovered: {len(nii_files)}')

    if deid_flag:
        logger.info(f'Now, the system will de-identify all the files found...')
        dcm_cleaned = list()
        if dcm_files.__len__() > 0:
            dcm_folders = dict()
            dcm_recipe = os.path.join(current_path, "../util/deid.dicom")
            for dcm_file in dcm_files:
                _path, _file = os.path.split(dcm_file)
                if directory_map[_path] not in dcm_folders:
                    list_cleaned, percentage_clean = de_identifier(input_folder=_path, recipe_file=dcm_recipe,
                                                                   output_folder=directory_map[_path])
                    dcm_cleaned.append(list_cleaned)
                    dcm_folders[directory_map[_path]] = True
                    logger.info(f'The current directory has been de-identified {percentage_clean:.2f}%')

    logger.info(f'The De-Identification process is done!')
    if deface_flag:
        # TODO: Transform all the DICOM cleaned into nifti files.
        nii_de_identified = dict()
        nii_defaced = dict()
        for k, v in dcm_folders.items():
            try:
                dicom2nifti.convert_directory(dicom_directory=k, output_folder=k, compression=True, reorient=True)
            except:
                logger.error(f'An error has been detected while transforming the dcm files in: {k}')
                traceback.print_exc()
                pass
            nii_de_identified[k] = walk_through(k, 'nii', 'nii.gz')
            if len(nii_de_identified[k]) > 0:
                for nifti in nii_de_identified[k]:
                    if nifti.endswith(tuple(nifti_formats)):
                        nii_defaced[nifti] = False
        # TODO: Deface the niftis.
        for k, v in nii_de_identified.items():
            for each in v:
                try:
                    pdu.deface_image(infile=each, forcecleanup=True, force=True)
                    pdu.cleanup_files()
                    if each in nii_defaced:
                        nii_defaced[each] = True
                except:
                    logger.error(f'An error has been detected while defacing the file: {v}')
                    traceback.print_exc()
                    pass
        logger.info(f'Percentage files defaced: {sum(nii_defaced.values()) / len(nii_defaced):.3f}%')
        logger.info(f'The defacing process has finished!')

    t.toc()
    logger.info(f'Process finished. Time elapsed: {t.elapsed:.6f}s')


if __name__ == '__main__':
    main()
