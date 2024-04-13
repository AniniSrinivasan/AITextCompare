from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


class SimilarityAnalyser:

    @staticmethod
    def get_similarity(embeddings1, embeddings2):
        cosine_similarity = util.pytorch_cos_sim(embeddings1, embeddings2)
        return cosine_similarity

    @staticmethod
    def add_similarity_to_result(new_sentence_string, old_sentence_string, result, is_similarity_checked):
        if old_sentence_string.lower() != new_sentence_string.lower():

            embeddings1 = model.encode(new_sentence_string, convert_to_tensor=True)
            embeddings2 = model.encode(old_sentence_string, convert_to_tensor=True)

            cosine_similarity = SimilarityAnalyser.get_similarity(embeddings1, embeddings2)

            if is_similarity_checked:
                result.append(SimilarityAnalyser.get_emoji(cosine_similarity.item()))
            if cosine_similarity.item() < 0.7:
                return False

        return True

    @staticmethod
    def get_emoji(similarity_index):
        if similarity_index > 0.7:
            return """[Similarity: <span class="emoji">👍</span>]"""
        else:
            return """[Similarity: <span class="emoji">👎</span>]"""


