import pandas as pd
import matplotlib.pyplot as plt
import re
import random
import string
from collections import OrderedDict
import numpy as np



## ------------------- STATICS ---------------------------------------------- ##
search = ["أ","إ","آ","ة","_","-","/",".","،"," و"," يا ",'"',"ـ","'","ى","\\",'\n', '\t','&quot;','?','؟','!',
"—", '‘']

replace = ["ا","ا","ا","ه"," "," ","","",""," و "," يا","","","","ي","",' ', ' ',' ',' ? ',' ؟ ',' ! ', '', '']



arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟‘.,'{}~¦+|!”…“–ـ٪'''

arabic_diacritics = re.compile("""
                         ّ    | # Tashdid
                         َ    | # Fatha
                         ً    | # Tanwin Fath
                         ُ    | # Damma
                         ٌ    | # Tanwin Damm
                         ِ    | # Kasra
                         ٍ    | # Tanwin Kasr
                         ْ    | # Sukun
                         ـ     # Tatwil/Kashida
                         ’
                     """, re.VERBOSE)
english_punctuations = string.punctuation
punctuations_list = arabic_punctuations + english_punctuations

# -------------------------------------------
arabic = ['ا','ب','ت', 'ث', 'ج','ح','خ', 'د', 'ذ','ر','ز','س','ش','ص','ض','ط','ظ','ع','غ','ف','ق','ك','ل','م','ن','ه','و','ي','ؤ','ئ','ء','ة','أ','إ','آ', ' ', 'ﻷ', 'ی','ﻻ', 'ئ']
arabic_replace = ['ۆ','ڪ','۶','ڤ','ک','چ','ژ','ڨ','ڭ','ﺎ','ﺭ', 'ﻕ','ء','ﺂ','ﻟ','ﺇ','ﻗ','','ٱ','پ', 'ﻣ', 'ﻬ','ﻢ','ﻥ', 'ﻤ', 'ﻭ', 'ﺖ', 'ﻫ', 'ﻂ','ﺿ', 'ﻚ', 'ﻉ']
special_chars =[' ','ی','﮼','ﻷ','ﺍ','ﻻ','ھ','ﺯ','ﺼ','ﺤ','ﺔ','ﺐ','ﻞ','ﺰ','ﺝ','ﺢ','ﻜ','ﻠ','ﻄ','ﻴ','ﺒ','ﺷ',
'ﻌ','ﻮ','ﺗ','ﺮ','ﺡ','ﻋ','ﺦ','ﺑ','ﻃ','ﻨ','ﺠ','ﺓ','ﺽ','ﺘ','ﺲ','ﺣ','ﻲ','ﻪ','ۈ','ﮧ','ﺩ','ﺜ','ﻛ','ﻘ','ﺪ','ﻡ',
 'ﺕ','ﺻ','ٺ','ں','ﻙ','ﺴ','ﻓ','ﻧ','ﻔ','ﻳ','ﻦ','ﻐ','ﻇ','ﻑ','ﻖ','ﺸ','ﺟ','ﻰ','ﺱ','ﻀ','ﺾ','ﺁ','ﻱ','ﺵ','ﺨ',
 'ﺳ','ﺬ','ﻊ','ﺀ','ﻝ','ﻩ','ﺧ','ﺙ','ﺋ','ﺺ','ﺛ','ﯾ']
# ---------------------------------------------
arabic_digits = ['٠','١','٢','٣','٤','٥','٦','٧','٨','٩']
arabic_chars = re.compile('[\u0627-\u064a]')

 ####---------------------------------------------------------------------------------------###


def normalize_arabic(text):
    text = re.sub("[ٲإٳأﺍﺁﭑﺈﺄﺃآا]", "ا", text)
    text = re.sub("_", " ", text)
    text = re.sub("[ٲإٳأﺍﺁﭑﺈﺄﺃآا]", "ا", text)
    text = re.sub("[ﻼﻷﻵﻹ]","لا", text)
    # text = re.sub("[ﻩﺓ]", "ه", text)

    # text = re.sub("ؤ", "ء", text)
    # text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    text = re.sub("ڳ","ك", text)
    text = re.sub("ﮔ","ك", text)
    text = re.sub("ٴ","ء", text)
    text = re.sub("ﻯ","ي", text)
    text = re.sub("ی", "ى", text)

    text = re.sub("ﺫ","ذ", text)
    text = re.sub("ﺏ","ب", text)
    text = re.sub("ﻹ","لا", text)
    text = re.sub("ﻵ","لا", text)
    text = re.sub("ﺶ","ش", text)
    text = re.sub("ﻏ","غ", text)
    text = re.sub("ݣ","ك", text)
    text = re.sub("چ", "ج", text)
    text = re.sub("ڤ", "ف", text)
    text = re.sub("ژ", "ز", text)
    text = re.sub("ۆ", "و", text)
    text = re.sub("پ", "ب", text)
    text = re.sub("ﻗ", "و", text)
    text = re.sub("ڨ", "ف", text)
    text = text.replace('ة', 'ه')
    return text


def remove_diacritics(text):
    text = re.sub(arabic_diacritics, '', text)
    return text


def remove_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)


def remove_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1', text)

    # step 1 remove punctuations
    # step 2 remove english chars
    # step 3 remove diacritics
    # step 4 normalize arabic
    # step 5 some of chars unicode still leaks into the text, filter the text char by char
    # step 6  removing words which contains single char 

def remove_single_char_word(text):
    filterd_text = ''
    for word in text.split():
        if len(word) > 1:
            filterd_text+=' '+word
    return filterd_text

def clean_arabic_tweet(tweet_text):

    p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    
    # step 1 remove punctuations
    tweet_text = tweet_text.replace('،', '')
    tweet_text = tweet_text.replace('"', '')
    tweet_text = tweet_text.replace('-', ' ')
    tweet_text = tweet_text.replace('—', ' ')
    tweet_text = tweet_text.replace('_', ' ')
    tweet_text = tweet_text.replace('+', ' ')
    tweet_text = tweet_text.replace('#', '')
    tweet_text = remove_punctuations(tweet_text)

    # step 2 remove english chars
    english_chars = re.compile("[a-zA-Z0-9?،؟><©®™;:,)({}[\]/\\\.\-_+=!@#$%\^&*|']")
    tweet_text = re.sub(english_chars,"", tweet_text)

    # step 3 remove     
    tweet_text = re.sub(p_tashkeel,"", tweet_text)
    tweet_text = remove_diacritics(tweet_text)
    
    # step 4 normalize arabic
    tweet_text = normalize_arabic(tweet_text)
    tweet_text = remove_repeating_char(tweet_text)
    
    # step 5 some of chars unicode still leaks into the text 
    # filter the text char by char

    tweet_text = re.sub(r'[^\u0600-\u06ff\u0750-\u077f\ufb50-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd50-\ufd8f\ufe70-\ufefc\uFDF0-\uFDFD]+', ' ', tweet_text)
    
    arabic_characters = arabic_chars.findall(tweet_text)#+arabic_replace+arabic_digits+arabic
    all_arabic = arabic_characters+arabic_replace+special_chars
    new_tweet_text = ''
    for char in tweet_text:
        if char in arabic_digits:
            pass
        elif char not in all_arabic:
            pass
        else:
            new_tweet_text+=char
            
    new_tweet_text.strip()

    # step 6  removing words which contains single char 
    final_tweet = remove_single_char_word(new_tweet_text)


    return final_tweet.strip()



def clean_arabic_tweetV0(tweet_text):
    tweet_text = tweet_text.replace('،', '')
    tweet_text = tweet_text.replace('"', '')
    tweet_text = tweet_text.replace('-', ' ')
    tweet_text = tweet_text.replace('—', ' ')
    tweet_text = tweet_text.replace('_', ' ')
    tweet_text = tweet_text.replace('+', ' ')
    tweet_text = tweet_text.replace('#', '')
    tweet_text = remove_punctuations(tweet_text)

    # step 2 remove english chars
    english_chars = re.compile("[a-zA-Z0-9?،؟><©®™;:,)({}[\]/\\\.\-_+=!@#$%\^&*|']")
    tweet_text = re.sub(english_chars,"", tweet_text)

    return tweet_text


#remove rare words.
#unique_count = 3
def remove_rare_words(df_column_name, unique_count):
    all_ = [x for y in df_column_name for x in y.split(' ') ]
    a,b = np.unique(all_, return_counts = True)
    to_remove = a[b<unique_count]
    print("words removed: ", len(to_remove))
    return [' '.join(np.array(y.split(' '))[~np.isin(y.split(' '), to_remove)]) for y in df_column_name]
    

#remove duplicate keywords from tweets.
def remove_duplicate_words(df_column_name):
    df_column_name = (df_column_name.str.split()
                              .apply(lambda x: OrderedDict.fromkeys(x).keys())
                              .str.join(' '))
    return df_column_name



#common_perecentage = 0.95
def remove_common_words(df_column_name, common_perecentage): 
    words_count = len([x for y in df_column_name for x in y.split(' ') ])
    print("words_count", words_count)
    minimum_words = words_count * common_perecentage
    print("minimum_words", minimum_words)
    df = pd.Series(df_column_name)
    return df.groupby((df.shift() != df).cumsum())\
                                 .filter(lambda x: len(x) < int(minimum_words))





# def clean_arabic_tweet(tweet_text):
#     global arabic_digits
#     global special_chars
#     global arabic_chars
#     global arabic_replace
#     global arabic
#     global punctuations_list
#     global arabic_diacritics
#     global search
#     global replace

#     unique_chars = []
#     p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    
#     tweet_text = tweet_text.replace('،', '')
#     tweet_text = tweet_text.replace('"', '')
#     tweet_text = tweet_text.replace('-', ' ')
#     tweet_text = tweet_text.replace('—', ' ')
#     tweet_text = tweet_text.replace('_', ' ')
#     tweet_text = tweet_text.replace('+', ' ')

#     english_chars = re.compile("[a-zA-Z0-9?،؟><©®™;:,)({}[\]/\\\.\-_+=!@#$%\^&*|']")
#     tweet_text = re.sub(english_chars,"", tweet_text)

#     tweet_text = re.sub(p_tashkeel,"", tweet_text)
#     tweet_text = remove_punctuations(tweet_text)
#     tweet_text = remove_diacritics(tweet_text)
#     tweet_text = normalize_arabic(tweet_text)
#     tweet_text = remove_repeating_char(tweet_text)
    
#     #remove longation
#     p_longation = re.compile(r'(.)\1+')
#     subst = r"\1\1"
#     tweet_text = re.sub(p_longation, subst, tweet_text)
    
#     tweet_text = tweet_text.replace('وو', 'و')
#     tweet_text = tweet_text.replace('يي', 'ي')
#     tweet_text = tweet_text.replace('اا', 'ا')
    
#     for i in range(0, len(search)):
#         tweet_text = tweet_text.replace(search[i], replace[i])
    
#     tweet_text = re.sub(r'[^\u0600-\u06ff\u0750-\u077f\ufb50-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd50-\ufd8f\ufe70-\ufefc\uFDF0-\uFDFD]+', ' ', tweet_text)
    
#     arabic_characters = arabic_chars.findall(tweet_text)#+arabic_replace+arabic_digits+arabic

#     all_arabic = arabic_characters+arabic_replace+special_chars
    
#     new_tweet_text = ''
#     for i, char in enumerate(tweet_text):
#         if char in arabic_digits:
#             pass
#         elif char not in all_arabic and char not in unique_chars:
#             unique_chars.append(char)
#             pass
#         else:
#             new_tweet_text+=char
            

#     new_tweet_text.strip()

#     return new_tweet_text



# def clean_arabic_tweet(tweet_text):
#   tweet_text = normalize_arabic(tweet_text)
#   p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
#   english_chars = re.compile("[a-zA-Z0-9?،؟><©®™;:,)({}[\]/\\\.\-_+=!@#$%\^&*|']")
#   tweet_text = re.sub(english_chars,"", tweet_text)
#   tweet_text = re.sub(p_tashkeel,"", tweet_text)
#   tweet_text = remove_punctuations(tweet_text)
#   tweet_text = remove_diacritics(tweet_text)
#   tweet_text = remove_repeating_char(tweet_text)

#   tweet_text = re.sub(r'[^\u0600-\u06ff\u0750-\u077f\ufb50-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd50-\ufd8f\ufe70-\ufefc\uFDF0-\uFDFD]+', ' ', tweet_text)

          
#   tweet_text.strip()

#   return tweet_text