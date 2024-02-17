
class ParaphraseAnalyser:

    @staticmethod
    def add_paraphrase_to_result(new_sentence_string, old_sentence_string, result, is_same_sentiment, is_similar):
        if old_sentence_string.lower() != new_sentence_string.lower():
            if is_same_sentiment and is_similar:
                result.append(ParaphraseAnalyser.get_emoji(True))
            else:
                result.append(ParaphraseAnalyser.get_emoji(False))

    @staticmethod
    def get_emoji(is_paraphrased):
        if is_paraphrased:
            return """[<span class="emoji">🔄</span> Paraphrased]"""
        else:
            return """[<span class="emoji">❌</span> Not Paraphrased]"""

