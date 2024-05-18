def count_sentiment_words(text, positive_words, negative_words):
    words = text.split()
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
    return positive_count, negative_count
