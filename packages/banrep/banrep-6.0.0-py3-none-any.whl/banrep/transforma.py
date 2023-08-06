# coding: utf-8
"""Módulo para crear modelos de transformación de texto."""
from collections import defaultdict
from itertools import groupby
import warnings

from gensim.corpora import Dictionary
from gensim.models import CoherenceModel
from gensim.models import Phrases
from gensim.models.ldamodel import LdaModel
from gensim.models.phrases import Phraser


class NgramFrases:
    """Info de frases incluyendo n-gramas.

    Parameters
    ----------
    frases : Iterable[dict (text: str, tokens: list[dict], meta: dict)]
        Anotaciones lingüísticas de cada frase.
    attr : str
        Atributo a usar como texto de cada token (text | lower_)
    th : float
        Score Threshold para formar n-gramas.
        Ver https://radimrehurek.com/gensim/models/phrases.html

    Yields
    ------
    dict (text: str, tokens: list[str], meta: dict)
        Info de cada frase incluyendo n-gramas.
    """

    def __init__(self, frases, attr="lower_", th=10.0):
        """Requiere: frases.

        Opcional attr, th.
        """
        self.frases = frases
        self.attr = attr
        self.th = th

        self.models = self.crear_modelos()

    def __iter__(self):
        """Info de cada frase incluyendo n-gramas."""
        big = self.models.get("bigrams")
        trig = self.models.get("trigrams")

        for frase in self.frases:
            info = frase.copy()
            tokens = [t.get(self.attr) for t in frase.get("tokens")]
            info["tokens"] = trig[big[tokens]]

            yield info

    def solo_tokens(self):
        """Extrae tokens de cada frase.

        Yields
        ------
        list[str]
            Tokens de cada frase.
        """
        for frase in self.frases:
            yield [t.get(self.attr) for t in frase.get("tokens")]

    def crear_modelos(self):
        """Crea modelos de n-gramas.

        Returns
        -------
        dict
            Modelos Phraser para bigramas y trigramas.
        """
        g = (tokens for tokens in self.solo_tokens())
        big = Phrases(g, threshold=self.th)
        bigrams = Phraser(big)

        g = (tokens for tokens in self.solo_tokens())
        trig = Phrases(bigrams[g], threshold=self.th)
        trigrams = Phraser(trig)

        return dict(bigrams=bigrams, trigrams=trigrams)


class Bags:
    """Documentos como Bag Of Words.

    Parameters
    ----------
    frases : Iterable[dict (text: str, tokens: list, meta: dict)]
        Anotaciones lingüísticas o Info de cada frase.
    idm : str
        Llave de Metadata para agrupar.
    attr : str | None
        Atributo a usar de token (text | lower_). None si ngramas.
    vocab : gensim.corpora.Dictionary, optional
        Vocabulario a considerar.

    Yields
    ------
    dict (idm: str, tokens: list[str], sparsed: list[tuple(int, int)])
        Bags of Words de cada documento.
    """

    def __init__(self, frases, idm, attr=None, vocab=None):
        """Requiere frases, idm.

        Opcional: attr, vocab.
        """
        self.frases = frases
        self.idm = idm
        self.attr = attr
        self.vocab = vocab

        self.n = 0

        if not self.vocab:
            self.vocab = self.crear_vocab()
            print(f"Diccionario con {len(self.vocab)} términos creado...")

    def __len__(self):
        return self.n

    def __repr__(self):
        return f"{self.__len__()} documentos y {len(self.vocab)} términos."

    def __iter__(self):
        """Bags Of Words de cada documento."""
        self.n = 0
        for k, g in groupby(self.frases, lambda x: x.get("meta").get(self.idm)):
            dtoks = []
            for frase in g:
                if self.attr:
                    tokens = [t.get(self.attr) for t in frase.get("tokens")]
                else:
                    tokens = frase.get("tokens")

                dtoks.extend(tokens)

            self.n += 1
            yield dict(idm=k, tokens=dtoks, sparsed=self.vocab.doc2bow(dtoks))

    def crear_vocab(self):
        """Crea diccionario de términos presentes."""
        if self.attr:
            return Dictionary(
                [t.get(self.attr) for t in frase.get("tokens")] for frase in self.frases
            )
        else:
            return Dictionary(frase.get("tokens") for frase in self.frases)


class Topicos:
    """Modelos de tópicos basados en LDA.

    Parameters
    ----------
    bags : banrep.transforma.Bags
        Bags of Words de documentos.
    kas : Iterable[int]
        Diferentes k tópicos para los cuales crear modelo.
    params : dict
        Parámetros requeridos en modelos LDA.
        Ver https://radimrehurek.com/gensim/models/ldamodel.html

    Yields
    ------
    dict (k:int, modelo: gensim.models.ldamodel.LdaModel, score: float)
        Modelo de Tópicos para cada k.
    """

    def __init__(self, bags, kas, params):
        """Requiere bags, kas, params."""
        self.bags = bags
        self.kas = kas
        self.params = params

        self.best = 0
        self.score = 0

    def __repr__(self):
        fmstr = f"Mejor k={self.best} con Coherence Score={self.score:.3f}"
        return f"Modelos LDA para k en {self.kas}: {fmstr}"

    def __iter__(self):
        """Modelo LDA para cada k."""
        for k in self.kas:
            modelo = self.crear_modelo(k, [b.get("sparsed") for b in self.bags])
            score = self.evaluar(modelo, [b.get("tokens") for b in self.bags])

            if score > self.score:
                self.score = score
                self.best = k

            yield dict(k=k, modelo=modelo, score=score)

    def crear_modelo(self, k, sparsed):
        """Crea modelo LDA de k tópicos.

        Parameters
        ----------
        k : int
            Número de tópicos a usar en modelo.
        sparsed : Iterable[list(tuple(int, int))]
            Bag of Words con id, freq de tokens.

        Returns
        -------
        gensim.models.ldamodel.LdaModel
            Modelo LDA de k tópicos.
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            modelo = LdaModel(
                sparsed, num_topics=k, id2word=self.bags.vocab, **self.params
            )

        return modelo

    def evaluar(self, modelo, textos):
        """Calcula Coherence Score de modelo de tópicos.

        Parameters
        ----------
        modelo : gensim.models.ldamodel.LdaModel
        textos : Iterable (list[str])
            Palabras de cada documento en un corpus.

        Returns
        -------
        float
            Coherencia calculada.
        """
        cm = CoherenceModel(
            model=modelo, texts=textos, dictionary=self.bags.vocab, coherence="c_v",
        )

        return cm.get_coherence()
