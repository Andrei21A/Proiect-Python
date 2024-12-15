import os
import subprocess
import sys


def matches_pattern(file_name, pattern, case_insensitive):
    if case_insensitive:
        file_name = file_name.lower()
        pattern = pattern.lower()
        
    if '*' in pattern:
        parts = pattern.split('*')
        prefix = parts[0]
        if len(parts) > 1:
            suffix = parts[1]
            print(suffix)
        else:
            suffix = ''
        return file_name.startswith(prefix) and file_name.endswith(suffix)
    elif '?' in pattern:
        if len(file_name) != len(pattern):
            return False
        for i in range(len(pattern)):
            if pattern[i] != '?' and pattern[i] != file_name[i]:
                return False
        return True

    return file_name == pattern


def execute_command(command, file_path):
    command = command.replace('{}', f'"{file_path}"')
    print(command)
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Comanda nu a fost executata pentru {file_path}. Eroare: {e}")


def find_files(directory='.', case_insensitive=False, name=None, exec_command=None):
    try:
        found = 0
        for root, dirs, files in os.walk(directory):
            # Excluderea directoarelor sau fisierelor ce incep cu '.'
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]

            # Filtrarea fisierelor
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

                # Cazul in care "-exec" este mentionat
                if exec_command:
                    execute_command(exec_command, file_path)

        # Cazul in care nu este gasit niciun fisier
        if found == 0:
            print(f"No files matching '{name}' were found in {directory}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    directory = os.getcwd()  # Default directory ul curent
    name = None
    case_insensitive = False
    exec_command = None

    # Cazul in care sunt prea putine argumente
    if len(sys.argv) < 2:
        print("Comanda ar trebui sa fie: python3 find.py [directory] -name <pattern> | -iname <pattern> | -exec <command>")
        sys.exit(1)

    # Cazul in care e mentionat sau nu directory-ul
    if sys.argv[1] != '' and sys.argv[1] not in ['-name', '-iname', '-exec']:
        directory = sys.argv[1]

        # Cazul in care directory-ul nu exista
        if not os.path.exists(directory):
            print(f"Directory '{directory}' does not exist.")
            sys.exit(1)

        # Cazul in care nu sunt prea putine argumente
        if len(sys.argv) < 4:
            print("Comanda ar trebui sa fie: python3 find.py [directory] -name <pattern> | -iname <pattern> | -exec <command>")
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
            print("Flag incorect. Foloseste -name, -iname, or -exec.")
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
            print("Flag incorect. Foloseste -name, -iname, or -exec.")
            sys.exit(1)

    # Prelucrarea argumentului exec inainte de a fi folosit
    if len(sys.argv) >= 5 and '-exec' in sys.argv:
        exec_index = sys.argv.index('-exec')
        exec_command = ' '.join(sys.argv[exec_index + 1:])

    # Apelarea functiei
    find_files(directory, case_insensitive, name, exec_command)
