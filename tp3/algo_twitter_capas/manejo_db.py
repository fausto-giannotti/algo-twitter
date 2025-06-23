import os
import sys

from manejo_cadenas import normalizar, tokenizar

DB_PATH = "db"
DB_INVALIDA = "Error al intentar abrir el programa."


def validar_db():
    """Verifica que DB_PATH sea un dir valido. Lo mismo con cada uno de los
    archivos dentro del dir. Si hay algun error => sys.exit(1)"""

    try:
        for archivo in os.listdir(DB_PATH):

            if not archivo.endswith(".txt"):
                raise IOError

            ruta = os.path.join(DB_PATH, archivo)

            with open(ruta, "r", encoding="utf8"):
                pass

    except (IOError, OSError, UnicodeDecodeError):
        print(DB_INVALIDA)
        sys.exit(1)


def inicializar_db(tweets, tweets_normalizados_tokenizados, len_tokenizacion):
    """Llama a validar_db() para verificar que sea valida. Si hay tweets en la
    db los almacena en los dicts que recibe por parametros. Los archivos vacios
    (i.e. de tweets borrados) son ingorados. Devuelve el ultimo id de la
    db + 1 si hay tweets, caso contrario devuelve id = 0."""

    id_max = 0

    validar_db()

    lista_archivos = os.listdir(DB_PATH)

    if len(lista_archivos) == 0:
        return id_max

    for archivo in lista_archivos:

        id = int(archivo.split(".")[0])
        ruta = os.path.join(DB_PATH, archivo)

        if id_max < id:
            id_max = id

        with open(ruta, "r", encoding="utf8") as archivo:

            tweet_a_almacenar = archivo.readline()
            tweet_normalizado = normalizar(tweet_a_almacenar)

            if not tweet_a_almacenar:
                continue

            tweet_tokenizado = tokenizar(tweet_normalizado, len_tokenizacion)

            almacenar_tweet(
                id,
                tweet_a_almacenar,
                tweets,
                tweets_normalizados_tokenizados,
                tweet_tokenizado,
            )

    return id_max + 1  # devuleve ultimo id + 1


def persistir_tweet(id, tweet):
    """Recibe un id y un tweet validos y los almacena en un archivo en db
    con nombre 'id.txt' y contenido el tweet"""

    validar_db()

    archivo = f"{id}.txt"
    ruta = os.path.join(DB_PATH, archivo)

    with open(ruta, "w", encoding="utf8") as arc:
        arc.write(tweet)


def eliminar_de_db(id):
    """Es llamado por eliminar_tweets() para vaciar el archivo de la
    db donde se encuentra el tweet a eliminar."""

    validar_db()

    archivo = f"{id}.txt"
    ruta = os.path.join(DB_PATH, archivo)

    with open(ruta, "w", encoding="utf8"):
        pass


def almacenar_tweet(
    id,
    tweet_a_almacenar,
    tweets,
    tweets_normalizados_tokenizados,
    tweet_tokenizado,
):
    """Recibe las 2 versiones del tweet (normalizado-tokenizado por
    un lado, y sin modificar por el otro) con su respectivo id y los dos dicts.
    Los almacena en ambos."""

    tweets[id] = tweet_a_almacenar

    for token in tweet_tokenizado:

        # si token ya fue almacenado antes, sumarle un nuevo id
        if token in tweets_normalizados_tokenizados:
            tweets_normalizados_tokenizados[token].append(id)

        # si token nunca fue almacenado antes,
        # guardarlo como clave con su respectivo id
        else:
            tweets_normalizados_tokenizados[token] = [id]
