from extraction.website import get_song_html
from logger import logger
from process.lyrics import organize_song_lyrics, parse_chords_and_lyrics, analyze_stanzas, set_stanza_default
from process.make_file import make_pdf
from process.similarity import analyze_stanzas_similarity
from process.stanza_scanning import analyze_repetition, change_stanzas

url = input("URL: ")
changes_check = input("Deseja fazer alterações de quebrar/juntar estrofes?(vazio=NAO): ")
song_name = f"{url.split('/')[-2]}"

if __name__ == "__main__":
    logger.info(f"Começando processo na URL: {url}")
    song_html = get_song_html(url)

    logger.info(f"Fazendo separação de linhas")
    song_lines = parse_chords_and_lyrics(song_html)

    logger.info(f"Organizando cifra em estrofes")
    formatted_lyrics = organize_song_lyrics(song_lines)

    if changes_check:
        print("===================")
        break_check = input("Esse passo por ser útil depois da visualização do pdf...\n"
                            "Deseja quebrar alguma estrofe em partes?(vazio=NAO): ")
        while break_check:
            change_stanzas(formatted_lyrics, action='break')
            break_check = input("Continuar quebrando estrofes?(vazio=NAO): ")

    logger.info(f"Encontrando repetições")
    filtered_formatted_lyrics = analyze_repetition(formatted_lyrics)

    logger.info(f"Analisando similaridade entre estrofes")
    individual_results, groups = analyze_stanzas_similarity(filtered_formatted_lyrics)
    if individual_results and groups:
        set_stanza_default(groups, filtered_formatted_lyrics)

    if changes_check:
        print("===================")
        join_check = input("Deseja juntar estrofes?(vazio=NAO): ")
        while join_check:
            change_stanzas(formatted_lyrics, action='join')
            join_check = input("Continuar juntando estrofes?(vazio=NAO): ")

    logger.info("Analisando estrofes para gerar sequência e PDF")
    sequence, id_map = analyze_stanzas(filtered_formatted_lyrics)
    print(f"Ordem: {sequence}")

    logger.info("Gerando PDF")
    make_pdf(song_name, sequence, id_map)
    # raw_pdf(song_lines, f"{song_name}.pdf")
    logger.info("Processo concluído")
