# fMRI Anonymizer

This project contains a series of scripts that perform 2 essential steps:

1. De-Identification
2. De-Facing

The main purpose of this porject is to have an "all-purpose" application that can automatize the whole anonymization process on MRI, fMRI data. This includes DICOM, and NIFTI formats. 

This application follows a "best-effort" approach in order to comply with [HIPAA regulations](https://www.hhs.gov/hipaa/for-professionals/privacy/laws-regulations/index.html).

## How to install it?

In order to use this packeage, you will need to use the following command (recommended to use it in a separate environment - like conda or venv):

`pip install fmri_anonymizer`

## How to use it?

This is pretty simple, you have 2 ways to use it:

`python -m fmri_anonymizer -i <INPUT_FOLDER> --dicom --anonymize --deface YES -o <OUTPUT_FOLDER>`

Or:

`fmri_anonymizer -i <INPUT_FOLDER> --dicom --anonymize --deface YES -o <OUTPUT_FOLDER>`

## How to get some help?

Simply type:

`python -m fmri_anonymizer -h`



H4ppy H4ck1n6!