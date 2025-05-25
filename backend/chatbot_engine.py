# backend/chatbot_engine.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ChatbotEngine:
    def __init__(self, csv_path, additional_csv_path=None):
        try:
            self.df = pd.read_csv(csv_path)

            if additional_csv_path:
                additional_df = pd.read_csv(additional_csv_path)

                if {'Description', 'Patient', 'Doctor'}.issubset(additional_df.columns):
                    transformed_df = pd.DataFrame({
                        'short_question': additional_df['Description'] + " " + additional_df['Patient'],
                        'short_answer': additional_df['Doctor']
                    })

                    if 'tags' in self.df.columns:
                        transformed_df['tags'] = [[] for _ in range(len(transformed_df))]
                    if 'label' in self.df.columns:
                        transformed_df['label'] = 1.0

                    self.df = pd.concat([self.df, transformed_df], ignore_index=True)
                    print(f"✅ Additional CSV loaded and merged.")
        except Exception as e:
            print(f"⚠️ Error loading datasets: {e}")
            self.df = pd.DataFrame(columns=['short_question', 'short_answer'])

        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer()
        self.question_vecs = self.vectorizer.fit_transform(self.df['short_question'])

        print("📁 Dataset initialized.")
        print("🧠 Total Q&A pairs:", len(self.df))

    def get_response(self, user_input):
        try:
            user_vec = self.vectorizer.transform([user_input])
            sim_scores = cosine_similarity(user_vec, self.question_vecs).flatten()
            best_match_idx = sim_scores.argmax()
            return self.df.iloc[best_match_idx]['short_answer']
        except Exception as e:
            print("⚠️ Error in get_response:", e)
            return "Oops! Something went wrong."

    def get_answer(self, user_query):
        try:
            query_vec = self.vectorizer.transform([user_query])
            similarities = cosine_similarity(query_vec, self.question_vecs).flatten()
            best_match_idx = similarities.argmax()
            best_score = similarities[best_match_idx]

            print(f"🔍 Best match index: {best_match_idx}, Score: {best_score}")

            if best_score < 0.5:
                return "I'm sorry, I couldn't understand your question."

            return self.df.iloc[best_match_idx]['short_answer']
        except Exception as e:
            print("⚠️ Error during get_answer:", e)
            return "Oops! Something went wrong."
