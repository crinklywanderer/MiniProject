# backend/chatbot_engine.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ChatbotEngine:
    def __init__(self, csv_path, additional_csv_path=None):
        # Load the primary dataset
        self.df = pd.read_csv(csv_path)

        # Load and combine additional dataset if provided
        if additional_csv_path:
            try:
                additional_df = pd.read_csv(additional_csv_path)

                # Check if the additional dataset has the required columns
                if 'Description' in additional_df.columns and 'Patient' in additional_df.columns and 'Doctor' in additional_df.columns:
                    # Transform the additional dataset to match the format of the primary dataset
                    transformed_df = pd.DataFrame({
                        'short_question': additional_df['Description'] + " " + additional_df['Patient'],
                        'short_answer': additional_df['Doctor']
                    })

                    # If the primary dataset has tags and label columns, add empty values for the additional dataset
                    if 'tags' in self.df.columns:
                        transformed_df['tags'] = [[] for _ in range(len(transformed_df))]
                    if 'label' in self.df.columns:
                        transformed_df['label'] = 1.0  # Assuming all entries are valid

                    # Combine the datasets
                    self.df = pd.concat([self.df, transformed_df], ignore_index=True)
                    print(f"Additional CSV loaded and combined successfully.")
            except Exception as e:
                print(f"Error loading additional CSV: {e}")

        # Initialize the vectorizer and transform the questions
        self.vectorizer = TfidfVectorizer()
        self.question_vecs = self.vectorizer.fit_transform(self.df['short_question'])

        print("CSV loaded successfully.")
        print("Number of questions:", len(self.df))
        print("Sample question:", self.df['short_question'].iloc[0])
        print("TF-IDF matrix shape:", self.question_vecs.shape)

    def get_response(self, user_input):
        user_vec = self.vectorizer.transform([user_input])
        sim_scores = cosine_similarity(user_vec, self.question_vecs)
        idx = sim_scores.argmax()
        return self.df.iloc[idx]['short_answer']

    def get_answer(self, user_query):
        try:
            query_vec = self.vectorizer.transform([user_query])
            similarities = cosine_similarity(query_vec, self.question_vecs).flatten()
            best_match_idx = similarities.argmax()
            best_score = similarities[best_match_idx]
            print(f"Best match index: {best_match_idx}, Score: {best_score}")
            if best_score < 0.1:
                return "I'm sorry, I couldn't understand your question."
            return self.df.iloc[best_match_idx]['short_answer']
        except Exception as e:
            print("Error during answer retrieval:", e)
            return "Oops! Something went wrong."
