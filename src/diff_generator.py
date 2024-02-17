import difflib
import os

from src.sentiment_analyser import SentimentAnalyser


class DiffGenerator:

    @staticmethod
    def generate_html_diff(new_words, old_words):
        # Compute the differences
        differ = difflib.Differ()
        diff = list(differ.compare(new_words.split(), old_words.split()))

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

                    SentimentAnalyser.add_sentiment_to_result(new_sentence_string, old_sentence_string, result)

        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Get the parent directory of the current directory
        parent_directory = os.path.dirname(current_directory)
        html_template_path = os.path.join(parent_directory, "template", "diff_output_template.html")

        return DiffGenerator.replace_diff_body(html_template_path, ' '.join(result))

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

    #
    # @staticmethod
    # def has_full_stop(self, new_sentence_string, old_sentence_string):
    #     return old_sentence_string.find(".") != -1 and new_sentence_string.find(".")

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
    def replace_diff_body(template_file, body):
        # Read the content of the template file
        with open(template_file, 'r') as file:
            template_content = file.read()

        # Replace the placeholder with the body string
        updated_content = template_content.replace("$$$DIFF_BODY$$$", body)
        return updated_content



