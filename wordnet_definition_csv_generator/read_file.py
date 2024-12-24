def read_words(input_file: str) -> list["str"]:
    words = []

    print(f"Reading file {input_file}...")
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                words.append(line)

    return words
