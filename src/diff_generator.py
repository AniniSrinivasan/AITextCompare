import difflib
import os

from src.ai_analyser.grammar_score_generator import GrammarScoreGenerator
from src.ai_analyser.paraphrase_analyser import ParaphraseAnalyser
from src.ai_analyser.sentiment_analyser import SentimentAnalyser
from src.ai_analyser.similarity_analyser import SimilarityAnalyser
from src.ai_analyser.summary_generator import SummaryGenerator


class DiffGenerator:

    @staticmethod
    def generate_html_diff(new_content, old_content):
        # Compute the differences
        differ = difflib.Differ()
        diff = list(differ.compare(new_content.split(), old_content.split()))

        current_old_sentence = []
        current_new_sentence = []
        result = []
        for index, item in enumerate(diff):
            itemValue = item[2:].strip()

            DiffGenerator.add_diff_highliter(item, itemValue, result)

            # Trace back each sentence
            DiffGenerator.trace_back_old_new_sentence(current_new_sentence, current_old_sentence, item, itemValue)

            if itemValue.endswith(".") or index == len(diff) - 1:
                old_sentence_string = DiffGenerator.join_array_get_string(' ', current_old_sentence)
                new_sentence_string = DiffGenerator.join_array_get_string(' ', current_new_sentence)

                if (old_sentence_string.find(".") != -1 and new_sentence_string.find(".") != -1) or index == len(diff) - 1:

                    current_old_sentence = []
                    current_new_sentence = []

                    # is_same_sentiment = SentimentAnalyser.add_sentiment_to_result(new_sentence_string, old_sentence_string, result)
                    # is_similar = SimilarityAnalyser.add_similarity_to_result(new_sentence_string, old_sentence_string, result)
                    # ParaphraseAnalyser.add_paraphrase_to_result(new_sentence_string, old_sentence_string, result, is_same_sentiment, is_similar)

        diff_string = DiffGenerator.join_array_get_string(' ', result)

        summary_html = SummaryGenerator.get_summary_html(new_content)
        grammar_html = GrammarScoreGenerator.get_grammar_score_html(new_content)

        return DiffGenerator.replace_diff_body(diff_string, summary_html, grammar_html)

    @staticmethod
    def trace_back_old_new_sentence(current_new_sentence, current_old_sentence, item, itemValue):
        if item.startswith('- '):
            isLineHasDelete = True
            current_old_sentence.append(f"{itemValue}")
        elif item.startswith('+ '):
            isLineHasAdd = True
            current_new_sentence.append(f"{itemValue}")
        elif item.startswith('? '):
            # Ignore the question marks used by difflib
            pass
        else:
            current_old_sentence.append(item)
            current_new_sentence.append(item)

    @staticmethod
    def add_diff_highliter(item, itemValue, result):
        if item.startswith('- '):
            result.append(f"<span class=\"diff_sub\">{itemValue} </span>")  # Red highlight for deleted words
        elif item.startswith('+ '):
            result.append(f"<span class=\"diff_add\">{itemValue} </span>")  # Green highlight for added words
        elif item.startswith('? '):
            # Ignore the question marks used by difflib
            pass
        else:
            result.append(item)

    @staticmethod
    def join_array_get_string(delimiter, array):
        return delimiter.join(array)

    @staticmethod
    def replace_diff_body(diff_html, summary_html, grammar_html):
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Get the parent directory of the current directory
        parent_directory = os.path.dirname(current_directory)
        template_file = os.path.join(parent_directory, "template", "diff_output_template.html")

        # Read the content of the template file
        with open(template_file, 'r') as file:
            template_content = file.read()

        # Replace the placeholder with the body string
        updated_content = template_content.replace("$$$DIFF_BODY$$$", diff_html)
        updated_content = updated_content.replace("$$$SUMMARY$$$", summary_html)
        updated_content = updated_content.replace("$$$GRAMMAR_SCORE$$$", grammar_html)

        return updated_content



