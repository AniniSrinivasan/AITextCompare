AI Text Compare
===============

AI Text Compare is a Python desktop application that compares two versions of text. It uses a PyQt5 user interface, renders the comparison as HTML, and can optionally add AI-based analysis for changed sentences and latest-version content.


What This Project Can Do
------------------------

- Compare an "Original Version" and a "Latest Version" of text.
- Highlight word-level differences:
  - added words are shown in green
  - deleted words are shown in red
- Let users paste text directly into the app.
- Let users upload `.txt` files for both versions.
- Save each comparison into a local `history/` folder.
- Reload earlier comparisons from the in-app history list.
- Optionally add AI analysis after comparison:
  - Sentiment: detects positive, neutral, or negative sentiment.
  - Similarity: checks semantic similarity between changed sentence pairs.
  - Paraphrase: marks text as paraphrased when sentiment and similarity both match.
  - Summary: summarizes the latest text when it has more than 100 words.
  - Grammar Score: compares the latest text with an AI-corrected version and returns a score.


Project Structure
-----------------

```text
src/
  gui_controller.py                  Starts the PyQt desktop app
  ui_renderer.py                     Builds the UI, handles uploads, comparison history, and HTML rendering
  diff_generator.py                  Generates word-level diff output and attaches AI analysis results
  ai_analyser/
    sentiment_analyser.py            Sentiment analysis using finiteautomata/bertweet-base-sentiment-analysis
    similarity_analyser.py           Sentence similarity using paraphrase-MiniLM-L6-v2
    paraphrase_analyser.py           Paraphrase result based on sentiment and similarity checks
    summary_generator.py             Summary generation using facebook/bart-large-cnn
    grammar_score_generator.py       Grammar score using pszemraj/flan-t5-large-grammar-synthesis

template/
  diff_output.html                   Initial empty HTML view
  diff_output_template.html          HTML template for comparison results
  styles.css                         Basic styling

sample/
  OriginalText.txt                   Sample original text
  LatestText.txt                     Sample latest text

static/
  upload.png                         Upload button icon

tests/
  test_ui_renderer.py                Existing UI test file
```


Setup
-----

Use Python 3.10 or newer. Python 3.11 is recommended because this project was developed with Python 3.11.

From the project root, create and activate a virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Install the required packages:

```bash
python -m pip install PyQt5 PyQtWebEngine torch torchvision tensorflow sentence-transformers transformers pyspellchecker
```

If `python3.11` is not available on your machine, check your installed Python version:

```bash
python3 --version
```

Then create the virtual environment with the available Python command, for example:

```bash
python3 -m venv .venv
```


Run the App
-----------

Start the desktop app from the project root:

```bash
source .venv/bin/activate
python src/gui_controller.py
```

How to use it:

1. Paste text into the Original Version and Latest Version text boxes, or upload `.txt` files with the upload buttons.
2. Click Compare.
3. Review the highlighted diff in the result area.
4. Select any AI checkboxes you want.
5. Click Compare again to regenerate the output with those AI results included.


Sample Input
------------

The `sample/` folder contains two small files that can be used for a quick manual check:

```text
sample/OriginalText.txt
sample/LatestText.txt
```


AI Model Notes
--------------

The AI features use Hugging Face models through `transformers` and `sentence-transformers`. The first run can take longer because the models may need to be downloaded and cached locally.

Models used:

- `finiteautomata/bertweet-base-sentiment-analysis`
- `paraphrase-MiniLM-L6-v2`
- `facebook/bart-large-cnn`
- `pszemraj/flan-t5-large-grammar-synthesis`

An internet connection may be required the first time these models are loaded.


Run Tests
---------

Run the existing tests with:

```bash
source .venv/bin/activate
python -m unittest
```

Note: the current UI test constructs PyQt widgets and may require a working desktop/GUI environment.


Troubleshooting
---------------

- If PyQt imports fail, make sure both `PyQt5` and `PyQtWebEngine` are installed in the active virtual environment.
- If AI imports fail, make sure `transformers`, `sentence-transformers`, and `torch` are installed.
- If the app cannot find the upload icon or templates, run it from the project root.
- If model loading is slow, wait for the first download/cache step to complete.
- If comparison history appears in the project folder, that is expected. The app creates a local `history/` directory when comparisons are made.
