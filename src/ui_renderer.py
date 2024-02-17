import os

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QHBoxLayout, QLabel, QCheckBox

from src.diff_generator import DiffGenerator


class UIRender(QWidget):
    def __init__(self, html_file, css_file=None):
        super(UIRender, self).__init__()

        layout = QVBoxLayout()

        # Add labels above the text areas
        label_layout = self.addLabel()
        layout.addLayout(label_layout)

        text_areas_layout = self.addTextArea()
        layout.addLayout(text_areas_layout)

        # Add a Compare button
        compare_button = self.addCompareButton()
        layout.addWidget(compare_button)

        # Add checkboxes for various features
        checkboxes_layout = self.addAICheckBoxes()
        layout.addLayout(checkboxes_layout)

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        self.setLayout(layout)
        self.render_from_files(html_file, css_file)

    def addLabel(self):
        original_label = QLabel("Original Version")
        latest_label = QLabel("Latest Version")
        label_layout = QHBoxLayout()
        label_layout.addWidget(original_label)
        label_layout.addWidget(latest_label)
        return label_layout

    def addCompareButton(self):
        compare_button = QPushButton("Compare")
        compare_button.clicked.connect(self.on_compare_clicked)
        compare_button.setSizePolicy(compare_button.sizePolicy().Expanding, compare_button.sizePolicy().Expanding)
        font = compare_button.font()
        font.setPointSize(18)  # Set the font size to 14
        compare_button.setFont(font)
        return compare_button

    def addTextArea(self):
        # Add two text areas for left and right content
        self.left_text_area = QTextEdit(self)
        self.right_text_area = QTextEdit(self)
        self.left_text_area.setMinimumSize(150, 150)
        self.right_text_area.setMinimumSize(150, 150)

        text_areas_layout = QHBoxLayout()
        text_areas_layout.addWidget(self.left_text_area)
        text_areas_layout.addWidget(self.right_text_area)
        return text_areas_layout

    def addAICheckBoxes(self):
        self.sentiment_checkbox = QCheckBox("Sentiment", self)
        self.similarity_checkbox = QCheckBox("Similarity", self)
        self.paraphrase_checkbox = QCheckBox("Paraphrase", self)
        self.summary_checkbox = QCheckBox("Summary", self)
        self.grammar_score_checkbox = QCheckBox("Grammar Score", self)
        checkboxes_layout = QHBoxLayout()
        checkboxes_layout.addWidget(self.sentiment_checkbox)
        checkboxes_layout.addWidget(self.similarity_checkbox)
        checkboxes_layout.addWidget(self.paraphrase_checkbox)
        checkboxes_layout.addWidget(self.summary_checkbox)
        checkboxes_layout.addWidget(self.grammar_score_checkbox)
        return checkboxes_layout

    def on_compare_clicked(self):
        # Get the content from the text areas
        left_content = self.left_text_area.toPlainText()
        right_content = self.right_text_area.toPlainText()

        # Generate HTML diff
        diff_html = DiffGenerator.generate_html_diff(left_content, right_content)



        # Write the HTML diff to a file in the same location
        output_file_path = os.path.join(os.path.dirname(__file__), "diff_output.html")
        with open(output_file_path, 'w') as f:
            f.write(diff_html)

        # Render the HTML diff
        self.web_view.setHtml(diff_html)

    def render_from_files(self, html_file, css_file=None):
        html_path = os.path.abspath(html_file)
        css_path = os.path.abspath(css_file) if css_file else None

        with open(html_path, 'r') as html_file:
            html_content = html_file.read()

        css_content = ""
        if css_path:
            with open(css_path, 'r') as css_file:
                css_content = css_file.read()

        self.render_html(html_content, css_content)

    def render_html(self, html, css=None):
        if css:
            html = f"<html><head><style>{css}</style></head><body>{html}</body></html>"
        else:
            html = f"<html><body>{html}</body></html>"

        self.web_view.setHtml(html)
