import argparse
from typing import List

import nltk
from nltk.corpus import wordnet


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="Input file, which contains words delimited by newlines",
    )

    return parser.parse_args()


def read_words(input_file: str) -> List['str']:
    words = []

    print(f"Reading file {input_file}...")
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                words.append(line)
    
    return words


def get_output_filename(input_file: str) -> str:
    if input_file.startswith("./") or input_file.startswith(".\\"):
        input_file = input_file[2:]
    
    if "." in input_file:
        return f"{input_file[:input_file.rfind('.')]}_wordnet_definitions.csv"
    else:
        return f"{input_file}_wordnet_definitions.csv"


def clean_definition(definition: str) -> str:
    definition = definition.replace(":", " -- ")
    definition = definition.replace("; ; ; ; - Karen Horney", "")
    definition = definition.replace('"', "'")
    definition = definition.replace("    ", " ")
    definition = definition.replace("   ", " ")
    definition = definition.replace("  ", " ")
    definition = definition.strip()

    return definition


def write_definitions_to_file(csv_file: str, words: List['str']):
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
                    line += f"{pos}: {definition}<br/>"

                line = line.rstrip("<br/>")
                line += '"\n'
                f.write(line)
            else:
                print(f"No definitions found for {word}. Creating stub instead.")
                f.write(f'"{word}":"TODO"\n')

    print(f"Definitions were written to file {csv_file}")


def main():
    args = parse_args()

    nltk.download("wordnet")
    nltk.download("omw-1.4")  # For accessing additional language mappings, if needed

    input_file: str = args.input.strip()

    words = read_words(input_file)
    if not words:
        print("No words were found in the file")
        return

    csv_file = get_output_filename(input_file)

    write_definitions_to_file(csv_file, words)


if __name__ == "__main__":
    main()
