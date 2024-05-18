def read_custom_stop_words(files):
    custom_stop_words = set()
    for filename in files:
        with open(filename, 'r') as file:
            custom_stop_words.update(file.read().split())
    return custom_stop_words
