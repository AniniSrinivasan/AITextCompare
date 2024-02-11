from PyQt5.QtWidgets import QApplication

from renderer import UIRender

if __name__ == "__main__":
    app = QApplication([])

    # Specify the paths to your HTML and CSS files
    html_file_path = "/Users/aninisrinivasan/PycharmProjects/AITextCompare/template/diff_output.html"
    css_file_path = "/Users/aninisrinivasan/PycharmProjects/AITextCompare/template/styles.css"

    renderer = UIRender(html_file_path, css_file_path)  # Pass HTML and CSS file paths as positional arguments
    renderer.show()
    app.exec_()
