#    Copyright 2020 Division of Medical Image Computing, German Cancer Research Center (DKFZ), Heidelberg, Germany
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from batchgenerators.utilities.file_and_folder_operations import subfiles, join
from hd_gliomouse.utils import blockPrint, enablePrint
blockPrint()
from nnunet.inference.predict import predict_cases
enablePrint()
import argparse
from hd_gliomouse.paths import folder_with_parameter_files
from hd_gliomouse.setup_hd_gliomouse import maybe_download_weights


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_folder", type=str, required=True,
                        help="folder with input files. All .nii.gz files in this folder will be processed.")
    parser.add_argument("-o", "--output_folder", type=str, required=True,
                        help="output folder. This is there the resulting segmentations will be saved. Cannot be the "
                             "same folder as the input folder. If output_folder does not exist "
                             "it will be created")
    parser.add_argument("-p", "--processes", default=4, type=str, required=False,
                        help="number of processes for data preprocessing and nifti export. You should not have to "
                             "touch this. So don't unless there is a clear indication that it is required. Default: 4")
    parser.add_argument('--keep_existing', default=True, required=False, action='store_false',
                        help="set to False to keep segmentations in output_folder and continue where you left off "
                             "(useful if something crashes). If this flag is not set, all segmentations that may "
                             "already be present in output_folder will be overwritten.")

    args = parser.parse_args()
    input_folder = args.input_folder
    output_folder = args.output_folder
    processes = args.processes
    keep_existing = args.keep_existing

    maybe_download_weights()

    # we must generate a list of input filenames
    nii_files = subfiles(input_folder, suffix='.nii.gz', join=False)
    input_list_of_lists = [[join(input_folder, i)] for i in nii_files]

    output_filenames = [join(output_folder, i) for i in nii_files]

    predict_cases(folder_with_parameter_files, input_list_of_lists, output_filenames, (0, 1, 2, 3, 4), False, processes,
                  processes, None, True, None, not keep_existing, False, 2, None, 3, 0)


if __name__ == "__main__":
    main()
