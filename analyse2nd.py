
import re

def analyze_logs(input_file):

    patterns = {
        "DEBUG": re.compile(r"\[DEBUG\]"),
        "ERROR": re.compile(r"\[ERROR\]"),
        "CRITICAL": re.compile(r"\[CRITICAL\]")
    }

    output_files = {
        "DEBUG": open("debug.log", "w"),
        "ERROR": open("error.log", "w"),
        "CRITICAL": open("critical.log", "w")
    }

    try:
        with open(input_file, "r") as f:
            for line in f:
                for level, pattern in patterns.items():
                    if pattern.search(line):
                        output_files[level].write(line)
                        break  
    except FileNotFoundError:
        print("Error: Log file not found.")
    finally:
        for file in output_files.values():
            file.close()

analyze_logs("feature.log")
