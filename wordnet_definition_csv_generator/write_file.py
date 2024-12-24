from nltk.corpus import wordnet

from utils import clean_definition


def get_output_filename(input_file: str) -> str:
    if input_file.startswith("./") or input_file.startswith(".\\"):
        input_file = input_file[2:]

    if "." in input_file:
        return f"{input_file[:input_file.rfind('.')]}_wordnet_definitions.csv"
    else:
        return f"{input_file}_wordnet_definitions.csv"


def write_definitions_to_file(csv_file: str, words: list["str"]):
    # Define a mapping from POS codes to human-readable names
    pos_mapping = {
        "n": "noun",
        "v": "verb",
        "a": "adjective",
        "s": "adjective",  # satellite adjective
        "r": "adverb",
    }

    print(f"Writing to file {csv_file}...")
    with open(csv_file, "w") as f:
        for word in words:
            # Remove special characters needed for csv out of word itself
            word = word.replace(":", " -- ")
            word = word.replace('"', "'")
            word = word.strip()

            synsets = wordnet.synsets(word)

            if synsets:
                print(f"{word}:")
                line = f'"{word}":"'
                for synset in synsets:
                    # POS = part of speech
                    pos = pos_mapping[synset.pos()]
                    definition = clean_definition(synset.definition())

                    print(f"  {pos}: {definition}")
                    line += f"{pos}: {definition}<br/><br/>"

                line = line.rstrip("<br/><br/>")
                line += '"\n'
                f.write(line)
            else:
                print(f"No definitions found for {word}. Creating stub instead.")
                f.write(f'"{word}":"TODO"\n')

    print(f"Definitions were written to file {csv_file}")
