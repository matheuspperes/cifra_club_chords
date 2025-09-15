from difflib import SequenceMatcher
from typing import Tuple

from constants import MINIMUM_PERCENTAGE


def calculate_similarity(stanza1: list, stanza2: list) -> float:
    """Calculate similarity percentage between two stanzas

    :return: similarity percentage
    """
    if not stanza1 or not stanza2:
        return 0.0

    # Convert stanzas to strings for comparison
    str1 = ' '.join(stanza1).lower()
    str2 = ' '.join(stanza2).lower()

    return SequenceMatcher(a=str1, b=str2).ratio() * 100


def analyze_stanzas_similarity(stanzas: list) -> Tuple[list, list]:
    """Analyze stanzas and find similar ones

    :param stanzas: list of stanzas
    :return: match in pairs | group of similarities
    """
    results = []
    similar_pairs = {}

    # Compare each pair of stanzas
    for i, stanza1 in enumerate(stanzas):
        if stanza1[0][0] in ("[", "("):
            continue
        for j, stanza2 in enumerate(stanzas[i + 1:], i + 1):
            if stanza2[0][0] in ("[", "("):
                continue
            similarity = calculate_similarity(stanza1, stanza2)

            if 100 > similarity > MINIMUM_PERCENTAGE:  # Threshold for considering as similar
                similar_pairs[(i, j)] = similarity
                results.append({
                    'stanza1_index': i,
                    'stanza2_index': j,
                    'similarity': round(similarity, 2),
                    'stanza1_preview': ' '.join(stanza1)[:40] + '...' if stanza1 else "Empty",
                    'stanza2_preview': ' '.join(stanza2)[:40] + '...' if stanza2 else "Empty"
                })

    similarity_groups = []
    processed = set()

    # Group similar stanzas
    for (id1, id2), similarity in similar_pairs.items():
        if id1 not in processed and id2 not in processed:
            group = {'indexes': [id1, id2], 'similarity': similarity}

            # Find other stanzas similar to this group
            for index in range(len(stanzas)):
                if index != id1 and index != id2 and index not in processed:
                    similar_to_id1 = calculate_similarity(stanzas[id1], stanzas[index])
                    similar_to_id2 = calculate_similarity(stanzas[id2], stanzas[index])
                    if 100 > similar_to_id1 > MINIMUM_PERCENTAGE or 100 > similar_to_id2 > MINIMUM_PERCENTAGE:
                        group['indexes'].append(index)
                        processed.add(index)

            similarity_groups.append(group)
            processed.update([id1, id2])

    return results, similarity_groups
