import os
from PyQt5.QtWidgets import QApplication
from ui_renderer import UIRender

if __name__ == "__main__":
    app = QApplication([])

    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Get the parent directory of the current directory
    parent_directory = os.path.dirname(current_directory)

    # Specify the relative paths to your HTML and CSS files
    html_file_path = os.path.join(parent_directory, "template", "diff_output.html")
    css_file_path = os.path.join(parent_directory, "template", "styles.css")

    renderer = UIRender(html_file_path, css_file_path)  # Pass HTML and CSS file paths as positional arguments
    renderer.show()
    app.exec_()
