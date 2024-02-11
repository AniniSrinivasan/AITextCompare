import unittest
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QApplication, QPushButton

from src.ui_renderer import UIRender


class TestUIRender(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])

    def tearDown(self):
        self.app.quit()

    def test_on_compare_clicked(self):
        # Mock the QTextEdit widget
        left_text_area = MagicMock()
        left_text_area.toPlainText.return_value = "Left content"
        right_text_area = MagicMock()
        right_text_area.toPlainText.return_value = "Right content"

        # Mock the QWebEngineView widget
        web_view = MagicMock()

        # Create an instance of UIRender
        renderer = UIRender("path_to_html_file", "path_to_css_file")
        renderer.left_text_area = left_text_area
        renderer.right_text_area = right_text_area
        renderer.web_view = web_view

        # Mock the generate_html_diff method
        renderer.generate_html_diff = MagicMock(return_value="<html>Diff</html>")

        # Trigger the on_compare_clicked method
        renderer.on_compare_clicked()

        # Assert that QTextEdit.toPlainText was called
        left_text_area.toPlainText.assert_called_once()
        right_text_area.toPlainText.assert_called_once()

        # Assert that generate_html_diff was called with correct arguments
        renderer.generate_html_diff.assert_called_once_with("Left content", "Right content")

        # Assert that QWebEngineView.setHtml was called with correct arguments
        web_view.setHtml.assert_called_once_with("<html>Diff</html>")

if __name__ == '__main__':
    unittest.main()
