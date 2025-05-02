# aca voy a hacer todo el desarollo

NUMERO_INVALIDO = "Numero de tweet invalido."
NO_ENCONTRADOS = "No se encontraron tweets."
INPUT_INVALIDO = "Input invalido."
FIN = "Finalizando..."
RESULTADOS_BUSQUEDA = "Resultados de la busqueda:"
TWEETS_ELIMINADOS = "Tweets eliminados:"
ATRAS = "**"

# errores validacion 1-10, 15-44, 46-52, 54, 55, 57-67
# resolver lo de poder eliminar con comas (o sea que 1, 2, 3, 7-10) funcione --> LISTO :)


def main():

    id = 0
    tweets = {}
    tweets_normalizados_tokenizado = {}

    while True:

        # se ejecutará hasta que el usuario ingrese 4
        user_input = input(
            "1. Crear Tweet\n"
            "2. Buscar Tweet\n"
            "3. Eliminar Tweet\n"
            "4. Salir\n"
            ">>> "
        )

        # cada funcion recibe parametros de los dicts/variables necesarias para ejecutarse

        if user_input == "1":

            # dado que crear tweet devuelve id+1 (si efectivamente se guarda el token)
            # id = crear_tweet actualiza id con nuevo valor (y si input == **)
            # devuelve el mismo id
            id = crear_tweet(id, tweets, tweets_normalizados_tokenizado)

        elif user_input == "2":
            buscar_tweet(tweets, tweets_normalizados_tokenizado)

        elif user_input == "3":
            # lista_de_ids_validos = validar_ids_eliminar(
            #    tweets, tweets_normalizados_tokenizado
            # )

            # if lista_de_ids_validos is None:
            #    continue

            eliminar_tweets(tweets, tweets_normalizados_tokenizado)

        elif user_input == "4":
            print(FIN)
            break
        else:
            print(INPUT_INVALIDO)


# -----------------------------------------------------------------------------

# todos los tweets se almacenan en un dict
# cada tweet tiene un calve (id) y un valor (el tweet en si)
# --> son de la forma {id:tweet}


"""
Crear tweet: el usuario ingresa un tweet que se almacena con su respectivo
id (que es unico e irrepetible)

Id se recibe como parametro por crear_tweet para poder tener en cuenta valor
pervio del id; de forma similar los dicts son recibidos por crear_tweet para
poder trabajar con ellos

Output esperado: OK id_tweet

Si tweet almacenado (i.e. normalizado) == vacío, entonces input invalido

Se utilizaran 2 diccionarios, uno con el tweet tal cual y otro con el tweet
normalizado y tokenizado donde cada token es una clave y sus valores son los
ids de los tweets que coinciden
"""


def crear_tweet(id, tweets, tweets_normalizados_tokenizado):

    while True:

        tweet_a_almacenar = input("Ingrese el tweet a almacenar: ")

        if tweet_a_almacenar == ATRAS:
            return id

        tweet_normalizado = normalizar(tweet_a_almacenar)

        if tweet_normalizado == "":
            print(INPUT_INVALIDO)
            continue

        # dado que tweet es valido, es almacenado en ambos dicts:

        tweets[id] = tweet_a_almacenar

        for token in tokenizar(tweet_normalizado):

            # si token ya fue almacenado antes, sumarle un nuevo id
            if token in tweets_normalizados_tokenizado:
                tweets_normalizados_tokenizado[token].append(id)

            # si token nunca fue almacenado antes,
            # guardarlo como clave con su respectivo id
            else:
                tweets_normalizados_tokenizado[token] = [id]

        print(f"OK {id}")

        id += 1
        return id


def normalizar(tweet):

    acentos_y_enie = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ñ": "n",
        "ü": "u",
    }
    # convierte al str en minus. y lo separa en una lista
    lista_caracteres = list(tweet.lower())

    # se realizan las comparaciones por cada elemento en la lista
    for posicion in range(len(lista_caracteres)):

        # si caracter =! num o letra o espacio, elimina dicho caracter
        if not (
            lista_caracteres[posicion].isalnum() or lista_caracteres[posicion] == " "
        ):
            lista_caracteres[posicion] = ""

        # reemplaza cada caracter que coincida con una
        # clave del dict con su valor
        lista_caracteres[posicion] = acentos_y_enie.get(
            lista_caracteres[posicion], lista_caracteres[posicion]
        )

        # si hay 2 espacios vacios elimina uno; lo hace desde la posicion 1
        if (
            posicion > 0
            and lista_caracteres[posicion] == " "
            and lista_caracteres[posicion - 1] == " "
        ):
            lista_caracteres[posicion] = ""

        # si el primer o ultimo caracter es un espacio, lo elimina
        if lista_caracteres[0] == " ":
            lista_caracteres[0] = ""

        if lista_caracteres[-1] == " ":
            lista_caracteres[-1] = ""

    # convierte la lista a una cadena nuevamente
    tweet_normalizado = "".join(lista_caracteres)

    # si solo tiene espacios devolver cadena vacia
    if tweet_normalizado.strip() == "":
        return ""

    return tweet_normalizado


# para tokenizar con n = 3, se tiene que ir almacenando por segmentos
# o sea desde pos a pos+3, desde pos a pos+4 y asi sucesivamente
# cuando se llega al final de las combinaciones para pos,
# se hace lo mismo para pos+1
# por ej: "buenas" --> "bue", "buen", "buena", "buenas", "uen",
# "uena", "uenas", "ena", "enas", "nas"
# si alguna combinacion ya esta almacenada, no almacenar de vuelta
# si len(palabra) <= 3 se almacena directamente la palabra

# para cada fin posible, desde inicio + 3 (min 3 caracteres)
# hasta el final de la palabra:
# ej: si inicio = 0 y len(palabra) = 4 ("hola"):
# el rango sería range(3, 4+1) = [3, 4, 5] = 3 iteraciones
#     inicio = 0, fin = 3 => palabra[0:3] = "hol"
#     inicio = 0, fin = 4 => palabra[0:4] = "hola"
# desp inicio = 1:
#     inicio = 1, fin = 4 => palabra[1:4] = "ola"
#     inicio = 1, fin = 5 => palabra[1:5] = "ola"
# --> si ya esta almacenado no lo almacena de vuelta
# y así con todas las palabras


def tokenizar(tweet_normalizado):

    tweet_tokenizado = []

    lista_de_palabras = tweet_normalizado.split(" ")

    for palabra in lista_de_palabras:

        # si longitud palabra menor igual que 3, se almacena directo
        if len(palabra) < 3:
            if palabra not in tweet_tokenizado:
                tweet_tokenizado.append(palabra)
            continue

        # para cada elemnto de la palabra:
        for inicio in range(len(palabra)):

            for fin in range(inicio + 3, len(palabra) + 1):
                segmento = palabra[inicio:fin]

                # para cada caracter, ir desde su pos a pos+3, +4, +n hasta
                # llegar al final de la palabra; desp arranca desde pos+3+1
                # y repite hasta almecenar cada combinacion

                # no volver a almacenar segmentos ya almacenados
                if segmento not in tweet_tokenizado:
                    tweet_tokenizado.append(segmento)

        if palabra not in tweet_tokenizado:
            tweet_tokenizado.append(palabra)

    return tweet_tokenizado


"""
Buscar tweet: el usuario ingresa texto a buscar
(si el texto es valido) es normalizado y tokenizado
el texto se compara con los tokens almacenados como claves en el dict
en caso de coincidir, se acceden a sus valores (que son los ids)
se imprimen los tweets originales en base a los ids con lo que se coincidio
(que pueden ser uno o varios)
devuelve lista de ids que coinciden
"""


def buscar_tweet(tweets, tweets_normalizados_tokenizado):
    while True:
        texto_a_buscar = input("Ingrese la/s palabra/s clave a buscar:\n>>> ")

        if texto_a_buscar == ATRAS:
            return None

        ids_comunes = obtener_ids_tweets_coincidentes(
            texto_a_buscar, tweets_normalizados_tokenizado
        )

        if ids_comunes is None:
            print(INPUT_INVALIDO)
            continue

        if not ids_comunes:
            print(NO_ENCONTRADOS)
            return []

        print(RESULTADOS_BUSQUEDA)
        for id in sorted(ids_comunes):
            print(f"{id}. {tweets[id]}")

        return ids_comunes


def obtener_ids_tweets_coincidentes(texto_a_buscar, tweets_normalizados_tokenizado):
    busqueda_normalizada = normalizar(texto_a_buscar)
    if busqueda_normalizada == "":
        return None

    busqueda_tokenizada = tokenizar(busqueda_normalizada)
    listas_de_ids = []

    for token in busqueda_tokenizada:
        if token not in tweets_normalizados_tokenizado:
            return []

        listas_de_ids.append(tweets_normalizados_tokenizado[token])

    if not listas_de_ids:
        return []

    ids_comunes = listas_de_ids[0]
    for lista in listas_de_ids[1:]:
        nueva_ids_comunes = []
        for id in ids_comunes:
            if id in lista:
                nueva_ids_comunes.append(id)
        ids_comunes = nueva_ids_comunes

    return ids_comunes


"""

"""


def eliminar_tweets(tweets, tweets_normalizados_tokenizado):
    while True:
        ids_coincidentes = buscar_tweet(tweets, tweets_normalizados_tokenizado)
        if ids_coincidentes is None or not ids_coincidentes:
            return None

        while True:
            ids_a_eliminar = input(
                "Ingrese los numeros de tweets a eliminar:\n>>> "
            ).split(",")

            if ids_a_eliminar[0] == ATRAS:
                return None

            lista_de_ids = listar_ids(ids_a_eliminar)

            if not validar_ids_seleccionados(lista_de_ids, ids_coincidentes):
                continue

            lista_de_ids.sort()

            print(TWEETS_ELIMINADOS)
            eliminar_ids_de_tweets(lista_de_ids, tweets, tweets_normalizados_tokenizado)
            return None


# def borrar_tweet_asociado_a_id(id, tweet, tweets):
#    del tweets[id]


def borrar_id_asociado_a_token(id, tweet, tweets_normalizados_tokenizado):
    tweet_normalizado = normalizar(tweet)

    for token in tokenizar(tweet_normalizado):
        # si token coincide con alguna calve del dict:
        if token in tweets_normalizados_tokenizado:
            # entonces se elimina el id de los tokens asociados
            if id in tweets_normalizados_tokenizado[token]:
                tweets_normalizados_tokenizado[token].remove(id)

            # si desp no queda asociado ningun id con ese token
            # directamenete se elimina ese token
            if not tweets_normalizados_tokenizado[token]:
                del tweets_normalizados_tokenizado[token]


def listar_ids(ids_a_eliminar):
    lista_ids = []
    error = None

    for numero_o_rango in ids_a_eliminar:
        numero_o_rango = numero_o_rango.strip()
        if not numero_o_rango:
            error = INPUT_INVALIDO
            break

        if numero_o_rango.isdigit():
            lista_ids.append(int(numero_o_rango))
            continue

        if "-" in numero_o_rango:
            partes = numero_o_rango.split("-")
            if len(partes) != 2:
                error = INPUT_INVALIDO
                break

            inicio, fin = partes[0].strip(), partes[1].strip()
            if not inicio.isdigit() or not fin.isdigit():
                error = INPUT_INVALIDO
                break

            inicio, fin = int(inicio), int(fin)
            if inicio > fin:
                return INPUT_INVALIDO

            for id in range(inicio, fin + 1):
                lista_ids.append(id)

        else:
            error = INPUT_INVALIDO
            break

    if error:
        return error
    return lista_ids


def validar_ids_seleccionados(lista_de_ids, ids_coincidentes):

    if lista_de_ids == INPUT_INVALIDO:
        print(INPUT_INVALIDO)
        return False

    for id in lista_de_ids:
        if id not in ids_coincidentes:
            print(NUMERO_INVALIDO)
            return False

    return True


def eliminar_ids_de_tweets(lista_de_ids, tweets, tweets_normalizados_tokenizado):

    eliminados = set()

    for id in lista_de_ids:
        if id in eliminados:
            continue
        eliminados.add(id)

        tweet = tweets[id]
        print(f"{id}. {tweet}")
        # borrar_id_asociado_a_token(id, tweet, tweets)
        borrar_id_asociado_a_token(id, tweet, tweets_normalizados_tokenizado)


# -----------------------------------------------------------------------------

# Esta parte del código se ejecuta al final,
# asegurando que se ejecute el programa
# mediante la terminal correctamente y permitiendo que se puedan realizar
# los tests de forma automática y aislada.
if __name__ == "__main__":
    main()
