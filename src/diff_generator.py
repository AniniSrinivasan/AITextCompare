import difflib


class DiffGenerator:
    @staticmethod
    def generate_html_diff(old_text, new_text):
        d = difflib.HtmlDiff()
        return d.make_file(old_text.splitlines(), new_text.splitlines())
