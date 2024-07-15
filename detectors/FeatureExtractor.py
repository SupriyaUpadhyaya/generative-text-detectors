import os
import numpy as np
import re
import string
from statistics import stdev, mean
import pandas as pd
import json
import nltk

class FeatureExtractor():
    def __init__(self):
        self.characters = [")", "-", ";", ":", "?", "'"]

    def count_sentences(self, text):
        # Tokenize the text into sentences
        sentences = nltk.sent_tokenize(text)
        return len(sentences)

    def count_sentences_per_paragraph(self, text):
        # Split the text into paragraphs
        paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters
        sentences_per_paragraph = []
        total = 0

        # Iterate through each paragraph and count the sentences
        for paragraph in paragraphs:
            num_sentences = self.count_sentences(paragraph)
            sentences_per_paragraph.append(num_sentences)
            total += num_sentences

        return total/len(paragraphs)

    def count_words(self, text):
        # Tokenize the text into words
        words = text.split()
        return len(words)

    def count_words_per_paragraph(self, text):
        # Split the text into paragraphs
        paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters
        words_per_paragraph = []
        total = 0

        # Iterate through each paragraph and count the words
        for paragraph in paragraphs:
            num_words = self.count_words(paragraph)
            words_per_paragraph.append(num_words)
            total += num_words

        return total/len(paragraphs)

    def check_character_presence(self, text, character):
        # Split the text into paragraphs
        paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters
        character_presence = 0
        count = 0

        # Iterate through each paragraph and check if the character is present
        for paragraph in paragraphs:
            if character in paragraph:
                character_presence = 1
                count += 1

        return count

    def paragraph_sentence_length_std_dev(self, text):
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

        return total/len(paragraphs)

    def max_length_difference_paragraph(self, paragraph):
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

    def count_short_sentences_in_paragraphs(self, text):
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

    def count_long_sentences_in_paragraphs(self, text):
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
        count = 0

        for paragraph in paragraphs:
            # Check if any of the words are present in the paragraph
            if any(word in paragraph for word in words_to_check):
                presence = 1
                count += 1

        return presence

    def check_numbers_in_paragraphs(self, text):
        # Split the text into paragraphs
        paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters
        
        presence_per_paragraph = []
        count = 0
        check = 0

        for paragraph in paragraphs:
            # Check if any numbers are present in the paragraph using regular expression
            if re.search(r'\d+', paragraph):
                presence_per_paragraph.append(1)
                check = 1
                count += 1
            else:
                presence_per_paragraph.append(0)

        return count

    def check_capitals_to_periods_ratio(self, text):
        # Split the text into paragraphs
        paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters
        
        presence_per_paragraph = []
        check = 0
        count = 0

        for paragraph in paragraphs:
            # Count the number of capital letters and periods in the paragraph
            capital_count = sum(1 for char in paragraph if char.isupper())
            period_count = paragraph.count('.')

            # Check if the paragraph contains twice as many capitals as periods
            if capital_count >= 2 * period_count:
                presence_per_paragraph.append(1)
                check = 1
                count += 1
            else:
                presence_per_paragraph.append(0)

        return count

    def check_et_in_paragraphs(self, text):
        # Split the text into paragraphs
        paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by double newline characters
        
        presence_per_paragraph = []
        check = 0
        count = 0

        for paragraph in paragraphs:
            # Check if the paragraph contains the substring "et"
            if 'et' in paragraph:
                presence_per_paragraph.append(1)
                check = 1
                count += 1
            else:
                presence_per_paragraph.append(0)

        return check

    def normalize_column(self, column):
        min_val = column.min()
        max_val = column.max()
        normalized_column = (column - min_val) / (max_val - min_val)
        return normalized_column

    def delete_csv_if_exists(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"File does not exist: {file_path}")

    def contains_word(self, string, word):
        return word in string
    
    def getFeatures(self, text):
        machine_abstract = df.machine_text

        #num_sentence_human = self.count_sentences_per_paragraph(abstract)
        num_sentence_machine = self.count_sentences_per_paragraph(machine_abstract)

        #num_words_human = self.count_words_per_paragraph(abstract)
        num_words_machine = self.count_words_per_paragraph(machine_abstract)

        # character0_human = self.check_character_presence(abstract, self.characters[0])
        # character1_human = self.check_character_presence(abstract, self.characters[1])
        # character2_human = self.check_character_presence(abstract, self.characters[2])
        # character3_human = self.check_character_presence(abstract, self.characters[3])
        # character4_human = self.check_character_presence(abstract, self.characters[4])
        # character5_human = self.check_character_presence(abstract, self.characters[5])

        # character2_3_human = 0

        # if character2_human == 1 or character3_human == 1:
        #     character2_3_human = 1

        character0_machine = self.check_character_presence(machine_abstract, self.characters[0])
        character1_machine = self.check_character_presence(machine_abstract, self.characters[1])
        character2_machine = self.check_character_presence(machine_abstract, self.characters[2])
        character3_machine = self.check_character_presence(machine_abstract, self.characters[3])
        character4_machine = self.check_character_presence(machine_abstract, self.characters[4])
        character5_machine = self.check_character_presence(machine_abstract, self.characters[5])

        character2_3_machine = 0

        if character2_machine == 1 or character3_machine == 1:
            character2_3_machine = 1
        
        #std_dev_human = self.paragraph_sentence_length_std_dev(abstract)
        std_dev_machine = self.paragraph_sentence_length_std_dev(machine_abstract)

        #sent_len_diff_human = self.max_length_difference_paragraph(abstract)
        sent_len_diff_machine = self.max_length_difference_paragraph(machine_abstract)

        #count_short_sentences_in_paragraphs_human = self.count_short_sentences_in_paragraphs(abstract)
        count_short_sentences_in_paragraphs_machine = self.count_short_sentences_in_paragraphs(machine_abstract)

        #count_long_sentences_in_paragraphs_human = self.count_long_sentences_in_paragraphs(abstract)
        count_long_sentences_in_paragraphs_machine = self.count_long_sentences_in_paragraphs(machine_abstract)


        words = ["although", "However", "but", "because", "this", "others", "researchers"]

        #check_word0_human = self.check_words_in_paragraphs(abstract, words[0])
        check_word0_machine = self.check_words_in_paragraphs(machine_abstract, words[0])

        #check_word1_human = self.check_words_in_paragraphs(abstract, words[1])
        check_word1_machine = self.check_words_in_paragraphs(machine_abstract, words[1])

        #check_word2_human = self.check_words_in_paragraphs(abstract, words[2])
        check_word2_machine = self.check_words_in_paragraphs(machine_abstract, words[2])

        #check_word3_human = self.check_words_in_paragraphs(abstract, words[3])
        check_word3_machine = self.check_words_in_paragraphs(machine_abstract, words[3])

        #check_word4_human = self.check_words_in_paragraphs(abstract, words[4])
        check_word4_machine = self.check_words_in_paragraphs(machine_abstract, words[4])

        #check_word5_human = self.check_words_in_paragraphs(abstract, words[5])
        check_word5_machine = self.check_words_in_paragraphs(machine_abstract, words[5])

        #check_word6_human = self.check_words_in_paragraphs(abstract, words[6])
        check_word6_machine = self.check_words_in_paragraphs(machine_abstract, words[6])

        check_word2_3_machine = 0

        if check_word2_machine == 1 or check_word3_machine == 1:
            check_word2_3_machine = 1

        # check_word2_3_human = 0

        # if check_word2_human == 1 or check_word3_human == 1:
        #     check_word2_3_human = 1

        #check_num_human = self.check_numbers_in_paragraphs(abstract)
        check_num_machine = self.check_numbers_in_paragraphs(machine_abstract)

        #check_capitals_human = self.check_capitals_to_periods_ratio(abstract)
        check_capitals_machine = self.check_capitals_to_periods_ratio(machine_abstract)

        #check_et_human = self.check_et_in_paragraphs(abstract)
        check_et_machine = self.check_et_in_paragraphs(machine_abstract)

        data = {}

        # for param in params:
        #     data[param] = dfs.loc[count, param]

        #data['no_sentence_human'] = [num_sentence_human]
        data['no_sentence_machine'] = [num_sentence_machine]
        #data['num_words_human'] = [num_words_human]
        data['num_words_machine'] = [num_words_machine]
        #data['character0_human'] = [character0_human]
        #data['character1_human'] = [character1_human]
        #data['character2_3_human'] = [character2_3_human]
        #data['character4_human'] = [character4_human]
        #data['character5_human'] = [character5_human]
        data['character0_machine'] = [character0_machine]
        data['character1_machine'] = [character1_machine]
        data['character2_3_machine'] = [character2_3_machine]
        data['character4_machine'] = [character4_machine]
        data['character5_machine'] = [character5_machine]
        #data['std_dev_human'] = [std_dev_human]
        data['std_dev_machine'] = [std_dev_machine]
        #data['sent_len_diff_human'] = [sent_len_diff_human]
        data['sent_len_diff_machine'] = [sent_len_diff_machine]
        #data['count_short_sentences_in_paragraphs_human'] = [count_short_sentences_in_paragraphs_human]
        data['count_short_sentences_in_paragraphs_machine'] = [count_short_sentences_in_paragraphs_machine]
        #data['count_long_sentences_in_paragraphs_human'] = [count_long_sentences_in_paragraphs_human]
        data['count_long_sentences_in_paragraphs_machine'] = [count_long_sentences_in_paragraphs_machine]
        #data['check_word0_human'] = [check_word0_human]
        #data['check_word1_human'] = [check_word1_human]
        #data['check_word2_3_human'] = [check_word2_3_human]
        #data['check_word3_human'] = [check_word3_human]
        #data['check_word4_human'] = [check_word4_human]
        #data['check_word5_human'] = [check_word5_human]
        data['check_word0_machine'] = [check_word0_machine]
        data['check_word1_machine'] = [check_word1_machine]
        data['check_word2_3_machine'] = [check_word2_3_machine]
        data['check_word3_machine'] = [check_word3_machine]
        data['check_word4_machine'] = [check_word4_machine]
        data['check_word5_machine'] = [check_word5_machine]
        #data['check_num_human'] = [check_num_human]
        data['check_num_machine'] = [check_num_machine]
        #data['check_capitals_human'] = [check_capitals_human]
        data['check_capitals_machine'] = [check_capitals_machine]
        #data['check_et_human'] = [check_et_human]
        data['check_et_machine'] = [check_et_machine]

        #count += 1
        df = pd.DataFrame(data)
        #df1.to_csv(outputfilename, mode='a', index=False, header=header)
        header = False
        
        #df = pd.read_csv(outputfilename)
        df['no_sentence_human'] = self.normalize_column(df['no_sentence_human'])
        df['no_sentence_machine'] = self.normalize_column(df['no_sentence_machine'])
        df['num_words_human'] = self.normalize_column(df['num_words_human'])
        df['num_words_machine'] = self.normalize_column(df['num_words_machine'])
        df['std_dev_human'] = self.normalize_column(df['std_dev_human'])
        df['sent_len_diff_human'] = self.normalize_column(df['sent_len_diff_human'])
        df['std_dev_machine'] = self.normalize_column(df['std_dev_machine'])
        df['sent_len_diff_machine'] = self.normalize_column(df['sent_len_diff_machine'])
        
        return df.values.tolist()