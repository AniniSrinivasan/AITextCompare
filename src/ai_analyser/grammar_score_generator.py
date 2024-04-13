import torch
from transformers import BertTokenizer, BertForMaskedLM
from spellchecker import SpellChecker
from transformers import pipeline

from difflib import SequenceMatcher

corrector = pipeline("text2text-generation", model="pszemraj/flan-t5-large-grammar-synthesis")


class GrammarScoreGenerator:

    @staticmethod
    def get_similarity_score(original_sentence, corrected_sentence):
        # Calculate the grammar score as the percentage of similarity between the two sentences
        grammar_score = 100 - (abs(len(original_sentence) - len(corrected_sentence)) / len(original_sentence) * 100)
        return int(grammar_score)

    @staticmethod
    # Function to calculate the grammar score for a given sentence
    def get_grammar_score_html(new_content):
        corrected_sentence = corrector(new_content)[0]["generated_text"]

        print("corrected_sentence : " + corrected_sentence)
        # grammar_score = GrammarScoreGenerator.get_similarity_score(new_content, corrected_sentence)
        grammar_score = GrammarScoreGenerator.calculate_grammar_score(new_content, corrected_sentence)

        return GrammarScoreGenerator.get_html(int(grammar_score))

    @staticmethod
    def calculate_grammar_score(original, corrected):
        # Tokenize both sentences by splitting on spaces
        original_tokens = original.split()
        corrected_tokens = corrected.split()

        # Use SequenceMatcher to find the number of matches
        matcher = SequenceMatcher(None, original_tokens, corrected_tokens)
        matches = matcher.get_matching_blocks()

        # Calculate the total number of matching tokens
        num_matching = sum(match.size for match in matches)

        # If there are no tokens in the original sentence, avoid division by zero
        if len(original_tokens) == 0:
            return 0

        # The grammar score is the percentage of tokens in the original sentence that remain unchanged
        grammar_score = (num_matching / len(original_tokens)) * 100
        return grammar_score

    @staticmethod
    def get_html(grammar_score):
        summary_template = f"""

                <h3>Grammar Score : {grammar_score}</h3> 

            """

        return summary_template


# Example usage
if __name__ == "__main__":
    generator = GrammarScoreGenerator()
    test_sentences = ["sasd sdfsfd sfdf hghghg hg", "This is good or bad. i dont know."]
    for sentence in test_sentences:
        print(f"Sentence: {sentence} - Score: {generator.get_grammar_score_html(sentence)}")
