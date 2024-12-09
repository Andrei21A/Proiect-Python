import os
import subprocess
import sys


# Function to match files based on patterns with wildcards
def matches_pattern(file_name, pattern, case_insensitive):
    if case_insensitive:
        file_name = file_name.lower()
        pattern = pattern.lower()

    # Handling wildcard '*' (matching anything)
    if '*' in pattern:
        parts = pattern.split('*')
        prefix = parts[0]
        suffix = parts[1] if len(parts) > 1 else ''
        return file_name.startswith(prefix) and file_name.endswith(suffix)

    # Handling wildcard '?' (matching single characters)
    elif '?' in pattern:
        if len(file_name) != len(pattern):
            return False
        for i in range(len(pattern)):
            if pattern[i] != '?' and pattern[i] != file_name[i]:
                return False
        return True

    # No wildcards present, do a direct comparison
    return file_name == pattern

# Function to execute a shell command with placeholders
def execute_command(command, file_path):
    command = command.replace('{}', f'"{file_path}"')
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute command on {file_path}. Error: {e}")

# Function to search for files and run commands based on patterns
def find_files(directory='.', case_insensitive=False, name=None, exec_command=None):
    try:
        found = 0
        for root, dirs, files in os.walk(directory):
            # Exclude hidden directories and files
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]

            matching_files = []

            if name:
                if case_insensitive:
                    matching_files = [f for f in files if matches_pattern(f, name, True)]
                else:
                    matching_files = [f for f in files if matches_pattern(f, name, False)]

            for f in matching_files:
                found = 1
                file_path = os.path.join(root, f)
                relative_path = os.path.relpath(file_path, start=directory)

                print(relative_path)

                # If -exec command is provided, run it
                if exec_command:
                    execute_command(exec_command, file_path)

        if found == 0:
            print(f"No files matching '{name}' were found in {directory}")

    except Exception as e:
        print(f"Error: {e}")

# Parse command-line arguments
if __name__ == '__main__':
    directory = os.getcwd()  # Default to current working directory
    name = None
    case_insensitive = False
    exec_command = None

    if len(sys.argv) < 2:
        print("Usage: python find.py [directory] -name <pattern> | -iname <pattern> | -exec <command>")
        sys.exit(1)

    # Check if a directory argument was provided
    if sys.argv[1] != '' and sys.argv[1] != '-name' and sys.argv[1] != '-iname' and sys.argv[1] != '-exec':
        
        directory = sys.argv[1]

        if not os.path.exists(directory):
            print(f"Directory '{directory}' does not exist.")
            sys.exit(1)
        if len(sys.argv) < 4:
            print("Usage: python find.py <directory> -name <pattern> | -iname <pattern>")
            sys.exit(1)

        flag = sys.argv[2]
        if flag == '-name':
            name = sys.argv[3]
        elif flag == '-iname':
            name = sys.argv[3]
            case_insensitive = True
        elif flag == '-exec':
            exec_command = ' '.join(sys.argv[3:])
        else:
            print("Invalid flag. Use -name, -iname, or -exec.")
            sys.exit(1)

    else:
        flag = sys.argv[1]
        if flag == '-exec':
            exec_command = ' '.join(sys.argv[2:])
        elif flag == '-name':
            name = sys.argv[2]
        elif flag == '-iname':
            name = sys.argv[2]
            case_insensitive = True
        else:
            print("Invalid flag. Use -name, -iname, or -exec.")
            sys.exit(1)
    if '-exec' in sys.argv[4]:
        exec_command = ' '.join(sys.argv[5:])
    # Call the search function
    print(exec_command)
    find_files(directory, case_insensitive, name, exec_command)
