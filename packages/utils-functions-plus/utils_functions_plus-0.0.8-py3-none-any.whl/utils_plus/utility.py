import logging
import shutil
import sys
import traceback
import os

USE_LOGGING = False


def init_log(project_name, use_logging=False):
    global USE_LOGGING
    USE_LOGGING = use_logging
    if USE_LOGGING:
        path = f'c:\\Temp\\{project_name}.log'
        if not os.path.isfile(path):
            open(path, "w").write("")

        logging.basicConfig(
            filename=path,
            level=logging.DEBUG,
            format=f'[{project_name}] %(asctime)-15s %(levelname)-7.7s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
        )


def print_log(*message):
    if USE_LOGGING:
        logging.debug(message)
    else:
        print(message)


def print_error():
    logging.error('-' * 60)
    traceback.print_exc(file=sys.stdout)
    formatted_lines = traceback.format_exc()
    if USE_LOGGING:
        logging.error(formatted_lines)
    else:
        print(formatted_lines)
    logging.error('-' * 60)
    return formatted_lines


def waiting(tasks):
    for task in tasks:
        task.start()

    for task in tasks:
        task.join()


def rename_files(path, index, generate_path):
    attaches = []
    for f in os.listdir(path):
        if os.path.isdir(str(path) + "/" + f):
            attaches += rename_files(str(path) + "/" + f, index, generate_path)
        else:
            new_name = generate_path(index)
            try:
                shutil.move(str(path) + "/" + f, new_name)
                attaches.append(new_name)
            except:
                print_error()
            index += 1
    return attaches
