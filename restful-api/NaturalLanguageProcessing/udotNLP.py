import yake
# from sentence_transformers import SentenceTransformer
# from tqdm import tqdm


def text2Keywords(data: list, _ngram: int = 3, _top: int = 25, _windowSize: int = 1) -> list:
    """
    :param data: List of texts. It is a 1D list where each element is a text.
    :param _ngram: How many words will be there in a sentence.
    :param _top: How many phrases we want to return.
    :param _windowSize: To how many words we are going to make comparisons.
    :return: A 1D list where each element is a String that has all the keywords for it.
    """

    kw_extractor = yake.KeywordExtractor(n=_ngram, top=_top, windowsSize=_windowSize)

    return_list = []
    if not (type(data) == list):
        #print("The given input is not a list, converting to list")
        data = [data]

    for text in data:
        keywords = kw_extractor.extract_keywords(text)

        keywords_list = []
        for _keywords in keywords:
            keywords_list.append(_keywords[0])

        return_list.append(keywords_list)

    for i in range(len(return_list)):
        str_tmp = ""
        for keyword in return_list[i]:
            str_tmp += str(keyword) + " "
        return_list[i] = str_tmp

    return return_list


def text2Embeddings(sentences: list, sentence_transformer: str = "msmarco-distilbert-base-v4") -> list:
    """

    :param sentences: data: List of texts. It is a 1D list where each element is a text.
    :param sentence_transformer: Model Name of the sentence_transformer
    :return:
    """
    model = SentenceTransformer(sentence_transformer)

    embeddings = []
    for sentence in sentences:
        embedding = model.encode(sentence)
        embeddings.append(embedding)

    return embeddings
