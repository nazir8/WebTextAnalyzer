import pandas as pd
from read_custom_files import read_custom_stop_words
from data_extraction import extract_article_text
from data_preprocessing import preprocess_text
from sentiment_analysis import count_sentiment_words 
from text_metrics import measure, cleaned_words, count_personal_pronouns
from nltk.tokenize import word_tokenize


# Read input data
input_df = pd.read_excel("Input.xlsx")

# Read custom stop words
custom_stop_words = read_custom_stop_words([
    "StopWords_Names.txt",
    "StopWords_Geographic.txt",
    "StopWords_Currencies.txt",
    "StopWords_Auditor.txt",
    "StopWords_DatesandNumbers.txt",
    "StopWords_Generic.txt",
    "StopWords_Genericlong.txt"
])

# Extract article text from URLs
output_data = []
for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    print(f"Processing URL {url_id}: {url}")
    article_title, article_text = extract_article_text(url)
    if article_text:
        output_data.append({'URL-ID': url_id, 'Article Title': article_title, 'Article Text': article_text})

# Preprocess text
df = pd.DataFrame(output_data)
df['processed_text'] = df['Article Text'].apply(lambda x: preprocess_text(x, custom_stop_words))

# Sentiment analysis
positive_words = set()
negative_words = set()

with open('positive-words.txt', 'r') as file:
    for line in file:
        positive_words.add(line.strip())

with open('negative-words.txt', 'r') as file:
    for line in file:
        negative_words.add(line.strip())

positive_words_list = []
negative_words_list = []
positive_score = []
negative_score = []
polarity_score = []
subjectivity_score = []

for index, row in df.iterrows():
    text = row['processed_text']
    positive_words_doc = [word for word in word_tokenize(text) if word.lower() in positive_words]
    negative_words_doc = [word for word in word_tokenize(text) if word.lower() in negative_words]
    positive_words_list.append(positive_words_doc)
    negative_words_list.append(negative_words_doc)
    positive_score.append(len(positive_words_doc))
    negative_score.append(len(negative_words_doc))
    polarity_score.append((positive_score[-1] - negative_score[-1]) / ((positive_score[-1] + negative_score[-1]) + 0.000001))
    subjectivity_score.append((positive_score[-1] + negative_score[-1]) / ((len(word_tokenize(text))) + 0.000001))

df['Positive Words'] = positive_words_list
df['Negative Words'] = negative_words_list
df['Positive Score'] = positive_score
df['Negative Score'] = negative_score
df['Polarity Score'] = polarity_score
df['Subjectivity Score'] = subjectivity_score

# Text metrics calculation
avg_sentence_length = []
Percentage_of_Complex_words = []
Fog_Index = []
complex_word_count = []
avg_syllable_word_count = []

for index, row in df.iterrows():
    avg_sentence_len, Percent_Complex_words, fog_index, num_complex_words, avg_syllables = measure(row['processed_text'])
    avg_sentence_length.append(avg_sentence_len)
    Percentage_of_Complex_words.append(Percent_Complex_words)
    Fog_Index.append(fog_index)
    complex_word_count.append(num_complex_words)
    avg_syllable_word_count.append(avg_syllables)

df['Average Sentence Length'] = avg_sentence_length
df['Percentage of Complex Words'] = Percentage_of_Complex_words
df['Fog Index'] = Fog_Index
df['Complex Word Count'] = complex_word_count
df['Average Syllable per Word Count'] = avg_syllable_word_count



# Apply the functions to each row in 'article text' column of df
word_count = []
average_word_length = []
personal_pronoun_count = []

for index, row in df.iterrows():
    text = row['Article Text']
    wc, awl = cleaned_words(text)
    word_count.append(wc)
    average_word_length.append(awl)
    personal_pronoun_count.append(count_personal_pronouns(text))

# Add the calculated metrics to the DataFrame
df['Word Count'] = word_count
df['Average Word Length'] = average_word_length
df['Personal Pronoun Count'] = personal_pronoun_count



# Save output data
output_df = pd.read_excel('Output Data Structure.xlsx')

variables = [positive_score,
            negative_score,
            polarity_score,
            subjectivity_score,
            avg_sentence_length,
            Percentage_of_Complex_words,
            Fog_Index,
            avg_sentence_length,
            complex_word_count,
            word_count,
            avg_syllable_word_count,
            personal_pronoun_count,
            average_word_length]

# write the values to the dataframe
for i, var in enumerate(variables):
    output_df.iloc[:,i+2] = var

#now save the dataframe to the disk
output_df.to_csv('Output_Data.csv')
