# coding: utf-8
"""Módulo para tabulaciones de lingüística y transformación de texto."""

import pandas as pd


def df_tokens(frases, ng=False):
    """DataFrame de tokens en frases.

    Parameters
    ----------
    frases : Iterable[dict (text: str, tokens: list[dict | str], meta: dict)]
        Anotaciones lingüísticas o Info de cada frase.
    ng : Bool
        Si frases contienen n-gramas.

    Returns
    -------
    pd.DataFrame
        Anotaciones lingüísticas o Info de cada token.
    """
    dfs = []
    for frase in frases:
        if ng:
            df = pd.DataFrame({"token": frase.get("tokens")})
        else:
            df = pd.DataFrame(frase.get("tokens"))

        for k, v in frase.get("meta").items():
            df[k] = v

        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


def df_frases(frases):
    """DataFrame de frases.

    Parameters
    ----------
    frases : Iterable[dict (text: str, tokens: list[dict | str], meta: dict)]
        Anotaciones lingüísticas de cada frase.

    Returns
    -------
    pd.DataFrame
        Texto y Metadata de cada frase.
    """
    df = pd.DataFrame(frase.get("meta") for frase in frases)
    df["text"] = [frase.get("text") for frase in frases]

    return df


def df_probables(modelo, n=15):
    """Distribución de probabilidad de tokens en tópicos de modelo.

    Parameters
    ----------
    modelo : gensim.models.ldamodel.LdaModel
    n : int optional
        Cuantos tokens incluir.

    Returns
    -------
    pd.DataFrame
        Tokens probables de cada tópico y sus probabilidades.
    """
    dfs = []
    for topico in range(modelo.num_topics):
        data = modelo.show_topic(topico, n)
        df = pd.DataFrame(data=data, columns=["token", "probabilidad"])
        df["topico"] = topico
        dfs.append(df)

    df_topicos = pd.concat(dfs, ignore_index=True)

    return df_topicos.sort_values(
        by=["topico", "probabilidad"], ascending=[True, False]
    )
