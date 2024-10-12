import os
import glob

# Импорт библиотек для обработки текста
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Импорт библиотек для векторизации и обработки
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import SentenceTransformer
import gensim

# Импорт библиотек для кластеризации
from sklearn.cluster import KMeans, DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import silhouette_score, pairwise
import numpy as np

# Загрузка nltk ресурсов
nltk.download('punkt')
nltk.download('stopwords')

from sklearn.metrics import silhouette_score

def read_and_preprocess_texts(folder_path):
    texts = []
    for file_path in glob.glob(os.path.join(folder_path, '*.txt')):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            # Предобработка
            tokens = word_tokenize(text.lower())
            filtered_text = ' '.join([word for word in tokens if word.isalnum()])
            texts.append(filtered_text)
    return texts

folder_path = 'second_task\sampled_texts'
documents = read_and_preprocess_texts(folder_path)

# Преобразование текстов в векторные представления
model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
embeddings = model.encode(documents)

# Кластеризация документов
num_clusters = 5
# Чтобы сделать результат более стабильным, цстановлено фиксированное значение для параметра random_state
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(embeddings)

labels = kmeans.labels_

# Оценка качества кластеризации
silhouette_avg = silhouette_score(embeddings, kmeans.labels_)
print(f'Silhouette Score: {silhouette_avg}')

# Пример классификации нового документа
def classify_new_document(new_document):
    # Предобработка
    tokens = word_tokenize(new_document.lower())
    filtered_text = ' '.join([word for word in tokens if word.isalnum()])
    
    # Преобразование в эмбеддинг
    new_embedding = model.encode([filtered_text])
    
    # Поиск ближайшего кластера
    nearest_neighbors = NearestNeighbors(n_neighbors=1)
    nearest_neighbors.fit(embeddings)
    nearest_index = nearest_neighbors.kneighbors(new_embedding, return_distance=False)
    
    return labels[nearest_index[0][0]]

# Пример использования на Lorem Ipsum (тк примеры текстов на английском, был использован перевод)
new_document = "There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain..."
predicted_cluster = classify_new_document(new_document)
print(f'Новый документ принадлежит кластеру: {predicted_cluster}')