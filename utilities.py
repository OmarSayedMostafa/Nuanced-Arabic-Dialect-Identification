import pandas as pd
import matplotlib.pyplot as plt
import re
import random
import string



## ------------------- STATICS ---------------------------------------------- ##
search = ["أ","إ","آ","ة","_","-","/",".","،"," و "," يا ",'"',"ـ","'","ى","\\",'\n', '\t','&quot;','?','؟','!',"—", '‘']
replace = ["ا","ا","ا","ه"," "," ","","",""," و"," يا","","","","ي","",' ', ' ',' ',' ? ',' ؟ ',' ! ', '', '']
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
arabic = ['ا','ب','ت', 'ث', 'ج','ح','خ', 'د', 'ذ','ر','ز','س','ش','ص','ض','ط','ظ','ع','غ','ف','ق','ك','ل','م','ن','ه','و','ي','ؤ','ئ','ء','ة','أ','إ','آ', ' ', 'ﻷ', 'ی','ﻻ']
arabic_replace = ['ۆ','ڪ','۶','ڤ','ک','چ','ژ','ڨ','ڭ','ﺎ','ﺭ', 'ﻕ','ء','ﺂ','ﻟ','ﺇ','ﻗ','','ٱ','پ', 'ﻣ', 'ﻬ','ﻢ','ﻥ', 'ﻤ', 'ﻭ', 'ﺖ', 'ﻫ', 'ﻂ','ﺿ', 'ﻚ', 'ﻉ']
arabic_digits = ['٠','١','٢','٣','٤','٥','٦','٧','٨','٩']
arabic_chars = re.compile('[\u0627-\u064a]')


special_chars =[' ','ی','﮼','ﻷ','ﺍ','ﻻ','ھ','ﺯ','ﺼ','ﺤ','ﺔ','ﺐ','ﻞ','ﺰ','ﺝ','ﺢ','ﻜ','ﻠ','ﻄ','ﻴ','ﺒ','ﺷ',
'ﻌ','ﻮ','ﺗ','ﺮ','ﺡ','ﻋ','ﺦ','ﺑ','ﻃ','ﻨ','ﺠ','ﺓ','ﺽ','ﺘ','ﺲ','ﺣ','ﻲ','ﻪ','ۈ','ﮧ','ﺩ','ﺜ','ﻛ','ﻘ','ﺪ','ﻡ',
 'ﺕ','ﺻ','ٺ','ں','ﻙ','ﺴ','ﻓ','ﻧ','ﻔ','ﻳ','ﻦ','ﻐ','ﻇ','ﻑ','ﻖ','ﺸ','ﺟ','ﻰ','ﺱ','ﻀ','ﺾ','ﺁ','ﻱ','ﺵ','ﺨ',
 'ﺳ','ﺬ','ﻊ','ﺀ','ﻝ','ﻩ','ﺧ','ﺙ','ﺋ','ﺺ','ﺛ','ﯾ']

 ####---------------------------------------------------------------------------------------###

def normalize_arabic(text):
    text = re.sub("[ٲإٳأﺍﺁﭑﺈﺄﺃآا]", "ا", text)
    text = re.sub("[ﻼﻷﻵﻹ]","لا", text)
    text = re.sub("[ﻩﺓ]", "ه", text)

    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    # text = re.sub("ة", "ه", text)
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


    return text


def remove_diacritics(text):
    text = re.sub(arabic_diacritics, '', text)
    return text


def remove_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)


def remove_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1', text)


def clean_arabic_tweet(tweet_text):
    global arabic_digits
    global special_chars
    global arabic_chars
    global arabic_replace
    global arabic
    global punctuations_list
    global arabic_diacritics
    global search
    global replace

    unique_chars = []
    p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    
    english_chars = re.compile("[a-zA-Z0-9?،؟><©®™;:,)({}[\]/\\\.\-_+=!@#$%\^&*|']")
    tweet_text = re.sub(english_chars,"", tweet_text)

    tweet_text = tweet_text.replace('،', '')
    tweet_text = tweet_text.replace('"', '')
    tweet_text = tweet_text.replace('-', ' ')
    tweet_text = tweet_text.replace('—', ' ')

    tweet_text = re.sub(p_tashkeel,"", tweet_text)
    tweet_text = remove_punctuations(tweet_text)
    tweet_text = remove_diacritics(tweet_text)
    tweet_text = normalize_arabic(tweet_text)
    tweet_text = remove_repeating_char(tweet_text)
    
    #remove longation
    p_longation = re.compile(r'(.)\1+')
    subst = r"\1\1"
    tweet_text = re.sub(p_longation, subst, tweet_text)
    
    tweet_text = tweet_text.replace('وو', 'و')
    tweet_text = tweet_text.replace('يي', 'ي')
    tweet_text = tweet_text.replace('اا', 'ا')
    
    for i in range(0, len(search)):
        tweet_text = tweet_text.replace(search[i], replace[i])
    
    tweet_text = re.sub(r'[^\u0600-\u06ff\u0750-\u077f\ufb50-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd50-\ufd8f\ufe70-\ufefc\uFDF0-\uFDFD]+', ' ', tweet_text)
    
    arabic_characters = arabic_chars.findall(tweet_text)#+arabic_replace+arabic_digits+arabic

    all_arabic = arabic_characters+arabic_replace+special_chars
    
    new_tweet_text = ''
    for i, char in enumerate(tweet_text):
        if char in arabic_digits:
            pass
        elif char not in all_arabic and char not in unique_chars:
            unique_chars.append(char)
            pass
        else:
            new_tweet_text+=char
            

    new_tweet_text.strip()

    return new_tweet_text