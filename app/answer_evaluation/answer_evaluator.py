import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import Levenshtein

class AnswerComparator:
    def __init__(self):
        # Download NLTK stopwords and load spaCy model
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))
        self.nlp = spacy.load('en_core_web_sm')
        self.vectorizer = None
        self.tfidf_matrix = None
        
    def preprocess(self, text):
        doc = self.nlp(text.lower())
        tokens = [token.lemma_ for token in doc if token.is_alpha and token.text not in self.stop_words]
        return ' '.join(tokens)

    def calculate_levenshtein_distance(self, answer1, answer2):
        return Levenshtein.distance(answer1, answer2)

    def get_tfidf_vectorizer(self, corpus):
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def compare_answer(self, user_answer, correct_answer, leven_threshold=5, cosine_threshold=0.5):
        if self.vectorizer is None or self.tfidf_matrix is None:
            raise ValueError("TF-IDF vectorizer and matrix not initialized. Call get_tfidf_vectorizer() first.")
        
        user_answer_processed = self.preprocess(user_answer)
        correct_answer_processed = self.preprocess(correct_answer)
        
        # Levenshtein distance
        levenshtein_distance = self.calculate_levenshtein_distance(user_answer_processed, correct_answer_processed)
        
        # Cosine similarity
        user_tfidf = self.vectorizer.transform([user_answer_processed])
        correct_tfidf = self.vectorizer.transform([correct_answer_processed])
        cosine_sim = cosine_similarity(user_tfidf, correct_tfidf).flatten()[0]
        
        # Decision making
        if levenshtein_distance <= leven_threshold or cosine_sim >= cosine_threshold:
            return True, levenshtein_distance, cosine_sim
        else:
            return False, levenshtein_distance, cosine_sim

# # Example usage
# if __name__ == "__main__":
#     comparator = AnswerComparator()
    
#     correct_answers = ["Paris is the capital of France.", "Water boils at 100 degrees Celsius."]
#     preprocessed_answers = [comparator.preprocess(answer) for answer in correct_answers]
    
#     comparator.get_tfidf_vectorizer(preprocessed_answers)
    
#     user_answer = "The capital of France is Paris."
    
#     for correct_answer in correct_answers:
#         is_correct, levenshtein_distance, cosine_sim = comparator.compare_answer(user_answer, correct_answer)
#         print(f"Levenshtein Distance: {levenshtein_distance}, Cosine Similarity: {cosine_sim}")
#         if is_correct:
#             print("The answer is correct.")
#         else:
#             print("The answer is incorrect.")
