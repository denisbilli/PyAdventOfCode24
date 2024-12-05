

def split_file_into_lists(file_path):
    # Liste per memorizzare le colonne
    column1 = []
    column2 = []

    # Legge il file riga per riga
    with open(file_path, 'r') as file:
        for line in file:
            # Splitta ogni riga in due valori
            parts = line.strip().split()
            if len(parts) == 2:  # Verifica che ci siano due colonne
                column1.append(int(parts[0]))  # Aggiunge alla prima lista
                column2.append(int(parts[1]))  # Aggiunge alla seconda lista

    return column1, column2

# Esempio di utilizzo
file_path = f".\\inputs\\01\\input.txt"

list1, list2 = split_file_into_lists(file_path)

print(list1)
print(list2)

print(f"list1: {len(list1)}")
print(f"list2: {len(list2)}")

list1.sort()
list2.sort()

print(list1)
print(list2)

print(f"list1 after sort: {len(list1)}")
print(f"list2 after sort: {len(list2)}")

summary = []
occurrences = {}

for idx in range(0, len(list1)):
    summary.append(abs(list1[idx]-list2[idx]))

    item = list2[idx]
    if occurrences.__contains__(item):
        occurrences[item] += 1
    else:
        occurrences[item] = 1

print(f"summary: {summary}")
print(f"summary length: {len(summary)}")
print(f"occurrences: {occurrences}")

sum = 0
for idx in range(0, len(summary)):
    sum += summary[idx]

print(f"sum: {sum}")

sum = 0
for idx in range(0, len(list1)):
    item = list1[idx]
    if occurrences.__contains__(item):
        sum += item * occurrences[item]

print(f"similarity: {sum}")

