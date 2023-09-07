import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path


def run_featureCount(args: tuple) -> str:
    """
    :param args: tuple of key and value from the dictionary
    :return: path to the temporary bed file with feature counts

    The function runs bedtools intersect and featureCount
    """
    # key is in the format of (path_to_regions_bed, path_to_reads_bed, spikein, overlap_type)
    # value is in the format of {name: [[position_left, position_right, size_left, size_right]]}
    key, value = args
    path_to_regions_bed, path_to_reads_bed, spikein, overlap_type = key
    json_data = json.dumps(value)

    # create a random name for the temporary bed file
    random_name_1, random_name_2 = str(uuid.uuid4()), str(uuid.uuid4())
    temp_data_bedtools, temp_data = Path(Path.cwd(), random_name_1 + ".bed"), Path(
        Path.cwd(), random_name_2 + ".bed"
    )

    # run bedtools
    cmd = f"bedtools intersect -a {path_to_regions_bed} -b {path_to_reads_bed} -wa -wb > {temp_data_bedtools}"
    completed_process = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)

    if completed_process.returncode != 0:
        error_message = completed_process.stderr.decode("utf-8")
        print(f"{error_message}")
        sys.exit(1)

    # call featureCount
    if os.name == "posix":  # Linux or macOS
        featureCount = "./featureCount"
    elif os.name == "nt":  # Windows
        featureCount = "./featureCount.exe"

    subprocess.run(
        [
            featureCount,
            temp_data_bedtools,
            json_data,
            temp_data,
            overlap_type,
            str(spikein),
        ]
    )

    # remove the temporary bed file
    os.remove(temp_data_bedtools)

    return temp_data


def consolidate_files(results: list, output_directory: str) -> None:
    """
    :param results: list of paths to the temporary bed files with counts
    :param output_directory: path to the output directory
    :return: None

    The function consolidates the temporary bed files with counts into one bed file
    """
    basename = os.path.basename(output_directory)
    try:
        basename[-4] != ".txt" or basename[-4] != ".bed"
    except IndexError:
        output_directory = output_directory + ".bed"

    files = [open(file, "r") for file in results]
    with open(output_directory, "w") as output_file:
        for lines in zip(*files):
            for line in lines:
                joined = [(line.split(), idx) for idx, line in enumerate(lines)]
                final_line = ""
                for each_line, idx in joined:
                    if idx == 0:
                        for each in each_line:
                            final_line += each + "\t"
                    if idx > 0:
                        for each in each_line[1:]:
                            final_line += each + "\t"
            output_file.write(final_line + "\n")

    for f in files:
        f.close()

    # remove the temporary bed files
    for path in results:
        os.remove(path)


def parse_args():
    """
    Get arguments and make multiple checks
    """

    parser = argparse.ArgumentParser(
        prog="dff_feature_count.py",
        description="The program tallies the number of DFF-Seq reads with specific length ranges that overlap within a designated genomic interval",
    )
    parser.add_argument(
        "regions",
        type=str,
        help="Bed file of genomic regions of chosen length. The regions should be of even length and the MaxTSS should be in the middle of the region.",
    )
    parser.add_argument(
        "-f",
        dest="fragments_range_size_position",
        metavar="\b",
        nargs="*",
        required=True,
        action="append",
        help="Singular fragment dataset, followed by position range, followed by fragment range\
                        Examples: -f /home/reads.bed 20 1000 400 800 \
                                 -f /home/reads.bed 20 1000 400 800 20 1000 300 600",
    )

    parser.add_argument(
        "-n",
        dest="names",
        metavar="\b",
        type=str,
        required=True,
        nargs="*",
        help="Provide a name for each feature (space sperated). The names should be in the same order as the features provided with -f. ",
    )
    parser.add_argument(
        "-t",
        dest="overlap_type",
        choices=["centers", "full", "partial"],
        required=True,
        help="Type of overlap: center, full, or partial",
    )
    parser.add_argument(
        "-o",
        dest="output_dir",
        metavar="\b",
        type=str,
        required=True,
        nargs=1,
        help="Path to output, for example -o /home/user/dir",
    )
    parser.add_argument(
        "-s",
        dest="spikein",
        metavar="\b",
        type=float,
        required=False,
        nargs="*",
        default=[1.0],  # Setting the default value to 1.0
        help="Correction factors - must be 1 per dataset (-f) space separated. The correction factors should be in the same order as the datasets provided with -f.",
    )

    args = parser.parse_args()
    regions = args.regions
    reads_sizes_positions = args.fragments_range_size_position
    output_directory = args.output_dir[0]
    names = args.names
    spikein = args.spikein
    overlap_type = args.overlap_type

    # checks
    # check that names are unique
    if len(names) != len(set(names)):
        sys.exit("The names must be unique")
    # check if the regions file exists
    if not os.path.isfile(regions):
        sys.exit("The regions file does not exist")
    if not os.path.isfile(reads_sizes_positions[0][0]):
        sys.exit("The reads file does not exist")
    # check if the output directory exists
    try:
        dir_name = os.path.dirname(output_directory)
        if not os.path.isdir(dir_name):
            sys.exit("The output directory does not exist")
    except:
        sys.exit("The output directory does not exist")
    # spike-in values must be 1 per dataset
    if len(spikein) != len(reads_sizes_positions):
        sys.exit(
            "The number of spike-in values must be equal to the number of datasets"
        )

    to_analyze_dict = {}
    count = 0
    for idx, dataset in enumerate(reads_sizes_positions):
        reads_bed_path = dataset[0]
        features = dataset[1:]

        if len(features) % 4 != 0:
            sys.exit("Each length and positions must have two values")
        for feature in range(0, len(features), 4):
            position_left, position_right, size_left, size_right = (
                int(features[feature]),
                int(features[feature + 1]),
                int(features[feature + 2]),
                int(features[feature + 3]),
            )
            # add to dictionary
            key = (regions, reads_bed_path, spikein[idx], overlap_type)
            sub_key = names[count]
            if key not in to_analyze_dict:
                to_analyze_dict[key] = {sub_key: []}

            if sub_key not in to_analyze_dict[key]:
                to_analyze_dict[key][sub_key] = []

            to_analyze_dict[key][sub_key].extend(
                [[position_left, position_right], [size_left, size_right]]
            )
            count += 1

    total_features = int(sum([len(x[1:]) / 4 for x in reads_sizes_positions]))
    if total_features != len(names):
        sys.exit("The number of names must be equal to the number of features")

    return (
        to_analyze_dict,
        output_directory,
    )


if __name__ == "__main__":
    (
        to_analyze_dict,
        output_directory,
    ) = parse_args()

    # iterate over the dictionary, dictionry will be in the form:
    # {(path_to_bed, spikein): {name: [[position_left, position_right, size_left, size_right]]}}
    final_dict = {}
    data = [(key, value) for key, value in to_analyze_dict.items()]

    # run featureCount
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(run_featureCount, data))

    # merge files
    consolidate_files(results, output_directory)
