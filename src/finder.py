from typing import List, Optional, Tuple

import numpy as np

from thefuzz.fuzz import partial_token_set_ratio

from transformers import AutoTokenizer, AutoModel
import torch

import re

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model_name = "cointegrated/LaBSE-en-ru"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).to(device)


def find_closest(query: str, candidates: List[str]) -> Optional[Tuple[int, int]]:
    """
    Поиск на основе соотношения множеств токенов (в нижнем регистре)

    :param query: Запрос
    :param candidates: Список кандидатов
    :return: Индекс ближайшего и соотношение
    """

    if len(candidates) == 0:
        return None
    ratios = [partial_token_set_ratio(query.lower(), candidate.lower()) for candidate in candidates]
    idx = np.argmax(ratios)
    return idx, ratios[idx]


def clear_text(text: str) -> str:
    """
    :param text: Исходный текст
    :return: Очищенный текст
    """

    text = re.sub(r"[«»'`]", '"', text)
    text = re.sub(r"\"+", '"', text)
    text = text.replace('\n', ' ')
    text = re.sub(r" +", ' ', text)
    return text


def get_embeds(sentences: List[str]) -> np.ndarray:
    """
    Построить эмбеддинги для предложений с помощью модели LaBSE

    :param sentences: Список предложений
    :return: Двумерный массив эмбеддингов размера 768
    """

    encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=128, return_tensors='pt').to(device)
    with torch.no_grad():
        model_output = model(**encoded_input)
    embeddings = model_output.pooler_output
    embeddings = torch.nn.functional.normalize(embeddings).detach().cpu()
    return np.array([embedding.numpy() for embedding in embeddings])


class Finder:
    """
    Класс для поиска ближайшего типа запроса и получения его атрибутов
    """

    def __init__(self, types: List[str]) -> None:
        """
        :param types: Список из названий запросов
        """

        self._type_embeds = get_embeds([clear_text(t) for t in types])

    def get(self, query: str, candidates: List[List[str]]) -> Tuple[int, List[Optional[Tuple[int, int]]]]:
        """
        :param query: Запрос
        :param candidates: Список кандидатов
        :return: Ближайший тип и лучшие кандидаты
        """

        nearest = []
        for values in candidates:
            nearest.append(find_closest(query, values))

        query = clear_text(query)

        query_embed = get_embeds([query])
        type_idx = np.argmax(query_embed @ self._type_embeds.T, axis=1)[0]

        return type_idx, nearest
