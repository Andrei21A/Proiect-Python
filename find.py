import os
import sys


def find(directory='/Users', file_name=None, case_insensitive=False, extension=None):
    try:
        found = 0
        for root, dirs, files in os.walk(directory):
            
            # Daca numele fișierului este specificat
            if file_name:
                file_name_lower = file_name.lower()

                # Daca extensia este specificată
                filtered_files = files
                if extension:
                    extension_lower = extension.lower()
                    filtered_files = [f for f in files if f.lower().endswith(extension_lower)]

                # Cazurile daca este sau nu case-sensitive
                if not case_insensitive:
                    if file_name in filtered_files:
                        found = 1
                        print(os.path.join(root, file_name))
                else:
                    if file_name_lower in map(str.lower, filtered_files):
                        original_file_name = [f for f in filtered_files if f.lower() == file_name_lower][0]
                        found = 1
                        print(os.path.join(root, original_file_name))

            # Daca doar extensia este specificată
            elif extension:
                for f in files:
                    if f.lower().endswith(extension.lower()):
                        found = 1
                        print(os.path.join(root, f))

            # Daca doar directory-ul este specificat
            else:
                for f in files:
                    found = 1
                    print(os.path.join(root, f))

        if found == 0:
            if file_name:
                print(f"{file_name} nu a fost găsit în {directory}")
            elif extension:
                print(f"Nu au fost găsite fișiere cu extensia {extension} în {directory}")
            else:
                print(f"Nu au fost găsite fișiere în {directory}")

    except IndexError:
        print(f"{file_name or 'File'} nu a fost găsit în {directory}")
    except Exception as e:
        print(f"Eroare: {e}")


if __name__ == '__main__':
    directory = '/Users'  # Directorul de start
    file_name = None
    case_insensitive = False
    extension = None

    # Analiza argumentelor
    if len(sys.argv) < 2:
        print("Comanda ar trebui să fie:")
        print("find.py <directory> [<numele fisierului>] [-name / -iname] [extensie]")
        sys.exit(1)

    # Cazul în care doar extensia este specificată
    if len(sys.argv) == 2 and sys.argv[1].startswith('.'):
        extension = sys.argv[1]

    # Cazul în care doar numele fișierului este specificat
    elif len(sys.argv) == 2 and '/' not in sys.argv[1]:
        file_name = sys.argv[1]
        
    # daca directoy-ul este specificat
    elif len(sys.argv) == 2 and '/' in sys.argv[1]:
        directory = sys.argv[1]
    # Cazul în care sunt specificate mai multe argumente
    elif len(sys.argv) >= 3:
        directory = sys.argv[1]

        if sys.argv[2] == "-iname":
            case_insensitive = True
        elif sys.argv[2] == "-name":
            case_insensitive = False
        elif '.' in sys.argv[2]:
            extension = sys.argv[2]
        else:
            file_name = sys.argv[2]

        if len(sys.argv) >= 4:
            extension = sys.argv[3]

    find(directory, file_name, case_insensitive, extension)
