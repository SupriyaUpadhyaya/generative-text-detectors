import numpy as np
import re
import string
from statistics import stdev, mean
import pandas as pd
import json
import nltk
nltk.download('punkt')

def count_sentences(text):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    return len(sentences)

def count_sentences_per_paragraph(text):
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters
    sentences_per_paragraph = []
    total = 0

    # Iterate through each paragraph and count the sentences
    for paragraph in paragraphs:
        num_sentences = count_sentences(paragraph)
        sentences_per_paragraph.append(num_sentences)
        total += num_sentences

    return total

def count_words(text):
    # Tokenize the text into words
    words = text.split()
    return len(words)

def count_words_per_paragraph(text):
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters
    words_per_paragraph = []
    total = 0

    # Iterate through each paragraph and count the words
    for paragraph in paragraphs:
        num_words = count_words(paragraph)
        words_per_paragraph.append(num_words)
        total += num_words

    return total

def check_character_presence(text, character):
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters
    character_presence = 0

    # Iterate through each paragraph and check if the character is present
    for paragraph in paragraphs:
        if character in paragraph:
            character_presence = 1

    return character_presence

def paragraph_sentence_length_std_dev(text):
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters
    
    paragraph_std_devs = []
    total = 0
    
    for paragraph in paragraphs:
        # Tokenize the paragraph into sentences
        sentences = nltk.sent_tokenize(paragraph)

        # Calculate the length of each sentence
        sentence_lengths = [len(nltk.word_tokenize(sentence)) for sentence in sentences]

        if len(sentence_lengths) > 1:
            # Calculate the mean length of sentences
            mean_length = np.mean(sentence_lengths)

            # Calculate the squared differences between each sentence length and the mean
            squared_diffs = [(length - mean_length) ** 2 for length in sentence_lengths]

            # Calculate the variance
            variance = np.mean(squared_diffs)

            # Calculate the standard deviation
            std_dev = np.sqrt(variance)
        else:
            # If there's only one sentence in the paragraph, standard deviation is 0
            std_dev = 0
        
        paragraph_std_devs.append(std_dev)
        total += std_dev

    return total

def max_length_difference_paragraph(paragraph):
    # Tokenize the paragraph into sentences
    sentences = nltk.sent_tokenize(paragraph)
    
    max_diff = 0

    # Iterate over each pair of consecutive sentences
    for i in range(len(sentences) - 1):
        # Calculate the length difference between consecutive sentences
        diff = abs(len(nltk.word_tokenize(sentences[i])) - len(nltk.word_tokenize(sentences[i+1])))

        # Update max_diff if the current difference is greater
        if diff > max_diff:
            max_diff = diff

    return max_diff

def count_short_sentences_in_paragraphs(text):
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters
    
    short_sentence_counts = 0
    
    for paragraph in paragraphs:
        # Tokenize the paragraph into sentences
        sentences = nltk.sent_tokenize(paragraph)

        # Count the number of sentences with less than 11 words
        count = sum(1 for sentence in sentences if len(nltk.word_tokenize(sentence)) < 11)

        short_sentence_counts += count

    return short_sentence_counts

def count_long_sentences_in_paragraphs(text):
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters
    
    long_sentence_counts = 0
    
    for paragraph in paragraphs:
        # Tokenize the paragraph into sentences
        sentences = nltk.sent_tokenize(paragraph)

        # Count the number of sentences with less than 11 words
        count = sum(1 for sentence in sentences if len(nltk.word_tokenize(sentence)) > 34)

        long_sentence_counts += count

    return long_sentence_counts

def check_words_in_paragraphs(text, words_to_check):
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters

    presence = 0

    for paragraph in paragraphs:
        # Check if any of the words are present in the paragraph
        if any(word in paragraph for word in words_to_check):
            presence = 1

    return presence

def check_numbers_in_paragraphs(text):
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters
    
    presence_per_paragraph = []
    check = 0

    for paragraph in paragraphs:
        # Check if any numbers are present in the paragraph using regular expression
        if re.search(r'\d+', paragraph):
            presence_per_paragraph.append(1)
            check = 1
        else:
            presence_per_paragraph.append(0)

    return check

def check_capitals_to_periods_ratio(text):
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters
    
    presence_per_paragraph = []
    check = 0

    for paragraph in paragraphs:
        # Count the number of capital letters and periods in the paragraph
        capital_count = sum(1 for char in paragraph if char.isupper())
        period_count = paragraph.count('.')

        # Check if the paragraph contains twice as many capitals as periods
        if capital_count >= 2 * period_count:
            presence_per_paragraph.append(1)
            check = 1
        else:
            presence_per_paragraph.append(0)

    return check

def check_et_in_paragraphs(text):
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters
    
    presence_per_paragraph = []
    check = 0

    for paragraph in paragraphs:
        # Check if the paragraph contains the substring "et"
        if 'et' in paragraph:
            presence_per_paragraph.append(1)
            check = 1
        else:
            presence_per_paragraph.append(0)

    return check

def normalize_column(column):
    min_val = column.min()
    max_val = column.max()
    normalized_column = (column - min_val) / (max_val - min_val)
    return normalized_column

if __name__ == "__main__":
    header = True

    df = pd.read_json('./arxiv_bloomz.jsonl', lines=True)
    characters = [")", "-", ";", ":", "?", "'"]

    for df in df.itertuples():
        num_sentence_human = count_sentences_per_paragraph(df.abstract)
        num_sentence_machine = count_sentences_per_paragraph(df.machine_abstract)

        num_words_human = count_words_per_paragraph(df.abstract)
        num_words_machine = count_words_per_paragraph(df.machine_abstract)

        character0_human = check_character_presence(df.abstract, characters[0])
        character1_human = check_character_presence(df.abstract, characters[1])
        character2_human = check_character_presence(df.abstract, characters[2])
        character3_human = check_character_presence(df.abstract, characters[3])
        character4_human = check_character_presence(df.abstract, characters[4])
        character5_human = check_character_presence(df.abstract, characters[5])

        character2_3_human = 0

        if character2_human == 1 or character3_human == 1:
            character2_3_human = 1

        character0_machine = check_character_presence(df.machine_abstract, characters[0])
        character1_machine = check_character_presence(df.machine_abstract, characters[1])
        character2_machine = check_character_presence(df.machine_abstract, characters[2])
        character3_machine = check_character_presence(df.machine_abstract, characters[3])
        character4_machine = check_character_presence(df.machine_abstract, characters[4])
        character5_machine = check_character_presence(df.machine_abstract, characters[5])

        character2_3_machine = 0

        if character2_machine == 1 or character3_machine == 1:
            character2_3_machine = 1
        
        std_dev_human = paragraph_sentence_length_std_dev(df.abstract)
        std_dev_machine = paragraph_sentence_length_std_dev(df.machine_abstract)

        sent_len_diff_human = max_length_difference_paragraph(df.abstract)
        sent_len_diff_machine = max_length_difference_paragraph(df.machine_abstract)

        count_short_sentences_in_paragraphs_human = count_short_sentences_in_paragraphs(df.abstract)
        count_short_sentences_in_paragraphs_machine = count_short_sentences_in_paragraphs(df.machine_abstract)

        count_long_sentences_in_paragraphs_human = count_long_sentences_in_paragraphs(df.abstract)
        count_long_sentences_in_paragraphs_machine = count_long_sentences_in_paragraphs(df.machine_abstract)


        words = ["although", "However", "but", "because", "this", "others", "researchers"]

        check_word0_human = check_words_in_paragraphs(df.abstract, words[0])
        check_word0_machine = check_words_in_paragraphs(df.machine_abstract, words[0])

        check_word1_human = check_words_in_paragraphs(df.abstract, words[1])
        check_word1_machine = check_words_in_paragraphs(df.machine_abstract, words[1])

        check_word2_human = check_words_in_paragraphs(df.abstract, words[2])
        check_word2_machine = check_words_in_paragraphs(df.machine_abstract, words[2])

        check_word3_human = check_words_in_paragraphs(df.abstract, words[3])
        check_word3_machine = check_words_in_paragraphs(df.machine_abstract, words[3])

        check_word4_human = check_words_in_paragraphs(df.abstract, words[4])
        check_word4_machine = check_words_in_paragraphs(df.machine_abstract, words[4])

        check_word5_human = check_words_in_paragraphs(df.abstract, words[5])
        check_word5_machine = check_words_in_paragraphs(df.machine_abstract, words[5])

        check_word6_human = check_words_in_paragraphs(df.abstract, words[6])
        check_word6_machine = check_words_in_paragraphs(df.machine_abstract, words[6])

        check_word2_3_machine = 0

        if check_word2_machine == 1 or check_word3_machine == 1:
            check_word2_3_machine = 1

        check_word2_3_human = 0

        if check_word2_human == 1 or check_word3_human == 1:
            check_word2_3_human = 1

        check_num_human = check_numbers_in_paragraphs(df.abstract)
        check_num_machine = check_numbers_in_paragraphs(df.machine_abstract)

        check_capitals_human = check_capitals_to_periods_ratio(df.abstract)
        check_capitals_machine = check_capitals_to_periods_ratio(df.machine_abstract)

        check_et_human = check_et_in_paragraphs(df.abstract)
        check_et_machine = check_et_in_paragraphs(df.machine_abstract)
        #print("num_words_human ", num_words_human)
        # print("character0_human ", character0_human)
        # print("character1_human ", character1_human)
        # print("character2_3_human ", character2_3_human)
        # print("character4_human ", character4_human)
        # print("character5_human ", character5_human)

        # print("character0_machine ", character0_machine)
        # print("character1_machine ", character1_machine)
        # print("character2_3_machine ", character2_3_machine)
        # print("character4_machine ", character4_machine)
        # print("character5_machine ", character5_machine)
        #print("count_long_sentences_in_paragraphs_human ", count_long_sentences_in_paragraphs_human)
        #print("count_long_sentences_in_paragraphs_machine ", count_long_sentences_in_paragraphs_machine)

        data = {
        'source' : [df.source],
        'source_ID' : [df.source_id],
        'model': [df.model],
        'title': [df.title],
        'human_text': [df.abstract],
        'machine_text': [df.machine_abstract],
        'no_sentence_human': [num_sentence_human],
        'no_sentence_machine': [num_sentence_machine],
        'num_words_human': [num_words_human],
        'num_words_machine': [num_words_machine],
        'character0_human': [character0_human],
        'character1_human': [character1_human],
        'character2_3_human': [character2_3_human],
        'character4_human': [character4_human],
        'character5_human': [character5_human],
        'character0_machine': [character0_machine],
        'character1_machine': [character1_machine],
        'character2_3_machine': [character2_3_machine],
        'character4_machine': [character4_machine],
        'character5_machine': [character5_machine],
        'std_dev_human': [std_dev_human],
        'std_dev_machine': [std_dev_machine],
        'sent_len_diff_human': [sent_len_diff_human],
        'sent_len_diff_machine': [sent_len_diff_machine],
        'count_short_sentences_in_paragraphs_human': [count_short_sentences_in_paragraphs_human],
        'count_short_sentences_in_paragraphs_machine': [count_short_sentences_in_paragraphs_machine],
        'count_long_sentences_in_paragraphs_human': [count_long_sentences_in_paragraphs_human],
        'count_long_sentences_in_paragraphs_machine': [count_long_sentences_in_paragraphs_machine],
        'check_word0_human': [check_word0_human],
        'check_word1_human': [check_word1_human],
        'check_word2_3_human': [check_word2_3_human],
        'check_word3_human': [check_word3_human],
        'check_word4_human': [check_word4_human],
        'check_word5_human': [check_word5_human],
        'check_word0_machine': [check_word0_machine],
        'check_word1_machine': [check_word1_machine],
        'check_word2_3_machine': [check_word2_3_machine],
        'check_word3_machine': [check_word3_machine],
        'check_word4_machine': [check_word4_machine],
        'check_word5_machine': [check_word5_machine],
        'check_num_human': [check_num_human],
        'check_num_machine': [check_num_machine],
        'check_capitals_human': [check_capitals_human],
        'check_capitals_machine': [check_capitals_machine],
        'check_et_human': [check_et_human],
        'check_et_machine': [check_et_machine]
        }

        df1 = pd.DataFrame(data)
        df1.to_csv('./features_bloomz.csv', mode='a', index=False, header=header)
        header = False
    
    df = pd.read_csv('./features_bloomz.csv')
    df['no_sentence_human'] = normalize_column(df['no_sentence_human'])
    df['no_sentence_machine'] = normalize_column(df['no_sentence_machine'])
    df['num_words_human'] = normalize_column(df['num_words_human'])
    df['num_words_machine'] = normalize_column(df['num_words_machine'])
    df['std_dev_human'] = normalize_column(df['std_dev_human'])
    df['sent_len_diff_human'] = normalize_column(df['sent_len_diff_human'])
    df['std_dev_machine'] = normalize_column(df['std_dev_machine'])
    df['sent_len_diff_machine'] = normalize_column(df['sent_len_diff_machine'])
    df.to_csv('./features_bloomz_normalized.csv', index=False)

