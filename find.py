import os
import sys


def find(directory='/Users', file_name=None, case_insensitive=False, extension=None):
    try:
        found = 0
        for root, dirs, files in os.walk(directory):
            
            # Daca numele fisierului este specificat
            if file_name:
                file_name_lower = file_name.lower()

                # Daca extensia este specificata
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
                        original_file_name = next(
                            (f for f in filtered_files if f.lower() == file_name_lower), None
                        )
                        if original_file_name:
                            found = 1
                            print(os.path.join(root, original_file_name))

            # Daca doar extensia este specificata
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

    # Analiza argumentelor
    if len(sys.argv) < 2:
        print("Comanda ar trebui sa fie:")
        print("find.py <directory> [<numele fisierului>] [-name / -iname] [extensie]")
        sys.exit(1)

    # Verificare pentru numărul și tipul argumentelor
    if len(sys.argv) >= 2:
        # Dacă primul argument este un director
        if '/' in sys.argv[1]:
            directory = sys.argv[1]

        # Dacă primul argument este o extensie
        elif sys.argv[1].startswith('.'):
            extension = sys.argv[1]

        # Dacă primul argument este numele unui fișier
        elif not sys.argv[1].startswith('-'):
            file_name = sys.argv[1]

    if len(sys.argv) >= 3:
        # Dacă al doilea argument este -iname sau -name
        if sys.argv[2] == '-iname':
            case_insensitive = True
        elif sys.argv[2] == '-name':
            case_insensitive = False
        # Dacă al doilea argument este o extensie
        elif sys.argv[2].startswith('.'):
            extension = sys.argv[2]
        # Dacă al doilea argument este numele unui fișier
        else:
            file_name = sys.argv[2]

    if len(sys.argv) >= 4:
        # Dacă al treilea argument este o extensie
        if sys.argv[3].startswith('.'):
            extension = sys.argv[3]

    if len(sys.argv) > 4:
        print("Comanda ar trebui sa fie:")
        print("find.py <directory> [<numele fisierului>] [-name / -iname] [extensie]")
        sys.exit(1)

    find(directory, file_name, case_insensitive, extension)
