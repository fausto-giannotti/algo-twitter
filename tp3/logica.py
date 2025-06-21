import sys

from manejo_cadenas import normalizar, tokenizar
from manejo_db import persistir_tweet, eliminar_de_db, almacenar_tweet

INPUT_INVALIDO = "Input invalido."
TOKENIZACION_INVALIDA = "El argumento de cantidad de tokens es inválido."

LEN_DEFAULT_TOKENIZACION = 3


# -----------------------------------------------------------------------------


def crear_tweet(id, tweet, tweets, tweets_normalizados_tokenizados, len_tokenizacion):
    """
    El usuario ingresa un tweet que se almacena con su respectivo id;
    id se recibe como parametro para poder tener en cuenta valor
    pervio del id y devolver id+1 (solo si efectivamente se guarda el
    token) caso contrario (o sea input == **) devuelve el mismo id.
    """

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


# -----------------------------------------------------------------------------


def buscar_tweet(
    texto_a_buscar, tweets, tweets_normalizados_tokenizados, len_tokenizacion
):
    """
    Pide input al usuario, lo normaliza y lo tokeniza. Si la busqueda se
    puede hacer (es decir, el input es valido) imprime tweets originales
    que coiciden o NO_ENCONTRADOS si no hay coicidencias. Devuelve
    lista de ids que coiciden con la busqueda.
    """
    busqueda_normalizada = normalizar(texto_a_buscar)

    ids_comunes = obtener_ids_tweets_coincidentes(
        busqueda_normalizada, tweets_normalizados_tokenizados, len_tokenizacion
    )
    return ids_comunes


def obtener_ids_tweets_coincidentes(
    busqueda_normalizada, tweets_normalizados_tokenizados, len_tokenizacion
):
    """Recibe la busqueda normalizada y la tokeniza. Para cada token de la busqueda
    almacena (si los hay) en una sublista los ids que coinciden. Finalmente, compara
    las sublistas y devuelve una lista donde solo estan los ids que coiciden con todos
    los tokens"""
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


# -----------------------------------------------------------------------------


def eliminar_tweets(
    ids_eliminables, tweets, tweets_normalizados_tokenizados, len_tokenizacion
):
    """
    Llama a buscar_tweet() y almacena lista de ids coincidentes con la busqueda.
    Pide ids a eliminar y verifica que estos sean validos (es decir, que el
    input sea valido y que los ids ingresados coicidan con el resultado
    de la busqueda) No devuelve nada, solo modifica los diccionarios.
    """
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
    """
    Crea un set para evitar repetir eliminaciones, y llama a
    borrar_id_asociado_a_token() (quien efectivamente borra
    ids y tokens)
    """
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
    """
    Normaliza y tokeniza tweet que coincide con id a eliminar; para cada
    token resultante, si este se encuentra en diccionario,
    elimina el id de los valores, si eso hace que token quede vacio
    (o sea no le queda ningun id asociado) tambien elimina el token
    """

    tweet_normalizado = normalizar(tweet)

    for token in tokenizar(tweet_normalizado, len_tokenizacion):
        if token in tweets_normalizados_tokenizados:

            if id in tweets_normalizados_tokenizados[token]:
                tweets_normalizados_tokenizados[token].remove(id)

            # si una vez que el id (el valor) se borro, el token (la clave)
            # queda vacio, borrar tambien el token
            if not tweets_normalizados_tokenizados[token]:
                del tweets_normalizados_tokenizados[token]


# -----------------------------------------------------------------------------


def importar_tweets(
    id, archivos_validos, tweets, tweets_normalizados_tokenizados, len_tokenizacion
):
    """Pide al usuario que ingrese las rutas de donde importar. Las valida y lee linea
    por linea cada tweet mientras los va almacenado en los dicts y guardando en la db.
    Devuelve el utlimo id almacenado + 1"""

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


# -----------------------------------------------------------------------------


def exportar_tweets(tweets, ruta):
    """Pide la ruta de una archivo. Si la ruta esta en un dir, verifica que el
    dir existe. Crea o sobrescribe el archivo dado por la ruta con los tweets
    almacenados en memoria (el dict 'tweets')"""

    num_tweets_exportados = exportar_tweets_a_archivo(ruta, tweets)

    return num_tweets_exportados


def exportar_tweets_a_archivo(ruta, tweets):
    num_tweets_exportados = 0
    with open(ruta, "w", encoding="utf-8") as archivo:
        for tweet in tweets.values():
            tweet = tweet.rstrip()
            archivo.write(f"{tweet}\n")
            num_tweets_exportados += 1

    return num_tweets_exportados


# -----------------------------------------------------------------------------


def validar_argumentos(args):
    """
    Si se ingresan argumentos por consola los recibe por args, sino,
    recibe args = None. Si args = None o solo se recibe 1 argumento
    (i.e. args = ["nombre_archivo"]), devuelve LEN_DEFAULT_TOKENIZACION.

    Si efectivamente se reciben mas argumentos, verifica que sea solo un
    entero positivo. Si lo es, se devuelve como int (que en main() se
    almacena como len_tokenizacion). Si no, se ejecuta sys.exit(1)).
    """

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
