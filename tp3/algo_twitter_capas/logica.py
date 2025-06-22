import sys

from manejo_cadenas import normalizar, tokenizar
from manejo_db import persistir_tweet, eliminar_de_db, almacenar_tweet

INPUT_INVALIDO = "Input invalido."
TOKENIZACION_INVALIDA = "El argumento de cantidad de tokens es inválido."

LEN_DEFAULT_TOKENIZACION = 3


# ------------------------------logica-crear-------------------------------


def crear_tweet(id, tweet, tweets, tweets_normalizados_tokenizados, len_tokenizacion):
    """Dado un tweet valido, lo normaliza y tokeniza para persistirlo y
    almacenarlo. Devuelve el proximo id."""

    tweet_normalizado = normalizar(tweet)

    tweet_tokenizado = tokenizar(tweet_normalizado, len_tokenizacion)

    persistir_tweet(id, tweet)

    almacenar_tweet(
        id,
        tweet,
        tweets,
        tweets_normalizados_tokenizados,
        tweet_tokenizado,
    )

    return id + 1


# ------------------------------logica-buscar-------------------------------


def buscar_tweet(
    texto_a_buscar, tweets, tweets_normalizados_tokenizados, len_tokenizacion
):
    """Dado un texto a buscar, lo normaliza y llama a
    obtener_ids_tweets_coincidentes() que devuelve
    una lista de ids que coiciden. Devuelve esto ultimo."""

    busqueda_normalizada = normalizar(texto_a_buscar)

    ids_comunes = obtener_ids_tweets_coincidentes(
        busqueda_normalizada, tweets_normalizados_tokenizados, len_tokenizacion
    )
    return ids_comunes


def obtener_ids_tweets_coincidentes(
    busqueda_normalizada, tweets_normalizados_tokenizados, len_tokenizacion
):
    """Recibe la busqueda normalizada y la tokeniza. Para cada token
    de la busqueda almacena (si los hay) en una sublista los ids que coinciden.
    Finalmente, compara las sublistas y devuelve una lista donde solo estan
    los ids que coiciden con todos los tokens"""

    busqueda_tokenizada = tokenizar(busqueda_normalizada, len_tokenizacion)

    listas_de_ids = []

    for token in busqueda_tokenizada:
        ids = tweets_normalizados_tokenizados.get(token)
        if ids is None:
            return []
        listas_de_ids.append(ids)

    ids_comunes = set(listas_de_ids[0])

    for lista in listas_de_ids[1:]:
        ids_comunes = ids_comunes & set(lista)

    return list(ids_comunes)


# ------------------------------logica-eliminar-------------------------------


def eliminar_tweets(
    ids_eliminables, tweets, tweets_normalizados_tokenizados, len_tokenizacion
):
    """Dada una lista de ids los elimina y devuelve una lista de los
    tweets eliminados."""

    tweets_eliminados = []

    ids_eliminados = eliminar_ids_de_tweets(
        ids_eliminables, tweets, tweets_normalizados_tokenizados, len_tokenizacion
    )

    for id_eliminado in ids_eliminados:
        tweets_eliminados.append(f"{id_eliminado}. {tweets[id_eliminado]}")
        del tweets[id_eliminado]

    return tweets_eliminados


def eliminar_ids_de_tweets(
    lista_de_ids, tweets, tweets_normalizados_tokenizados, len_tokenizacion
):
    """Crea un set para evitar repetir eliminaciones, y llama a
    borrar_id_asociado_a_token() (quien efectivamente borra
    ids y tokens)"""
    eliminados = set()

    for id in lista_de_ids:
        if id in eliminados:
            continue

        eliminados.add(id)

        tweet = tweets[id]

        eliminar_de_db(id)

        # borra todos los ids del tweet asociados a tokens y si el unico id
        # asociado era el eliminado, tambien elimina token
        borrar_id_asociado_a_token(
            id, tweet, tweets_normalizados_tokenizados, len_tokenizacion
        )

    list(eliminados)
    return eliminados


def borrar_id_asociado_a_token(
    id, tweet, tweets_normalizados_tokenizados, len_tokenizacion
):
    """Normaliza y tokeniza tweet que coincide con id a eliminar;
    para cada token resultante, si este se encuentra en diccionario,
    elimina el id de los valores, si eso hace que token quede vacio
    (o sea no le queda ningun id asociado) tambien elimina el token"""

    tweet_normalizado = normalizar(tweet)

    for token in tokenizar(tweet_normalizado, len_tokenizacion):
        if token in tweets_normalizados_tokenizados:

            if id in tweets_normalizados_tokenizados[token]:
                tweets_normalizados_tokenizados[token].remove(id)

            # si una vez que el id (el valor) se borro, el token (la clave)
            # queda vacio, borrar tambien el token
            if not tweets_normalizados_tokenizados[token]:
                del tweets_normalizados_tokenizados[token]


# ------------------------------logica-importar-------------------------------


def importar_tweets(
    id, archivos_validos, tweets, tweets_normalizados_tokenizados, len_tokenizacion
):

    id = recorrer_archivos_tweets_importar(
        archivos_validos,
        len_tokenizacion,
        id,
        tweets,
        tweets_normalizados_tokenizados,
    )

    return id


def recorrer_archivos_tweets_importar(
    archivos_validos, len_tokenizacion, id, tweets, tweets_normalizados_tokenizados
):
    """Dada una lista de archivos validos, importa los tweets de cada uno."""

    for archivo in archivos_validos:
        id = almacenar_y_persitir_tweets_importados(
            archivo, len_tokenizacion, id, tweets, tweets_normalizados_tokenizados
        )

    return id


def almacenar_y_persitir_tweets_importados(
    archivo, len_tokenizacion, id, tweets, tweets_normalizados_tokenizados
):
    with open(archivo, "r", encoding="utf8") as archivo_tweets:
        for tweet in archivo_tweets:
            tweet_normalizado = normalizar(tweet.rstrip())
            if tweet_normalizado == "":
                continue
            tweet_tokenizado = tokenizar(tweet_normalizado, len_tokenizacion)

            almacenar_tweet(
                id,
                tweet,
                tweets,
                tweets_normalizados_tokenizados,
                tweet_tokenizado,
            )
            persistir_tweet(id, tweet)
            id += 1

    return id


# ------------------------------logica-exportar-------------------------------


def exportar_tweets(ruta, tweets):
    """Almacena todos los tweets en memoria a una ruta dada.
    Devuelve el total de tweets exportados."""
    num_tweets_exportados = 0
    with open(ruta, "w", encoding="utf-8") as archivo:
        for tweet in tweets.values():
            tweet = tweet.rstrip()
            archivo.write(f"{tweet}\n")
            num_tweets_exportados += 1

    return num_tweets_exportados


# ----------------------------logica-validar-args-----------------------------


def validar_argumentos(args):
    """Si se ingresan argumentos por consola los recibe por args, sino,
    recibe args = None. Si args = None o solo se recibe 1 argumento
    (i.e. args = ["nombre_archivo"]), devuelve LEN_DEFAULT_TOKENIZACION.

    Si efectivamente se reciben mas argumentos, verifica que sea solo un
    entero positivo. Si lo es, se devuelve como int (que en main() se
    almacena como len_tokenizacion). Si no, se ejecuta sys.exit(1))."""

    if args is None or len(args) < 2:
        return LEN_DEFAULT_TOKENIZACION

    if len(args) != 2 or not args[1].isdigit():
        print(TOKENIZACION_INVALIDA)
        sys.exit(1)

    valor = int(args[1])

    if valor <= 0:
        print(TOKENIZACION_INVALIDA)
        sys.exit(1)

    return valor
