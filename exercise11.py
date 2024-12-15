import concurrent.futures


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


def split_string_by_separator(input_string, separator):
    """
    Divide una stringa in una lista basandosi su un separatore specificato.

    Args:
        input_string (str): La stringa da dividere.
        separator (str): Il separatore da utilizzare.

    Returns:
        list: Una lista di sottostringhe separate dal separatore.
    """
    if not separator:
        raise ValueError("Il separatore non può essere una stringa vuota.")

    return input_string.split(separator)


print("-----------------------------\nPART 1")

file_path = f"./inputs/11/input.txt"
file_content = read_file_to_string(file_path)

element_list = split_string_by_separator(file_content, ' ')
output_list = []

#2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2
#2097446912 14168 4048 0 40 48 0 40 48 80 96 2 8 6 7 6 0 3 2

cache = {}
sublists_cache = {}

def process_sublist(sublist):
    """
    Esegue il calcolo su una sottolista.
    """
    # Usa la cache per tutta la sottolista, se possibile
    sublist_key = tuple(sublist)
    if sublist_key in sublists_cache:
        return sublists_cache[sublist_key]

    output = []
    for element in sublist:
        # Verifica nella cache se l'elemento è già calcolato
        if element in cache:
            cached_result = cache[element]
            if isinstance(cached_result, list):
                output.extend(cached_result)
            else:
                output.append(cached_result)
            continue

        # Calcolo per l'elemento
        element_output = None
        element_int = int(element)  # Conversione solo una volta
        str_element = str(element)  # Conversione solo una volta

        if element_int == 0:
            element_output = '1'
        elif len(str_element) % 2 == 0:
            # Dividi l'elemento in due parti
            half_length = len(str_element) // 2
            left_part = int(str_element[:half_length])
            right_part = int(str_element[half_length:])
            element_output = [left_part, right_part]
        else:
            # Calcolo per valori dispari
            element_output = element_int * 2024

        # Memorizza i risultati
        if isinstance(element_output, list):
            output.extend(element_output)
        else:
            output.append(element_output)

        # Aggiorna la cache per il singolo elemento
        cache[element] = element_output

    # Memorizza la cache per l'intera sottolista
    sublists_cache[sublist_key] = output
    return output

def parallel_process(element_list, num_sublists):
    """
    Divide element_list in num_sublists parti e processa ogni parte in parallelo.
    """
    # Divide la lista in sottoliste
    chunk_size = len(element_list) // num_sublists
    sublists = [element_list[i:i + chunk_size] for i in range(0, len(element_list), chunk_size)]

    # Processa le sottoliste in parallelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_sublist, sublists)

    # Combina i risultati
    combined_results = []
    for result in results:
        combined_results.extend(result)

    return combined_results

from collections import Counter

def process_with_frequencies(element_list, iterations):
    """
    Processa una lista di elementi per un certo numero di iterazioni,
    ottimizzando l'uso della memoria tramite frequenze.

    Args:
        element_list (list): Lista iniziale di elementi (stringhe o numeri).
        iterations (int): Numero di iterazioni da simulare.

    Returns:
        Counter: Frequenza finale degli elementi dopo le iterazioni.
    """
    # Conta le occorrenze iniziali
    frequency = Counter(element_list)

    for _ in range(iterations):
        new_frequency = Counter()

        for element, count in frequency.items():
            element_int = int(element)
            str_element = str(element)

            if element_int == 0:
                # Caso: Elemento 0 -> Genera '1'
                new_frequency['1'] += count
            elif len(str_element) % 2 == 0:
                # Caso: Lunghezza pari -> Dividi in due parti
                half_length = len(str_element) // 2
                left_part = int(str_element[:half_length])
                right_part = int(str_element[half_length:])
                new_frequency[str(left_part)] += count
                new_frequency[str(right_part)] += count
            else:
                # Caso: Lunghezza dispari -> Moltiplica per 2024
                result = element_int * 2024
                new_frequency[str(result)] += count

        # Aggiorna la frequenza con i nuovi valori
        frequency = new_frequency

    return frequency

# Numero di iterazioni
iterations = 25

# Calcola le frequenze finali
final_frequencies = process_with_frequencies(element_list, iterations)

# BRUTE FORCE MODE
# for i in range(0, 25):
#     print(f"> round {i+1}")
#     for element in element_list:
#         if int(element) == 0:
#             output_list.append('1')
#         elif len(str(element)) % 2 == 0:
#             half_length = len(str(element)) // 2
#             left_part = int(str(element)[:half_length])
#             right_part = int(str(element)[half_length:])
#             output_list.append(left_part)
#             output_list.append(right_part)
#         else:
#             output_list.append(int(element)*2024)
#     element_list = output_list.copy()
#     output_list = []
    #print(' '.join([str(num) for num in element_list]))

print(f"\nSOLUTION --------------------\n")

# Mostra i risultati
print("Frequenze finali:")
for element, count in final_frequencies.items():
    print(f"{element}: {count}")

# Numero totale di elementi
total_elements = sum(final_frequencies.values())

print("-----------------------------\nPART 2")

element_list = split_string_by_separator(file_content, ' ')
output_list = []

iterations = 75

# Calcola le frequenze finali
final_frequencies = process_with_frequencies(element_list, iterations)

print(f"\nSOLUTION --------------------\n")

# Mostra i risultati
print("Frequenze finali:")
for element, count in final_frequencies.items():
    print(f"{element}: {count}")

# Numero totale di elementi
total_elements = sum(final_frequencies.values())

print(f"solution: {total_elements}\n")

