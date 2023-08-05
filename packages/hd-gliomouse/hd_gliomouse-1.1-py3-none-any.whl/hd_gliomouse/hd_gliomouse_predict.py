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

from hd_gliomouse.utils import blockPrint, enablePrint
blockPrint()
from nnunet.inference.predict import predict_cases
enablePrint()
import argparse
from hd_gliomouse.paths import folder_with_parameter_files
from hd_gliomouse.setup_hd_gliomouse import maybe_download_weights


def main():
    parser = argparse.ArgumentParser(description="This script will allow you to predict a single case with hd_gliomouse. "
                                                 "If you have multiple cases, please use hd_gliomouse_predict_folder (this one "
                                                 "will be substantially faster for multiple cases because we can "
                                                 "interleave preprocessing, GPU prediction and nifti export.")

    parser.add_argument("-i", type=str, required=True,
                        help="input file")
    parser.add_argument("-o", "--output_file", type=str, required=True,
                        help="output filename. Must end with .nii.gz")

    args = parser.parse_args()
    inp = args.i
    output_file = args.output_file

    maybe_download_weights()

    predict_cases(folder_with_parameter_files, [[inp, ]], [output_file], (0, 1, 2, 3, 4), False, 1, 1, None, True,
                  None, True)


if __name__ == "__main__":
    main()

