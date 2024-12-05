
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


def parse_custom_string(input_string):
    """
    Elabora una stringa per produrre due elementi:
    1. Una lista di liste di 2 elementi ciascuna, separati da "|".
    2. Una lista di liste di N elementi, separati da ",".

    La stringa è separata da una riga vuota che distingue le due sezioni.

    Args:
        input_string (str): La stringa da elaborare.

    Returns:
        tuple: Un tuple contenente due elementi:
            - Lista di liste di 2 elementi (separati da "|").
            - Lista di liste di N elementi (separati da ",").
    """
    # Divide le due sezioni usando la riga vuota come separatore
    parts = input_string.strip().split("\n\n")

    # Verifica che ci siano esattamente due parti
    if len(parts) != 2:
        raise ValueError("La stringa deve contenere esattamente due sezioni separate da una riga vuota.")

    # Prima sezione: lista di liste di 2 elementi separati da "|"
    section1 = [line.split("|") for line in parts[0].splitlines()]

    # Seconda sezione: lista di liste di N elementi separati da ","
    section2 = [line.split(",") for line in parts[1].splitlines()]

    return section1, section2


def list_to_grouped_dict(input_list):
    """
    Converte una lista di liste in un dizionario raggruppato:
    - La chiave è il primo elemento di ogni sotto-lista.
    - Il valore è una lista di tutti i secondi elementi associati alla chiave.

    Args:
        input_list (list): Lista di liste, dove ogni lista contiene esattamente 2 elementi.

    Returns:
        dict: Dizionario con chiavi uniche e valori come liste accorpate.
    """
    grouped_dict = {}
    for key, value in input_list:
        if key not in grouped_dict:
            grouped_dict[key] = []
        grouped_dict[key].append(value)
    return grouped_dict


def is_list_contained(left_list, right_list):
    """
    Verifica se tutti gli elementi della lista di sinistra sono contenuti
    nella lista di destra.

    Args:
        left_list (list): La lista di sinistra da controllare.
        right_list (list): La lista di destra in cui cercare gli elementi.

    Returns:
        bool: True se tutti gli elementi di left_list sono in right_list, altrimenti False.
    """
    from collections import Counter
    # Conta le occorrenze di ciascun elemento nelle due liste
    left_counter = Counter(left_list)
    right_counter = Counter(right_list)

    # Verifica se ogni elemento della lista di sinistra ha abbastanza occorrenze nella lista di destra
    for element, count in left_counter.items():
        if right_counter[element] < count:
            return False
    return True


print("-----------------------------\nPART 1")

file_path = f".\\inputs\\05\\test.txt"
file_content = read_file_to_string(file_path)

section1, section2 = parse_custom_string(file_content)

# print(f"ordering rules: {section1}")
print(f"updates: {section2}")

# lista delle regole => dizionario regole
rules = list_to_grouped_dict(section1)
correct_updates = []
incorrect_updates = []

print(f"ordering rules: {rules}")

# per ogni update
for update in section2:
    # print(f"checking: {update}")
    result = True

    for idx in range(0, len(update)):
        item1 = update[idx]
        # print(f" > item: {item1}")

        tail = update[idx+1:]
        if rules.keys().__contains__(item1):
            item2 = rules[item1]
        else:
            item2 = []
        # print(f" > checking sublist {tail} in rules {item2}")

        if not is_list_contained(tail, item2):
            # print(" >>> ERR")
            result = False
            break

    if not result:
        print(f"@ {update} NOT OK")
        incorrect_updates.append(update)
    else:
        print(f"@ {update} OK !!!")
        correct_updates.append(update)

print(f"\nSOLUTION --------------------\n")
print(f"correct_updates: {correct_updates}")

sum = 0
for update in correct_updates:
    middle_elem = int(len(update) / 2)
    sum += int(update[middle_elem])
    print(update[middle_elem])

print(f"result: {sum}")


print("-----------------------------\nPART 2")
print(f"incorrect_updates: {incorrect_updates}")