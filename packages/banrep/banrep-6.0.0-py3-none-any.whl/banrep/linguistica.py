# coding: utf-8
"""Módulo para procesar documentos lingüísticamente."""

from spacy.pipeline import EntityRuler
from spacy.tokens import Token


class Frases:
    """Anotaciones lingüísticas de cada frase en corpus.

    Parameters
    ----------
    lang : spacy.language.Language
        Modelo de lenguaje spaCy.
    datos : Iterable (str, dict)
        Información de cada documento (texto, metadata).
    tk : int, optional
        Filtro para número mínimo de tokens válidos en frases.
    filtros : dict, optional
        Filtros a evaluar en cada token.
        (is_alpha, lower_, pos_, dep_, ent_type_, chars)
    grupos : dict (str: set), optional
        Grupos de listas de palabras a identificar.
    entes : dict (str: set), optional
        Grupos de expresiones a considerar como Entities.

    Yields
    ------
    dict (text: str, tokens: list[dict], meta: dict)
        Anotaciones lingüísticas de cada frase.
    """

    def __init__(self, lang, datos, tk=0, filtros=None, grupos=None, entes=None):
        """Requiere: lang, datos.

        Opcional tk, filtros, grupos, entes.
        """
        self.lang = lang
        self.datos = datos
        self.tk = tk
        self.filtros = filtros
        self.grupos = grupos
        self.entes = entes

        self.exts_token = self.extensiones()

        self.fijar_extensiones()
        self.fijar_pipes()

        self.n = 0

    def __len__(self):
        return self.n

    def __repr__(self):
        return f"{self.__len__()} frases procesadas lingüísticamente."

    def __iter__(self):
        """Anotaciones lingüísticas de cada frase."""
        self.n = 0
        for doc, meta in self.lang.pipe(self.datos, as_tuples=True):
            for frase in self.detalles_doc(doc):
                self.n += 1
                frase["meta"] = meta.copy()
                frase["meta"].update({"id_sent": f"{self.n:0>7}"})

                yield frase

    def extensiones(self):
        """Crea lista de extensiones a usar."""
        exts = set()
        exts.add("ok_token")
        if self.grupos:
            for grupo in self.grupos:
                exts.add(grupo)

        return exts

    def crear_patrones(self):
        """Crea patrones para encontrar Entities."""
        patrones = [
            {"label": k, "pattern": v} for k in self.entes for v in self.entes.get(k)
        ]

        return patrones

    def fijar_extensiones(self):
        """Fija extensiones globalmente."""
        if not Token.has_extension("ok_token"):
            Token.set_extension("ok_token", default=True)

        if self.grupos:
            for grupo in self.grupos:
                if not Token.has_extension(grupo):
                    Token.set_extension(grupo, default=False)

    def fijar_pipes(self):
        """Fija componentes adicionales del Pipeline de procesamiento."""
        if not self.lang.has_pipe("cumplimiento"):
            self.lang.add_pipe(self.cumplimiento, name="cumplimiento", last=True)

        if self.grupos:
            if not self.lang.has_pipe("presencia"):
                self.lang.add_pipe(self.presencia, name="presencia", last=True)

        if self.entes:
            if not self.lang.has_pipe("entes"):
                ruler = EntityRuler(self.lang, phrase_matcher_attr="LOWER")
                ruler.add_patterns(self.crear_patrones())

                self.lang.add_pipe(ruler, name="entes", before="ner")

    def token_cumple(self, token):
        """Determina si token pasa los filtros.

        Parameters
        ----------
        token : spacy.tokens.Token
            Token a evaluar.

        Returns
        -------
        bool
            Si token pasa los filtros o no.
        """
        if not self.filtros:
            return True

        if self.filtros.get("is_alpha"):
            if not token.is_alpha:
                return False

        attr = ["lower_", "pos_", "dep_", "ent_type_"]
        ok = [getattr(token, a) not in self.filtros.get(a, list()) for a in attr]
        if not all(ok):
            return False

        chars = self.filtros.get("chars", 0)
        if chars:
            return len(token) > chars

        return True

    def cumplimiento(self, doc):
        """Cambia valores durante componente cumplimiento si falla filtros.

        Parameters
        ----------
        doc : spacy.tokens.Doc

        Returns
        -------
        doc : spacy.tokens.Doc
        """
        for token in doc:
            if not self.token_cumple(token):
                token._.set("ok_token", False)

        return doc

    def presencia(self, doc):
        """Cambia valores durante componente presencia si en grupos.

        Parameters
        ----------
        doc : spacy.tokens.Doc

        Returns
        -------
        spacy.tokens.Doc
        """
        for grupo in self.grupos:
            palabras = self.grupos.get(grupo)
            for token in doc:
                if token.lower_ in palabras:
                    token._.set(grupo, True)

        return doc

    def token_features(self, token):
        """Extrae anotaciones lingüísticas de un token.

        Parameters
        ----------
        token : spacy.tokens.Token
            Token a evaluar.

        Returns
        -------
        dict (str, str | bool)
            Anotaciones lingüísticas del token.
        """
        attributes = [
            "text",
            "i",
            "ent_type_",
            "ent_iob_",
            "lower_",
            "is_alpha",
            "is_oov",
            "pos_",
            "dep_",
        ]

        anotaciones = {a: getattr(token, a) for a in attributes}
        anotaciones["chars"] = len(token)

        for ext in self.exts_token:
            anotaciones[ext] = token._.get(ext)

        return anotaciones

    def detalles_doc(self, doc):
        """Obtiene detalles lingüísticos de documento.

        Parameters
        ----------
        doc : spacy.tokens.Doc

        Yields
        ------
        dict (text: str, tokens: list)
            Anotaciones lingüísticas de cada frase.
        """
        for sent in doc.sents:
            tokens = [self.token_features(t) for t in sent if t._.get("ok_token")]
            if len(tokens) > self.tk:
                frase = {}
                frase["text"] = sent.text
                frase["tokens"] = tokens

                yield frase
