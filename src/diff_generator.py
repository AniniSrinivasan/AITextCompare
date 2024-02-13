import difflib


class DiffGenerator:
    @staticmethod
    def generate_html_diff_1(old_text, new_text):
        diffHtml = difflib.HtmlDiff()
        return diffHtml.make_file(old_text.splitlines(), new_text.splitlines())

    @staticmethod
    def generate_html_diff(new_words, old_words):
        # Compute the differences
        differ = difflib.Differ()
        diff = list(differ.compare(old_words.split(), new_words.split()))

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

        return DiffGenerator.replace_diff_body("/Users/aninisrinivasan/PycharmProjects/AITextCompareProject/template/diff_output_template.html", ' '.join(result))

    @staticmethod
    def replace_diff_body(template_file, body):
        # Read the content of the template file
        with open(template_file, 'r') as file:
            template_content = file.read()

        # Replace the placeholder with the body string
        updated_content = template_content.replace("$$$DIFF_BODY$$$", body)
        return updated_content
        # # Write the modified content back to the file
        # with open(template_file, 'w') as file:
        #     file.write(updated_content)



