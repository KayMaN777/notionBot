from dataclasses import dataclass
from typing import List, Union

import numpy as np

from transformers import AutoTokenizer, AutoModel
import torch

from nltk.tokenize import RegexpTokenizer
import re

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model_name = "cointegrated/LaBSE-en-ru"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).to(device)

name_tokenizer = RegexpTokenizer(r"\"[^\"]+\"")
date_tokenizer = RegexpTokenizer(r"\d{2}\.\d{2}\.\d{4}|\d{2}\.\d{2}\.\d{2}")
time_tokenizer = RegexpTokenizer(r"\d{1,2}:\d{2}")


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


@dataclass
class Attrs:
    """
    Метаданные, включая тип запроса
    """

    type_idx: int
    name: Union[str, None]
    date: Union[str, None]
    time: Union[str, None]


class Finder:
    """
    Класс для поиска ближайшего типа запроса и получения его атрибутов
    """

    def __init__(self, types: List[str]) -> None:
        """
        :param types: Список из названий запросов
        """

        self._type_embeds = get_embeds([clear_text(t) for t in types])

    def get_attrs(self, query: str) -> Attrs:
        """
        :param query: Запрос
        :return: Атрибуты и ближайший тип
        """

        query = clear_text(query)

        query_embed = get_embeds([query])
        type_idx = np.argmax(query_embed @ self._type_embeds.T, axis=1)[0]

        name = name_tokenizer.tokenize(query)
        name = name[0][1: -1].strip() if len(name) == 1 else None
        date = date_tokenizer.tokenize(query)
        date = date[0] if len(date) == 1 else None
        time = time_tokenizer.tokenize(query)
        time = time[0] if len(time) == 1 else None

        return Attrs(type_idx, name, date, time)
