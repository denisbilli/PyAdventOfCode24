
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


def check_solution(rules, list):
    idx = 0
    for idx in range(0, len(list)):
        item1 = list[idx]
        #print(f" > item: {item1}")

        tail = list[idx + 1:]
        if rules.keys().__contains__(item1):
            item2 = rules[item1]
        else:
            item2 = []
        #print(f" > checking sublist {tail} in rules {item2}")

        if not is_list_contained(tail, item2):
            #print(" >>> ERR")
            return False, idx
    return True, idx


def swap_with_offset(lst, index, offset):
    """
    Swappa l'elemento corrente della lista con quello successivo di `offset` posizioni,
    se l'indice di destinazione è valido.

    Args:
        lst (list): La lista di elementi.
        index (int): L'indice dell'elemento corrente da swappare.
        offset (int): Numero di posizioni da swappare.

    Returns:
        None: La lista viene modificata inline.
    """
    target_index = index + offset
    # Controlla che l'indice di destinazione sia valido
    if 0 <= target_index < len(lst):
        lst[index], lst[target_index] = lst[target_index], lst[index]


def append_list(original, replacement, start):
    """
    Sostituisce gli elementi di una lista originale a partire da una posizione
    specificata con una nuova lista, rimuovendo gli elementi rimanenti.

    Args:
        original (list): La lista originale.
        replacement (list): La lista di sostituzione.
        start (int): L'indice da cui iniziare la sostituzione.

    Returns:
        None: La lista originale viene modificata inline.
    """
    original[start:] = replacement


def check_list(rules, list, swap_level):
    if not list:
        return False

    result = False
    idx = 0
    for idx in range(0, len(list)):
        result, good_numbers = check_solution(rules, list)
        print(f" > {list} result: {result} with {good_numbers} good numbers")

        if not result and good_numbers > 0:
            sublist = list[good_numbers:]
            print(f" > new sublist: {sublist}")
            swap_with_offset(sublist, idx, 1)
            print(f" > swap {idx} with +{1}: {sublist[idx]}<->{sublist[idx+1]}")
            print(f" > checking sublist: {sublist}")
            if check_list(rules, sublist, 1):
                append_list(list, sublist, good_numbers)
                print(f" >> new list: {list}")
                return True
            return False
        elif not result and good_numbers == 0:
            swap_with_offset(list, idx, swap_level)
            print(f" > swap {idx} with +{swap_level}: {list[idx]}<->{list[idx+swap_level]}")
            print(f" > checking sublist: {list}")
            return check_list(rules, list, swap_level+1)
        else:
            result = True
            return result

    return result


# region PART 1
print("-----------------------------\nPART 1")

file_path = f"./inputs/05/input.txt"
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
    result, _ = check_solution(rules, update)

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

# endregion

# region PART 2
print("-----------------------------\nPART 2")
print(f"incorrect_updates: {incorrect_updates}")

correct_updates = []

for update in incorrect_updates:
    print(f"\n\nchecking {update}")

    update_copy = update.copy()

    result = check_list(rules, update_copy, 1)

    if not result:
        print(f"@ {update_copy} NOT OK")
    else:
        print(f"@ {update_copy} OK !!!")
        correct_updates.append(update_copy)

print(f"\nSOLUTION --------------------\n")
print(f"correct_updates: {correct_updates}")

sum = 0
for update in correct_updates:
    middle_elem = int(len(update) / 2)
    sum += int(update[middle_elem])
    print(update[middle_elem])

print(f"result: {sum}")

# endregion