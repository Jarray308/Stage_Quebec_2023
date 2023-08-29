from datetime import datetime, timedelta
import random
from django import template
from datetime import timedelta
from datetime import datetime, timedelta
import re
from django.shortcuts import render
register = template.Library()

def index(request):
   
    return render(request,'text_pages/index.html')


@register.filter
def generate_nearby_dates(date1_str):
    import locale
# Définir la locale en français
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    month_mapping = {
    'JANVIER': 1,
    'FÉVRIER': 2,
    'MARS': 3,
    'AVRIL': 4,
    'MAI': 5,
    'JUIN': 6,
    'JUILLET': 7,
    'AOÛT': 8,
    'SEPTEMBRE': 9,
    'OCTOBRE': 10,
    'NOVEMBRE': 11,
    'DÉCEMBRE': 12
     }
    day, month_str, year = date1_str.split()
    month = month_mapping[month_str.upper()]
    date1 = datetime(int(year), month, int(day))

# Générer trois dates à partir de la date initiale
    num_dates = 5
    dates_generated = [date1 + timedelta(days=random.randint(1, 365)) for _ in range(num_dates)]

    
# Formater et afficher les dates générées
    formatted_dates = []
    for date in dates_generated:
        formatted_date = date.strftime("%d %B %Y")
        formatted_dates.append(formatted_date)
    
    return formatted_dates

def extract_dates_and_sentences(text):
    date_pattern = r'\b(\d{1,2}\s(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s\d{4})\b'
    dates_found = re.findall(date_pattern, text, re.IGNORECASE)
    
    sentences = re.split(r'(?<=[.,])+', text)
    
    datesf = []  # Initialisez datesf en dehors de la boucle
    
    for sentence in sentences:
        for date in dates_found:
            if date in sentence:
                clean_text = re.sub(date_pattern, '', sentence, flags=re.IGNORECASE)
                sentence2 = clean_text.strip()
                dates =[]
                dates = generate_nearby_dates(date)
                dates.insert(0,date)
                datesf.append({"Question": sentence2, "Option_Correct": date, "Options": dates})
            
    return datesf










































from django.http import HttpResponse
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from django.shortcuts import render
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize


def show_result(text):
    

        stop_words = set(stopwords.words("french"))
        words = [word.lower() for word in word_tokenize(text) if word.isalpha() and word not in stop_words]

        word_freq = FreqDist(words)
        most_common_words = word_freq.most_common()

        # Filtrer les déterminants et sélectionner les 4 mots les plus fréquents
        filtered_words = [(word, freq) for word, freq in most_common_words if word not in stop_words][:4]

        return filtered_words

import spacy
from django.shortcuts import render
from nltk.corpus import stopwords
from collections import Counter

nlp = spacy.load("fr_core_news_sm")
stop_words = set(stopwords.words("french"))
def extract_important_words(text):
    doc = nlp(text)
    
    word_counter = Counter()
    
    for token in doc:
        if token.is_alpha and token.text.lower() not in stop_words:
            word_counter[token.text] += 1
    
    important_words = [word for word, _ in word_counter.most_common(3)]
    important_words.append("Tous faux")
    
    word_important = important_words[0]
    word_pas_important = important_words
    liste3 =word_pas_important
    #liste2.append(word_important)
 
    liste_word = []
    liste_word.append({
        "Question": "Le mot important dans le texte est ?",
        "Option_Correct": word_important,
        "Options":liste3
    })

    return liste_word











from django.shortcuts import render
import spacy
from geopy.geocoders import Nominatim

nlp = spacy.load("en_core_web_sm")
geolocator = Nominatim(user_agent="geo_app")

import spacy

nlp = spacy.load("fr_core_news_sm")

def detecter_les_locations(text):
    regions = ["nord-france", "sud-suisse", "est-america", "ouest-Asie", "est-belgique", "Nord-Espania", "Sud-africa", "Sud-Europe", "nord-america", "nord-australie", "ouest-Europe"]

    doc = nlp(text)
    lieux_detectes = []

    for entite in doc.ents:
        if entite.label_ == "LOC":
            lieux_detectes.append(entite.text)

    locf = []  # Définir locf en dehors de la boucle

    if lieux_detectes:
        autres_regions = random.sample(regions, min(3, len(regions)))
        autres_regions.insert(0, lieux_detectes[0])
        Qst = " Le site d'historique des textes est : "
        locf.append({"Question": Qst, "Option_Correct": lieux_detectes[0], "Options": autres_regions})

    return locf

    


      
           
    






import spacy

nlp = spacy.load("fr_core_news_sm")

def extract_verbs_in_future(text):
    doc = nlp(text)
    future_verbs = []

    for token in doc:
        if token.pos_ == "VERB" and "Fut" in token.morph.get("Tense", ""):
            future_verbs.append(token.text)

    fv = []  # Définissez fv en dehors de la boucle

    if future_verbs:
        f = []
        base = future_verbs[0][:-3]

        # Create the new forms by appending different suffixes
        f.append(future_verbs[0])
        f.append(base + "ez")
        f.append(base + "ons")
        f.append(base + "ont")

        fv.append({"Question": base + " " + "en Futur ?", "Option_Correct": future_verbs[0], "Options": f})

    return fv
 # Return the first verb
     


          
def generate_future_forms(future_verbs):
    future_forms = []

    # Remove the last three characters from the verb
    base_form = future_verbs[0][:-3]

    # Create the new forms by appending different suffixes
    future_forms.append(base_form + "ez")
    future_forms.append(base_form + "ons")
    future_forms.append(base_form + "ont")

    return future_forms



import spacy
from django.shortcuts import render
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def extract_summary(text):
    parser = PlaintextParser.from_string(text, Tokenizer("french"))
    
    if parser != "":
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, sentences_count=2)  # You can adjust the number of sentences in the summary
        
    
        return " ".join(str(sentence) for sentence in summary)
    else:
 
 
 
           return None
    
def generate_sum(extract_summary):
    sum = []

    if extract_summary != "":
        # Perform manipulations on extract_summary
        base_form = extract_summary.split(' ', 1)[1]  # Remove the first word
        base_form2 = ' '.join(extract_summary.split(' ', 4)[4:])  # Remove the first two words
        base_form3 = ' '.join(extract_summary.split(' ')[:-2])  # Remove the last two words
        sumof = extract_summary
        sum.append(sumof + "....")
        sum.append(base_form + "....")
        sum.append(base_form2 + "....")
        sum.append(base_form3 + "  " + base_form2 + "....")

        sumf = []
        sumf.append({
            "Question": "Quel est le résumé approprié du texte ?",
            "Option_Correct": sumof,
            "Options": sum
        })

        return sumf
    else:
        return None

import spacy
# extractions.py
import spacy

import spacy

import spacy

def person(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    person_info = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            ent_start = text.index(ent.text)
            ent_end = ent_start + len(ent.text)
            
            after_phrase_end = None
            for i in range(ent_end, len(text)):
                if text[i] in [',', '.', '!', '?']:
                    after_phrase_end = i
                    break
            
            if after_phrase_end is not None:
                after_phrase = text[ent_end:after_phrase_end].strip()
            else:
                after_phrase = text[ent_end:].strip()
            
            options = [
                after_phrase,
                ' '.join(after_phrase.split()[1:]),  # Remove the first word and join back into a string
                ' '.join(after_phrase.split()[:-2]),  # Remove the last word and join back into a string
                "aucune réponse"
            ]

            person_info.append({
                "Question": ent.text + " ...?",
                "Option_Correct": after_phrase.split(',')[0].split('.')[0],
                "Options": options
            })
            break

    return person_info


# Texte à traiter
#text = "Harry Potter and Hermione Granger were best friends at Hogwarts. Ron Weasley, on the other hand, had a pet rat."




def page1(request):
    if request.method == 'POST':
        text = request.POST.get('text')

        #appelle function extraire les dates de text

        liste_dates = extract_dates_and_sentences(text)
        #appelle function extraire les words important de text
      
        liste_words_imp = extract_important_words(text)
       
        #appelle function extraire les verb futur de text
        liste_verb_future =extract_verbs_in_future(text)

        #appelle function extraire les locations  dans le  text
        liste_locations =  detecter_les_locations(text)

        #appelle function extraire les summary de text
        summary = extract_summary(text)
        liste_sum_genrer = generate_sum(summary)

        #appelle function extraire les personnage de text
        liste_personnes =person(text)

        #all_data = liste_words_imp + liste_dates + liste_verb_future + liste_locations + liste_sum_genrer + liste_personnes  # Vos listes de dictionnaires
         
        all_data = liste_words_imp + liste_dates + liste_verb_future + liste_locations + liste_sum_genrer + liste_personnes  # Vos listes de dictionnaires

        random.shuffle(all_data)
        
       
            
        


           
        return render(request, 'text_pages/quiz.html',  {'quiz_data': all_data})
               
        '''return render(request, 'text_pages/jareb.html', { 'liste_dates' : liste_dates, 
                                                         'impcle' : liste_words_imp ,
                                                          'vf' : liste_verb_future ,
                                                          'loc' : liste_locations ,
                                                          'sum' : summary ,
                                                          'gen' : liste_sum_genrer ,
                                                          'per' : liste_personnes 
                                                          })'''
           
    return render(request, 'text_pages/page1.html' , {})




def page2(request):
    return render(request, 'temp/aff.html')