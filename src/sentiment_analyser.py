from transformers import pipeline, AutoConfig

# Creating a sentiment analysis pipeline using the default model
sentiment_pipeline = pipeline("sentiment-analysis")

# Creating a sentiment analysis pipeline using a specific model (BERTweet)
model_name = "finiteautomata/bertweet-base-sentiment-analysis"
config = AutoConfig.from_pretrained(model_name)
specific_model = pipeline("sentiment-analysis", model=model_name, config=config)


class SentimentAnalyser:

    @staticmethod
    def get_sentiment(sentence):
        sentiment = specific_model(sentence)[0]['label']
        return sentiment

    @staticmethod
    def add_sentiment_to_result(new_sentence_string, old_sentence_string, result):
        if old_sentence_string.lower() == new_sentence_string.lower():
            sentiment = SentimentAnalyser.get_sentiment(old_sentence_string)

            result.append(SentimentAnalyser.get_emoji(sentiment))

        else:
            old_sentiment = SentimentAnalyser.get_sentiment(old_sentence_string)
            new_sentiment = SentimentAnalyser.get_sentiment(new_sentence_string)

            if old_sentiment == new_sentiment:
                result.append(SentimentAnalyser.get_emoji(old_sentiment))
            else:
                result.append(
                    "[Sentiment:"
                    + SentimentAnalyser.get_emoji_alone(old_sentiment)
                    + """<span class="arrow">→</span>"""
                    + SentimentAnalyser.get_emoji_alone(new_sentiment)
                    + "]")

    @staticmethod
    def get_emoji(sentiment):
        return "[Sentiment:" + SentimentAnalyser.get_emoji_alone(sentiment) + "]"

    @staticmethod
    def get_emoji_alone(sentiment):
        if sentiment == "NEU":
            return """ <span class="emoji">😐</span>"""
        elif sentiment == "POS":
            return """<span class="emoji">😊</span>"""
        elif sentiment == "NEG":
            return """<span class="emoji">😞</span>"""

