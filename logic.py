import random

def sort_data_by_init(data): # Sorting logic
    # Should sort form the highest initiative number to lowest.
    # If initiative scores are the same, it should order from the greatest dexterity modifier to least
    sorted_data = sorted(data, key=lambda x: (int(x['init']), int(x['dex'])), reverse=True)

    # If both the initiative and dexterity modifiers are the same then the order is randomized
    i = 0
    while i < len(sorted_data) - 1:
        start = i
        # Ranges the numbers with the same data
        while i < len(sorted_data) - 1 and sorted_data[i]['init'] == sorted_data[i + 1]['init'] and sorted_data[i]['dex'] == sorted_data[i + 1]['dex']:
            i += 1
        if start < i:
            # Randomizes the order of matching dexterity modifiers and initiative scores
            sublist = sorted_data[start:i + 1]
            random.shuffle(sublist)
            sorted_data[start:i + 1] = sublist
        i += 1

    return sorted_data
