import os
import datetime
import shutil
from pathlib import Path
from unicodedata import name

# Path to check
directory = "M:\\MMC\\ArchivBestellungen\\"

# debug_mode
debug_mode = 0

# file_directory | file_name
not_correct_files = [], []

# get the current project path
def get_project_root() -> Path:
    return Path(__file__).parent.parent

def log(message, onlyPrintWhenDebug=0):
    # return when debug_mode is not active
    if onlyPrintWhenDebug == 1 and debug_mode == 0:
        return

    log_file_path = os.path.join(get_project_root(), "log.txt")
    log_file = open(log_file_path, "a", encoding="utf8")

    date = datetime.datetime.now()
    current_time = date.strftime("%H:%M:%S")
    formated_actual_date = "%s.%s.%s %s" % (date.day, date.month, date.year, current_time)

    print("%s: %s" % (formated_actual_date, message))
    log_file.write("%s: %s" % (formated_actual_date, message))
    log_file.write("\n")
    log_file.close()

def check_files():
    log("function check_files", 1)
    for file_directory, dirs, files in os.walk(directory, topdown=False):
        for current_file_name in files:
            current_file_name_splitted = current_file_name.split(".")

            # when file is not a pdf
            if not current_file_name_splitted[1] == "pdf":
                log("Continue - file is not a pdf: %s\\%s" % (file_directory, current_file_name), 1)
                continue

            # when file is double order and is correct
            if "(" in current_file_name_splitted[0]:
                current_file_name_with_bracket = current_file_name_splitted[0].split("(")
                if len(current_file_name_with_bracket[0]) == 5:
                    log("Continue - file is correct: %s\\%s" % (file_directory, current_file_name), 1)
                    continue

            if len(current_file_name_splitted[0]) >= 6:
                log("Found - file is not correct: %s\\%s" % (file_directory, current_file_name))
                not_correct_files[0].append("%s\\" % file_directory)
                not_correct_files[1].append("%s" % current_file_name)

def check_directorys():
    log("function check_directorys", 1)
    for file_directory, dirs, files in os.walk(directory, topdown=False):
        for current_dir_name in dirs:

            # loop through not correct file names
            for i in range(len(not_correct_files[1])):
                current_file_name = not_correct_files[1][i]

                # when directory name is equal to first digits of not correct file name
                if current_dir_name == current_file_name[:len(current_dir_name)]:

                    log("Found directory %s - %s\\%s" % (current_dir_name, not_correct_files[0][i], current_file_name))

                    file_src = "%s\\%s" % (not_correct_files[0][i], current_file_name)
                    file_dest = "%s\\%s\\%s" % (directory, current_dir_name, current_file_name)

                    log(file_src)
                    log(file_dest)

                    file_move = shutil.move(file_src, file_dest)
                    log("File moved from %s to: %s" % (file_src, file_move))

log("START SKRIPT")
check_files()
check_directorys()
print("END")