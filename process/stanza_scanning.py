from logger import logger


def analyze_repetition(lyrics: list[list[str]]) -> list:
    """Analyzes if there is a repetition that can be filtered

    :param lyrics: song lyrics
    :return: filtered lyrics
    """
    new_lyrics = []

    for stanza in lyrics:
        if stanza[0][0] == "(":
            new_lyrics.append(stanza)
            continue

        new_stanzas = identify_repetition_inside_stanza(stanza)
        if isinstance(new_stanzas, tuple):
            new_lyrics.extend(new_stanzas)
            continue

        new_lyrics.append(new_stanzas)

    return new_lyrics


def identify_repetition_inside_stanza(stanza: list[str]) -> list | tuple:
    """Identifies a repetition by analyzing blocks of lines

    :param stanza: lines of a stanza
    :return: filtered stanza
    """
    result = stanza.copy()
    lenght_stanza = len(result)
    count = 1

    while count < lenght_stanza:

        if result[0].strip() == result[count].strip():
            pattern_length = count

            is_valid_pattern = True
            for index in range(pattern_length):
                if count + index >= lenght_stanza or result[index].strip() != result[count + index].strip():
                    is_valid_pattern = False
                    break

            if is_valid_pattern:

                # Check if the pattern repeats completely to the end
                remaining_length = lenght_stanza - pattern_length
                if remaining_length % pattern_length == 0:
                    num_repetitions = lenght_stanza // pattern_length
                    separated_stanzas = [result[qty_repetition * pattern_length:(qty_repetition + 1) * pattern_length]
                                         for qty_repetition in range(num_repetitions)]

                    return tuple(separated_stanzas)

        count += 1

    return result


def break_stanzas(formatted_lyrics: list) -> None:
    """Breaks stanzas in a specific line

    :param formatted_lyrics:
    """
    logger.info(f"Existem {len(formatted_lyrics)} estrofes")
    print("Aqui estao o começo delas:")
    for index, stanza in enumerate(formatted_lyrics):
        length = 4
        len_stanza = len(stanza)

        if len_stanza < length:
            length = len(stanza)

        print(f"Estrofe {index} - {stanza[:length]}")

    print("===================")
    stanza_index = int(input("Qual estrofe deseja alterar?: "))
    for index, line in enumerate(formatted_lyrics[stanza_index]):
        print(f"Linha {index}: {line}")

    line_index = int(input("Em qual linha deseja começar uma nova estrofe?: "))

    second_stanza = formatted_lyrics[stanza_index][line_index:]

    formatted_lyrics[stanza_index] = formatted_lyrics[stanza_index][:line_index]
    formatted_lyrics.insert(stanza_index + 1, second_stanza)
    return
