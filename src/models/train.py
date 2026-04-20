
import os
import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

#Preprocessing
# We are not performing too much pre processing becuase in embeddings it will loose the meaning 
def preprocess(text):
    return str(text).strip().lower()


#Load Data
def load_data():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    file_path = os.path.join(project_root, 'data', 'processed', 'sampled_complaints.csv')
    df = pd.read_csv(file_path)  

    df = df[['issue', 'sub_issue', 'consumer_complaint_narrative', 'product']].copy()
    df['sub_issue'] = df['sub_issue'].fillna('')
    df['consumer_complaint_narrative'] = df['consumer_complaint_narrative'].fillna('')

    df['combined_text'] = (
        df['issue'] + " " +
        df['sub_issue'] + " " +
        df['consumer_complaint_narrative']
    )

    df['combined_text'] = df['combined_text'].apply(preprocess)

    df = df[df['product'].notna()]

    return df

#Embedding
def generate_embeddings(texts, model):
    return model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True
    )

#Training
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    return model

#Main Pipeline
def main():
    print("Loading data...")
    df = load_data()

    print("Loading embedding model...")
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Generating embeddings...")
    X = generate_embeddings(df['combined_text'].tolist(), embed_model)
    y = df['product'].values

    print("Training model...")
    model = train_model(X, y)

    print("Saving model...")
    pickle.dump(model, open("model.pkl", "wb"))

    print("Training complete!")


if __name__ == "__main__":
    main()