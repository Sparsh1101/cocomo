from collections import defaultdict
from django.conf import settings
import os
import json
import math


# This function takes in certain paramters where
# username: is used to locate the directory where the project has been uploaded on the server
# software_project_type: is used to know which type of project is it in the cocomo basic model
# init_time: the time in months taken to build the project
# init_person: no of developers that worked on the project
def processor(username, software_project_type, init_time, init_persons):
    all_files = []  # Stores the path to every file in the project
    LOC = 0  # Lines of Code
    KLOC = 0  # Kilo Lines of Code

    base_dir = os.path.join(
        settings.BASE_DIR, "media/" + username
    )  # This is the root at which the project directory is located

    # Following loops goes through the whole project directory and stores the path to every file in all_files list
    for root, directory, files in os.walk(base_dir, topdown=True):
        for file in files:
            all_files.append(root + "/" + file)

    # Loading the json file which contains the comment syntax for every language
    with open(
        os.path.join(settings.BASE_DIR, "main/comment_syntax.json"), "r"
    ) as json_file:
        comment_syntax = json.load(json_file)

    # Loop that runs thorugh every file in the project
    for file in all_files:

        # Retreiving the comment syntax for this specific file type
        file_comment_syntax = defaultdict()
        file_extension = "." + file.split("/")[-1].split(".")[-1]
        if file_extension in comment_syntax.keys():
            file_comment_syntax = comment_syntax[file_extension]

        # Opening the file
        with open(file, "r") as a_file:

            # Initializing some basic variables
            multi_line_comment_enabled = False
            multi_line_comment_end = ""

            try:  # Try block to make sure that only files in UTF-8 code are processed
                for line in a_file:
                    is_comment_line = False
                    stripped_line = line.strip()

                    # Checking if the line is empty
                    if stripped_line == "":
                        continue

                    # Checking for comments
                    if file_comment_syntax:
                        # Checking if this line is the end of a multi line comment
                        # that has been initiated
                        if multi_line_comment_enabled:
                            if (
                                stripped_line[: len(multi_line_comment_end)]
                                == multi_line_comment_end
                                or stripped_line[-len(multi_line_comment_end) :]
                                == multi_line_comment_end
                            ):
                                multi_line_comment_enabled = False
                            continue

                        # Checking for single line comments
                        if "single" in file_comment_syntax.keys():
                            for single_comment_type in file_comment_syntax["single"]:
                                if (
                                    stripped_line[: len(single_comment_type)]
                                    == single_comment_type
                                ):
                                    is_comment_line = True
                                    break
                            if is_comment_line:
                                continue

                        # Checking for multi line comments
                        if "multi" in file_comment_syntax.keys():
                            for multi_comment_type in file_comment_syntax["multi"]:
                                if (
                                    stripped_line[: len(multi_comment_type["start"])]
                                    == multi_comment_type["start"]
                                ):
                                    is_comment_line = True
                                    # Checking if the multiline comment ended in the same line
                                    # or extends to further lines
                                    if (
                                        stripped_line[-len(multi_comment_type["end"]) :]
                                        != multi_comment_type["end"]
                                    ):
                                        multi_line_comment_enabled = True
                                        multi_line_comment_end = multi_comment_type[
                                            "end"
                                        ]

                    # If not a comment line then increasing the count of LOC
                    if not is_comment_line:
                        LOC += 1

                    # If LOC increase over 1000 then updating KLOC
                    if LOC > 1000:
                        KLOC += LOC // 1000
                        LOC = LOC % 1000

            except:
                continue

    # Generating the final KLOC from the leftover LOC after all the files are scanned
    KLOC += LOC / 1000

    # Defining all the cocomo basic model constants
    cocomo_basic_model_constants = {
        "organic": {"a": 2.4, "b": 1.05, "c": 2.5, "d": 0.38},
        "semi detached": {"a": 3, "b": 1.12, "c": 2.5, "d": 0.35},
        "embedded": {"a": 3.6, "b": 1.2, "c": 2.5, "d": 0.32},
    }

    constants = cocomo_basic_model_constants[
        software_project_type
    ]  # Constants for the provided project type

    # Calculating the effort, time and persons that should have been used according to cocomo
    cocomo_effort = constants["a"] * (KLOC) ** constants["b"]
    cocomo_time = constants["c"] * (cocomo_effort) ** constants["d"]
    cocomo_persons = math.ceil(cocomo_effort / cocomo_time)

    # Calculating the efficiency of time and persons according to cocomo
    # over the time and person already used for the following project
    time_efficiency = ((init_time - cocomo_time) * 100) // cocomo_time
    persons_efficiency = ((init_persons - cocomo_persons) * 100) // cocomo_persons

    # Returning all the calculated result
    return [KLOC, cocomo_time, cocomo_persons, time_efficiency, persons_efficiency]
