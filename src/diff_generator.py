import difflib
import os


class DiffGenerator:

    @staticmethod
    def generate_html_diff(new_words, old_words):
        # Compute the differences
        differ = difflib.Differ()
        diff = list(differ.compare(new_words.split(), old_words.split()))

        result = []
        for index, item in enumerate(diff):
            if item.startswith('- '):
                result.append(f"<span class=\"diff_sub\">{item[2:]} </span>")  # Strikethrough for deleted words
            elif item.startswith('+ '):
                result.append(f"<span class=\"diff_add\">{item[2:]} </span>")  # Bold for added words
            elif item.startswith('? '):
                # Ignore the question marks used by difflib
                pass
            else:
                result.append(item)

        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Get the parent directory of the current directory
        parent_directory = os.path.dirname(current_directory)
        html_template_path = os.path.join(parent_directory, "template", "diff_output_template.html")
        return DiffGenerator.replace_diff_body(html_template_path, ' '.join(result))

    @staticmethod
    def replace_diff_body(template_file, body):
        # Read the content of the template file
        with open(template_file, 'r') as file:
            template_content = file.read()

        # Replace the placeholder with the body string
        updated_content = template_content.replace("$$$DIFF_BODY$$$", body)
        return updated_content



