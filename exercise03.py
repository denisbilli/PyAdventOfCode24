import re


def export_regex_matches_with_groups(pattern, text):
    """
    Esporta tutti i match di una regex da un input, includendo i gruppi catturati.

    Args:
        pattern (str): La regex da utilizzare per il matching.
        text (str): Il testo su cui cercare i match.

    Returns:
        list: Una lista di tuple, ciascuna contenente i gruppi del match.
              Se non ci sono gruppi, restituisce i match completi.
    """
    try:
        matches = re.findall(pattern, text)
        # Verifica se la regex cattura gruppi
        if matches and isinstance(matches[0], tuple):
            return [list(match) for match in matches]  # Converte ogni tuple in lista
        else:
            return matches  # Restituisce i match semplici se non ci sono gruppi
    except re.error as e:
        print(f"Errore nella regex: {e}")
        return []


def export_regex_matches_with_positions(pattern, text):
    """
    Esporta tutti i match di una regex da un input, inclusi i gruppi e la posizione nel testo.

    Args:
        pattern (str): La regex da utilizzare per il matching.
        text (str): Il testo su cui cercare i match.

    Returns:
        list: Una lista di dizionari con i dettagli dei match, gruppi e posizione.
              Ogni dizionario contiene:
                - 'match': Il testo del match.
                - 'groups': I gruppi catturati (se presenti).
                - 'start': L'indice di inizio del match.
                - 'end': L'indice di fine del match.
    """
    try:
        results = []
        for match in re.finditer(pattern, text):
            results.append({
                'match': match.group(0),
                'groups': match.groups(),
                'start': match.start(),
                'end': match.end()
            })
        return results
    except re.error as e:
        print(f"Errore nella regex: {e}")
        return []


def read_file_to_string(file_path):
    """
    Legge un intero file e restituisce il contenuto come stringa.

    Args:
        file_path (str): Il percorso del file da leggere.

    Returns:
        str: Il contenuto del file come stringa.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Errore: Il file '{file_path}' non esiste.")
        return ""
    except IOError as e:
        print(f"Errore durante la lettura del file: {e}")
        return ""

print("-----------------------------\nPART 1")

file_path = f".\\inputs\\03\\input.txt"
regex = r"mul\(([0-9]+),([0-9]+)\)"

file_content = read_file_to_string(file_path)
max_value = len(file_content)

risultati = export_regex_matches_with_positions(regex, file_content)
print(f"risultati: {risultati}")

sum = 0
for ris in risultati:
    elem1 = int(ris["groups"][0])
    elem2 = int(ris["groups"][1])

    mul = elem1*elem2
    sum += mul


print("-----------------------------\nRESULT 1:")
print(f"sum: {sum}")

# ---------------------------------

print("-----------------------------\nPART 2")

do_regex = r"do\(\)"
do_list = export_regex_matches_with_positions(do_regex, file_content)

dont_regex = r"don't\(\)"
dont_list = export_regex_matches_with_positions(dont_regex, file_content)

print(f"do_list: {do_list}")
print(f"dont_list: {dont_list}")

infinito_positivo = float('inf')
infinito_negativo = float('-inf')


def get_first_match_after(matches, value):
    """
    Restituisce il primo match nella lista dove 'start' è maggiore di un valore specificato.

    Args:
        matches (list): Lista di dizionari con dettagli dei match (contenenti 'start').
        value (int): Il valore rispetto al quale confrontare il campo 'start'.

    Returns:
        dict or None: Il primo dizionario nella lista dove 'start' > value,
                      oppure None se nessun match soddisfa la condizione.
    """
    for match in matches:
        if int(match['start']) > value:
            return match
    return None


def exists_in_list(matches, value):
    for match in matches:
        if int(value["start"]) >= int(match['start']) and int(value["end"]) <= int(match['end']):
            return True
    return False


dos = []
donts = []
risultati_without_donts = risultati.copy()


for item in do_list:
    match = get_first_match_after(dont_list, int(item["start"]))

    end_value = max_value
    if match is not None:
        end_value = match["end"]

    dos.append({
        "start": int(item["start"]),
        "end": end_value
        })

for item in dont_list:
    match = get_first_match_after(do_list, int(item["start"]))

    end_value = max_value
    if match is not None:
        end_value = match["start"]

    donts.append({
        "start": int(item["start"]),
        "end": end_value
    })


print(f"dos: {dos}")
print(f"donts: {donts}")

print(f"risultati_without_donts {len(risultati_without_donts)}: {risultati_without_donts}")

print("-----------------------------\nCHECK:")
for idx in range(0, len(risultati)):
    item = risultati[idx]
    result = exists_in_list(donts, risultati[idx])
    print(f"checking: {item} => {result}")
    if result:
        print(f" > removing: {item} {idx}")
        risultati_without_donts.remove(item)
        print(f" > risultati_without_donts {len(risultati_without_donts)}: {risultati_without_donts}")

print("-----------------------------\nRESULTS:")
print(f"risultati_without_donts {len(risultati_without_donts)}: {risultati_without_donts}")


sum = 0
for ris in risultati_without_donts:
    elem1 = int(ris["groups"][0])
    elem2 = int(ris["groups"][1])

    mul = elem1*elem2
    sum += mul


print("-----------------------------\nRESULT 2:")
print(f"sum: {sum}")