import nltk

from args import parse_args
from read_file import read_words
from write_file import get_output_filename, write_definitions_to_file


def read_and_write_file(input_file: str):
    words = read_words(input_file)
    if not words:
        raise Exception(f"No words were found in the file: {input_file}")

    csv_file = get_output_filename(input_file)
    write_definitions_to_file(csv_file, words)


def main():
    args = parse_args()

    nltk.download("wordnet")
    nltk.download("omw-1.4")  # For accessing additional language mappings, if needed

    read_and_write_file(args.input.strip())


if __name__ == "__main__":
    main()
