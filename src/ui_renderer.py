import os
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QHBoxLayout, QLabel, QCheckBox, QFileDialog

from src.diff_generator import DiffGenerator


class UIRender(QWidget):
    def __init__(self, html_file, css_file=None):
        super(UIRender, self).__init__()

        layout = QVBoxLayout()

        # Add labels above the text areas with upload buttons
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
        original_upload_button = QPushButton()
        original_upload_button.setIcon(QIcon('../static/upload.png'))
        original_upload_button.setIconSize(QSize(16, 16))  # Fix the icon size here
        original_label_layout = QHBoxLayout()
        original_label_layout.addWidget(original_label)
        original_label_layout.addWidget(original_upload_button)
        original_upload_button.clicked.connect(self.upload_left_file)

        latest_label = QLabel("Latest Version")
        latest_upload_button = QPushButton()
        latest_upload_button.setIcon(QIcon('../static/upload.png'))
        latest_upload_button.setIconSize(QSize(16, 16))  # Fix the icon size here
        latest_label_layout = QHBoxLayout()
        latest_label_layout.addWidget(latest_label)
        latest_label_layout.addWidget(latest_upload_button)
        latest_upload_button.clicked.connect(self.upload_right_file)

        label_layout = QHBoxLayout()  # Use QHBoxLayout for placing widgets side by side
        label_layout.addLayout(original_label_layout)
        label_layout.addStretch(1)  # Add a stretchable space
        label_layout.addWidget(QLabel("   "))  # Add some additional space between the label sets
        label_layout.addLayout(latest_label_layout)
        return label_layout

    def upload_left_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Original File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.left_text_area.setPlainText(content)

    def upload_right_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Latest File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.right_text_area.setPlainText(content)

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

    def upload_left_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Original File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.left_text_area.setPlainText(content)

    def upload_right_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Latest File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.right_text_area.setPlainText(content)


