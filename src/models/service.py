import pickle
from sentence_transformers import SentenceTransformer

model = pickle.load(open("model.pkl", "rb"))
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def preprocess(text):
    return str(text).strip().lower()

def predict(text: str):
    text = preprocess(text)
    embedding = embed_model.encode([text])
    prediction = model.predict(embedding)[0]
    return prediction