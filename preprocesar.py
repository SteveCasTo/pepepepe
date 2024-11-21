import pandas as pd
import re
import spacy

# Cargar el modelo de SpaCy en español
def cargar_modelo_spacy():
    return spacy.load("es_core_news_sm")

# Cargar los datos y preprocesarlos
def cargar_datos(archivo_csv):
    df = pd.read_csv(archivo_csv)
    stopwords_personalizadas = ["él","el","de","en","que","y","una","uno","a","del","por","ser","ese","para","con","su","al","este","haber","más","como","o","no","tener"]
    
    nlp = cargar_modelo_spacy()
    for palabra in stopwords_personalizadas:
        lex = nlp.vocab[palabra]
        lex.is_stop = True 
        lex.norm_ = palabra  # Normaliza la palabra para evitar errores con acentos

    def limpiar_texto_spacy(texto):
        if not isinstance(texto, str):
            return ""  # Si no es una cadena, devolver vacío
        texto = re.sub(r'[^a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s]', '', texto)
        texto = texto.lower()
        doc = nlp(texto)
        palabras_limpias = [token.lemma_ for token in doc if token.lemma_ not in stopwords_personalizadas and token.is_alpha]
        return ' '.join(palabras_limpias)

    df['news_clean'] = df['news'].apply(limpiar_texto_spacy)
    return df