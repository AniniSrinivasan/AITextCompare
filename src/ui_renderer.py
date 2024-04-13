import os
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QHBoxLayout, QLabel, QCheckBox, QFileDialog, QFrame, QListWidget, QListWidgetItem

from src.diff_generator import DiffGenerator

class UIRender(QWidget):
    def __init__(self, html_file, css_file=None):
        super(UIRender, self).__init__()

        # Initialise history list
        self.history = []

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

        # Add history list
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.load_left_content_from_history)
        layout.addWidget(self.history_list)

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        self.setLayout(layout)
        self.render_from_files(html_file, css_file)

    def load_left_content_from_history(self, item):
        # Get selected history item text (e.g., compare_1)
        history_item = item.text()

        # Extract the index from the history item text (e.g., 1)
        compare_index = int(history_item.split('_')[1])

        # Load left and right content from the corresponding history files
        left_file_path = os.path.join('history', f'compare_{compare_index}_left.txt')
        right_file_path = os.path.join('history', f'compare_{compare_index}_right.txt')

        if os.path.exists(left_file_path):
            with open(left_file_path, 'r') as left_file:
                left_content = left_file.read()
                self.left_text_area.setPlainText(left_content)

        if os.path.exists(right_file_path):
            with open(right_file_path, 'r') as right_file:
                right_content = right_file.read()
                self.right_text_area.setPlainText(right_content)

    def addHistoryPanel(self):
        panel = QFrame()
        panel_layout = QVBoxLayout()
        panel_layout.setAlignment(Qt.AlignTop)

        # Add a button to toggle the visibility of the history panel
        toggle_button = QPushButton("History")
        toggle_button.clicked.connect(self.toggle_history_panel)
        panel_layout.addWidget(toggle_button)

        # Add a list widget to display the compare history
        self.history_list = QListWidget()
        panel_layout.addWidget(self.history_list)

        panel.setLayout(panel_layout)
        return panel

    def toggle_history_panel(self):
        if self.history_panel.isHidden():
            self.history_panel.show()
        else:
            self.history_panel.hide()

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

        # Disable the checkboxes
        self.sentiment_checkbox.setEnabled(False)
        self.similarity_checkbox.setEnabled(False)
        self.paraphrase_checkbox.setEnabled(False)
        self.summary_checkbox.setEnabled(False)
        self.grammar_score_checkbox.setEnabled(False)

        checkboxes_layout = QHBoxLayout()
        checkboxes_layout.addWidget(self.sentiment_checkbox)
        checkboxes_layout.addWidget(self.similarity_checkbox)
        checkboxes_layout.addWidget(self.paraphrase_checkbox)
        checkboxes_layout.addWidget(self.summary_checkbox)
        checkboxes_layout.addWidget(self.grammar_score_checkbox)
        return checkboxes_layout

    def on_compare_clicked(self):

        self.sentiment_checkbox.setEnabled(True)
        self.similarity_checkbox.setEnabled(True)
        self.paraphrase_checkbox.setEnabled(True)
        self.summary_checkbox.setEnabled(True)
        self.grammar_score_checkbox.setEnabled(True)

        # Get the content from the text areas
        left_content = self.left_text_area.toPlainText()
        right_content = self.right_text_area.toPlainText()

        # Save compared files to local folder
        if not os.path.exists('history'):
            os.makedirs('history')

        compare_index = len(self.history) + 1
        compare_name = f'compare_{compare_index}'
        compare_left_path = os.path.join('history', f'{compare_name}_left.txt')
        compare_right_path = os.path.join('history', f'{compare_name}_right.txt')

        with open(compare_left_path, 'w') as left_file:
            left_file.write(left_content)

        with open(compare_right_path, 'w') as right_file:
            right_file.write(right_content)

        # Update history list
        self.history.append(compare_name)
        self.update_history_list()

        # Generate HTML diff
        diff_html = DiffGenerator.generate_html_diff(left_content, right_content,
                                                     self.sentiment_checkbox.isChecked(),
                                                     self.similarity_checkbox.isChecked(),
                                                     self.paraphrase_checkbox.isChecked(),
                                                     self.summary_checkbox.isChecked(),
                                                     self.grammar_score_checkbox.isChecked())

        # Render the HTML diff
        self.web_view.setHtml(diff_html)

    def update_history_list(self):
        self.history_list.clear()
        for item in self.history:
            list_item = QListWidgetItem(item)
            self.history_list.addItem(list_item)

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
