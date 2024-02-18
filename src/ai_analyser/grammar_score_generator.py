from transformers import pipeline

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
        grammar_score = GrammarScoreGenerator.get_similarity_score(new_content, corrected_sentence)
        return GrammarScoreGenerator.get_html(grammar_score)

    @staticmethod
    def get_html(grammar_score):
        summary_template = f"""
                
                <h3>Grammar Score : {grammar_score}</h3> 
                
            """

        return summary_template





