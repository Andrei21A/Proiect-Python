import os
import sys


def find(directory='/Users', file_name=None, case_insensitive=False, extension=None):
    try:
        found = 0
        for root, dirs, files in os.walk(directory):
            
            # daca numele fisierului este specificat
            if file_name:
                file_name_lower = file_name.lower()

                # daca extensia este specificata
                filtered_files = files
                if extension:
                    extension_lower = extension.lower()
                    filtered_files = [f for f in files if f.lower().endswith(extension_lower)]

                # cazurile daca este sau nu case-sensitive
                if not case_insensitive:
                    if file_name in filtered_files:
                        found = 1
                        print(os.path.join(root, file_name))
                else:
                    if file_name_lower in map(str.lower, filtered_files):
                        original_file_name = next(
                            (f for f in filtered_files if f.lower() == file_name_lower), None
                        )
                        if original_file_name:
                            found = 1
                            print(os.path.join(root, original_file_name))

            # daca doar extensia este specificata
            elif extension:
                for f in files:
                    if f.lower().endswith(extension.lower()):
                        found = 1
                        print(os.path.join(root, f))

            # daca doar directory-ul este specificat
            else:
                for f in files:
                    found = 1
                    print(os.path.join(root, f))

        if found == 0:
            if file_name:
                print(f"{file_name} nu a fost gasit in {directory}")
            elif extension:
                print(f"Nu au fost gasite fisiere cu extensia {extension} in {directory}")
            else:
                print(f"Nu au fost gasite fisiere in {directory}")

    except Exception as e:
        print(f"Eroare: {e}")


if __name__ == '__main__':
    directory = '/Users'  # Directorul de start
    file_name = None
    case_insensitive = False
    extension = None

    if len(sys.argv) < 2:
        print("Comanda ar trebui sa fie:")
        print("find.py <directory> [<numele fisierului>] [-name / -iname] [extensie]")
        sys.exit(1)

    # daca directory-ul este specificat
    if len(sys.argv) >= 2:
        directory = sys.argv[1]

    # Cazurile pentru argumentele -name, -iname, si extensia
    if len(sys.argv) >= 3:
        if sys.argv[2] in ['-name', '-iname']:
            if sys.argv[2] == '-iname':  # Cazul pentru -iname
                case_insensitive = True
            if len(sys.argv) >= 4:
                file_name = sys.argv[3]  # Seteaza numele fisierului daca este specificat
        elif '.' in sys.argv[2]:  # Cazul in care este specificata doar extensia
            extension = sys.argv[2]
        else:  # Cazul in care doar numele fisierului este specificat
            file_name = sys.argv[2]

    # Extensia este specificata ca al patrulea argument
    if len(sys.argv) >= 5:
        extension = sys.argv[4]

    # Verifica daca sunt prea multe argumente
    if len(sys.argv) > 5:
        print("Comanda ar trebui sa fie:")
        print("find.py <directory> [<numele fisierului>] [-name / -iname] [extensie]")
        sys.exit(1)

    find(directory, file_name, case_insensitive, extension)
