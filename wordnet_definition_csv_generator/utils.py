def clean_definition(definition: str) -> str:
    # remove WordNet comments
    comment_index = definition.find("; ;")
    if comment_index >= 0:
        definition = definition[:comment_index]

    comment_index = definition.find("; -")
    if comment_index >= 0:
        definition = definition[:comment_index]

    while definition.endswith(";") or definition.endswith(" "):
        definition = definition.rstrip(";")
        definition = definition.rstrip(" ")

    definition = definition.replace(":", " -- ")
    definition = definition.replace('"', "'")
    definition = definition.replace("    ", " ")
    definition = definition.replace("   ", " ")
    definition = definition.replace("  ", " ")
    definition = definition.strip()

    return definition
