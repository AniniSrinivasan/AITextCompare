from transformers import BartTokenizer, BartForConditionalGeneration

class SummaryGenerator:

    @staticmethod
    def summarize_text(input_text, max_length=150):
        # Load pre-trained model and tokenizer
        model_name = "facebook/bart-large-cnn"
        tokenizer = BartTokenizer.from_pretrained(model_name)
        model = BartForConditionalGeneration.from_pretrained(model_name)
        # Tokenize input text and generate summary
        inputs = tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs["input_ids"], max_length=max_length, length_penalty=2.0, num_beams=4,
                                     early_stopping=True)
        # Decode the generated summary
        return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    @staticmethod
    def get_summary_html(new_content):
        words = new_content.split()

        # Find the size (number of words)
        total_words = len(words)
        if total_words > 100:
            summary_string = SummaryGenerator.summarize_text(new_content)
            return SummaryGenerator.get_html(summary_string)
        else:
            return ""

    @staticmethod
    def get_html(summary_string):
        summary_template = f"""
                
                <h3>Summary </h3>
                <tbody>{summary_string}</tbody>
                   
            """

        return summary_template





