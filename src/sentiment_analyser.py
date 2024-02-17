from transformers import pipeline, AutoConfig

# Creating a sentiment analysis pipeline using the default model
sentiment_pipeline = pipeline("sentiment-analysis")

# Creating a sentiment analysis pipeline using a specific model (BERTweet)
model_name = "finiteautomata/bertweet-base-sentiment-analysis"
#specific_model = pipeline(model=model_name)
config = AutoConfig.from_pretrained(model_name)
specific_model = pipeline("sentiment-analysis", model=model_name, config=config)


class SentimentAnalyser:

    @staticmethod
    def get_sentiment(sentence):
        sentiment = specific_model(sentence)[0]['label']
        print(sentiment)