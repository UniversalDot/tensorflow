import yake
from tqdm import tqdm


def textKeywords(data: list, _ngram: int = 3, _top: int = 25, _windowSize: int = 1) -> list:
    """

    :param data: List of texts. It is a 1D list where each element is a text
    :param _ngram: How many words will be there in a sentence
    :param _top: How many phrases we want to return
    :param _windowSize: To how many words we are going to make comparisons.
    :return: A 1D list where each element is a String that has all the keywords for it.
    """

    kw_extractor = yake.KeywordExtractor(n=_ngram, top=_top, windowsSize=_windowSize)

    return_list = []
    for text in tqdm(data):
        keywords = kw_extractor.extract_keywords(text)

        keywords_list = []
        for _keywords in keywords:
            keywords_list.append(_keywords[0])

        return_list.append(keywords_list)

    for i in tqdm(range(len(return_list))):
        str_tmp = ""
        for keyword in return_list[i]:
            str_tmp += str(keyword) + " "
        return_list[i] = str_tmp

    return return_list