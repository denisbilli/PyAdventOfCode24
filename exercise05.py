
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


def swap_with_next(lst, index):
    """
    Swappa l'elemento corrente della lista con quello successivo, se non è l'ultimo elemento.

    Args:
        lst (list): La lista di elementi.
        index (int): L'indice dell'elemento corrente da swappare.

    Returns:
        None: La lista viene modificata inline.
    """
    if index < len(lst) - 1:  # Controlla che non sia l'ultimo elemento
        lst[index], lst[index + 1] = lst[index + 1], lst[index]


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


def check_solution(rules, update):
    idx = 0
    for idx in range(0, len(update)):
        item1 = update[idx]
        print(f" > item: {item1}")

        tail = update[idx + 1:]
        if rules.keys().__contains__(item1):
            item2 = rules[item1]
        else:
            item2 = []
        print(f" > checking sublist {tail} in rules {item2}")

        if not is_list_contained(tail, item2):
            print(" >>> ERR")
            return False, idx
    return True, idx


# per ogni update
for update in section2:
    print(f"checking: {update}")
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


print("-----------------------------\nPART 2")
print(f"incorrect_updates: {incorrect_updates}")

correct_updates = []


def find_solution(rules, list):
    if not list:
        return

    result, good_numbers = check_solution(rules, list)

    if good_numbers > 0:
        new_list = list[good_numbers:]
        return find_solution(rules, new_list)


# per ogni update
for update in incorrect_updates:
    print(f"checking: {update}")
    result = False
    idx = 0

    old_good_numbers = 0
    good_numbers = 0
    improving_solution = False
    update_copy = update.copy()

    while not result:
        result, good_numbers = check_solution(rules, update_copy)
        improving_solution = good_numbers - old_good_numbers

        if not result:
            if improving_solution > 0 or (good_numbers == 0 and old_good_numbers == 0):
                idx += (good_numbers - idx)
            else:
                idx -= 1
            swap_with_next(update_copy, idx)
            print(f"swapped {idx} with next > now checking {update_copy}")
            if idx == len(update_copy) - 1:
                idx = 0
            else:
                idx += 1
        else:
            update = update_copy

        old_good_numbers = good_numbers

    if not result:
        print(f"@ {update} NOT OK")
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