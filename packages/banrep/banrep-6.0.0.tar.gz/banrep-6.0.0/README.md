# BanRep: Analítica de Texto

[banrep][pypi_banrep] es una librería en Python para analizar conjuntos de documentos textuales. Ofrece las funciones usadas recurrentemente en el [Banco de la República][web_banrep] para el preprocesamiento y análisis de texto.

[pypi_banrep]: https://pypi.org/project/banrep/
[web_banrep]: http://www.banrep.gov.co/

----

## 📖Cómo usar

Visite la [documentación][web_docs] para información detallada de uso.

[web_docs]: https://munozbravo.github.io/banrep/

|                       |                                  |
|----------------------------|----------------------------------|
| [Instalación][instalacion] | Cómo instalar en su equipo       |
| [Extracción][extraccion]     | Cómo usar para extracción de texto en documentos |
| [Uso general][general]  | Funcionalidad principal de la librería       |

[instalacion]: https://munozbravo.github.io/banrep/instalacion/
[extraccion]: https://munozbravo.github.io/banrep/uso_extraccion/
[general]: https://munozbravo.github.io/banrep/uso_general/

----

## Instalación

Se requiere tener instalado [Python 3.7][web_python].

Si es la primera vez que va a instalar este lenguaje de programación, se recomienda instalarlo usando [Anaconda3][web_anaconda] o [Miniconda3][web_conda]. Siga las instrucciones de instalación para su sistema.

[web_python]: https://www.python.org/downloads/
[web_anaconda]: https://www.anaconda.com/distribution/
[web_conda]: https://conda.io/miniconda.html

Se recomienda instalar en un entorno virtual para no interferir con otras instalaciones de python.

Tanto Anaconda como Miniconda instalan un programa llamado `conda`, para crear y activar un entorno virtual que instale `pip`.

Desde la *línea de comandos* ([Terminal][terminal] en macOS, [Anaconda Prompt][anacondocs] en windows):

[terminal]: https://support.apple.com/guide/terminal/welcome/mac
[anacondocs]: https://docs.anaconda.com/anaconda/install/verify-install/

```bash
# crear un entorno...
~$ conda create --name entorno python=3.7 pip jupyterlab
```

```bash
# confirmar que quiere descargar lo solicitado...
Proceed ([y]/n)? y
```

```bash
# activar el entorno creado...
~$ conda activate entorno
```

### pip

Una vez activado el entorno, instalar usando `pip`. Esto instalará automáticamente las librerías que [banrep][pypi_banrep] requiere.

```bash
~$ pip install --upgrade banrep
```

### Modelo de Lenguaje Natural

Se requiere un modelo pre-entrenado de [Spacy][spacy_models], que depende del idioma del texto que se quiera procesar.

[spacy_models]: https://spacy.io/models

Existen diversas formas de instalar, la más fácil es usando `download`.

```bash
~$ python -m spacy download es_core_news_md
```

Cuando se piensa usar el mismo modelo para diferentes proyectos, una alternativa es hacer una [instalación manual][spacy_manual]: descargar el [archivo del modelo][spacy_esmd], guardarlo en el directorio deseado, y crear un [vínculo simbólico][spacy_link] a dicho modelo.

[spacy_manual]: https://spacy.io/usage/models#download-manual
[spacy_esmd]: https://github.com/explosion/spacy-models/releases/download/es_core_news_md-2.2.5/es_core_news_md-2.2.5.tar.gz
[spacy_link]: https://spacy.io/usage/models#usage-link

### Verificar instalación
Puede verificar si [banrep][pypi_banrep] instaló correctamente usando `python` o `jupyter lab` desde la línea de comandos:

```bash
~$ python
>>> from banrep.linguistica import Documentos
>>>
```

Si no aparece ningún error quiere decir que la instalación fue exitosa.

----
