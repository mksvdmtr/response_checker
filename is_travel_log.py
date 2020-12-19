import sys


def is_travel_log(log_file_path: str) -> bool:
    try:
        with open('travelask_log_paths.txt') as travel_log_paths_file:
            travel_log_paths = travel_log_paths_file.read().splitlines()
            return log_file_path in travel_log_paths

    except FileNotFoundError:
        print('File travelask_log_paths.txt not found')
        sys.exit(1)
