from django.shortcuts import render
import re

def index(request):
    context = {
        'message': "Hello, this is a Django HTML page!",
    }
    return render(request,'text_pages/index.html', context)

import spacy
from django.shortcuts import render
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def extract_summary(text):
    parser = PlaintextParser.from_string(text, Tokenizer("french"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences_count=2)  # You can adjust the number of sentences in the summary
    return " ".join(str(sentence) for sentence in summary)


 
nlp = spacy.load("fr_core_news_sm")

def extract_verbs_in_future(text):
    doc = nlp(text)
    future_verbs = []

    for token in doc:
        if token.pos_ == "VERB" and "Fut" in token.morph.get("Tense", ""):
            future_verbs.append(token.text)

    return future_verbs


def extract_dates_and_sentences(text):
    date_pattern = r'\b(\d{1,2}\s(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s\d{4})\b'
    dates_found = re.findall(date_pattern, text, re.IGNORECASE)

    sentences = re.split(r'(?<=[.,]) +', text)
    sentences_with_dates = []

    for sentence in sentences:
        for date in dates_found:
            if date in sentence:
                sentences_with_dates.append((sentence, date))
                break

    return sentences_with_dates
def extraire_locations(text):
    # Utiliser spaCy pour analyser le texte
    doc = nlp(text)
    
    # Liste pour stocker les emplacements extraits
    locations = []
    
    # Parcourir les entités nommées extraites par spaCy
    for entite in doc.ents:
        if entite.label_ == "LOC":  # LOC est l'étiquette pour les emplacements
            locations.append(entite.text)
    
    return locations
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
def extract_verbs(text):
   
    words = word_tokenize(text)
    tagged_words = pos_tag(words)
    verbs = [word for word, pos in tagged_words if pos.startswith('VB')]
    
    return verbs 
def extraire_personnes(texte):
    doc = nlp(texte)
    personnes = []
    for entite in doc.ents:
        if entite.label_ == "PER":  # PER est l'étiquette pour les personnes
            personnes.append(entite.text)
    return personnes

nlp = spacy.load("fr_core_news_sm")


def extraire_evenements(text):
    doc = nlp(text)
    evenements = []
    for entite in doc.ents:
        if entite.label_ == "EVENT":
            evenements.append(entite.text)
    return evenements

def extraire_verbes_passe_simple(text):
    doc = nlp(text)
    verbes_passe_simple = []
    for token in doc:
        print(token.text, token.pos_, token.tag_)
        if token.pos_ == "VERB" and token.tag_ == "VPS":
            verbes_passe_simple.append(token.text)
    return verbes_passe_simple
from django.shortcuts import render
from django.http import HttpResponse
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from django.shortcuts import render
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist


from django.shortcuts import render
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

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
        
        important_words = [word for word, _ in word_counter.most_common(2)]

        return important_words






    


def page1(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        impword= extract_important_words(text)
        sentences_with_dates = extract_dates_and_sentences(text)
        future_verbs = extract_verbs_in_future(text)
        summary = extract_summary(text)
        locations = extraire_locations(text)  # Add this line
        personnes = extraire_personnes(text)
        evenements_extrait = extraire_evenements(text)
        show = show_result(text)
        passe_compose = re.findall(r'\b\w+é\b', text)
        futur = re.findall(r'\b\w+ra\b', text)
        subjonctif = re.findall(r'\bqu\'.+\b(?:que\b)?', text)
        
        verbes_passe_simple_extrait = extraire_verbes_passe_simple(text)
        dates = my_view(text)
        gen_dates = []
        func = generate_nearby_dates(dates) 
        gen_dates.append(func)
        return render(request, 'text_pages/quiz.html', { 
            'dates' : dates ,
            'gen_dates' : gen_dates ,
             'impword': impword,
         'passe_compose': passe_compose,
            'futur': futur,
            'subjonctif': subjonctif,
            'show' : show ,
            'verbes_passe_simple': verbes_passe_simple_extrait , 
            'evenements': evenements_extrait ,
            'personnes' : personnes ,
                                                          'locations': locations ,
                                                          'text': text, 
                                                          'sentences_with_dates': sentences_with_dates, 
                                                          'future_verbs': future_verbs, 
                                                          'summary': summary})  # Include 'singular_verbs'

    return render(request, 'text_pages/page1.html')


def page2(request):
    return render(request, 'temp/aff.html')


nlp = spacy.load("fr_core_news_sm")

def extract_verbs_in_future(text):
    doc = nlp(text)
    future_verbs = []

    for token in doc:
        if token.pos_ == "VERB" and "Fut" in token.morph.get("Tense", ""):
            future_verbs.append(token.text)

    return future_verbs






