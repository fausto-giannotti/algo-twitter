# import os
import sys

ERROR_IMPORTACION = "El/los archivos a importar deben existir y ser .txt válidos"
DIRECCION_ERRONEA = "No se pudo exportar a esa dirección."
TOKENIZACION_INVALIDA = "El argumento de cantidad de tokens es inválido."
DB_INVALIDA = "Error al intentar abrir el programa."

RESULTADOS_BUSQUEDA = "Resultados de la busqueda:"
NO_ENCONTRADOS = "No se encontraron tweets."
TWEETS_ELIMINADOS = "Tweets eliminados:"
NUMERO_INVALIDO = "Numero de tweet invalido."
INPUT_INVALIDO = "Input invalido."
ATRAS = "**"
FIN = "Finalizando..."
DB_PATH = "db"

MENU = (
    "1. Crear Tweet\n"
    "2. Buscar Tweet\n"
    "3. Eliminar Tweet\n"
    "4. Importar Tweet\n"
    "5. Exportar Tweet\n"
    "6. Salir\n"
    ">>> "
)

CREAR_TWEET = "1"
BUSCAR_TWEET = "2"
ELIMINAR_TWEET = "3"
IMPORTAR_TWEET = "4"
EXPORTAR_TWEET = "5"
FINALIZAR = "6"

INGRESE_TWEET = "Ingrese el tweet a almacenar: "
INGRESE_BUSQUEDA = "Ingrese la/s palabra/s clave a buscar:\n>>> "
INGRESE_TWEETS_ELIMINAR = "Ingrese los numeros de tweets a eliminar:\n>>> "

LEN_DEFAULT_TOKENIZACION = 3


def main(arg=LEN_DEFAULT_TOKENIZACION):

    id = 0
    tweets = {}
    tweets_normalizados_tokenizados = {}

    len_tokenizacion = arg

    while True:

        user_input = input(MENU)

        if user_input == CREAR_TWEET:
            id = crear_tweet(
                id, tweets, tweets_normalizados_tokenizados, len_tokenizacion
            )

        elif user_input == BUSCAR_TWEET:
            buscar_tweet(tweets, tweets_normalizados_tokenizados, len_tokenizacion)

        elif user_input == ELIMINAR_TWEET:
            eliminar_tweets(tweets, tweets_normalizados_tokenizados, len_tokenizacion)

        elif user_input == FINALIZAR:
            print(FIN)
            break

        else:
            print(INPUT_INVALIDO)


# -----------------------------------------------------------------------------


def crear_tweet(id, tweets, tweets_normalizados_tokenizados, len_tokenizacion):
    """
    El usuario ingresa un tweet que se almacena con su respectivo id (que es
    unico e irrepetible); id se recibe como parametro por para poder tener
    en cuenta valor pervio del id y devolver sumarle 1 id+1 (solo si
    efectivamente se guarda el token) caso contrario (o sea input == **)
    devuelve el mismo id.
    """

    while True:  # hasta recibir input valido o ATRAS

        tweet_a_almacenar = input(INGRESE_TWEET)

        if tweet_a_almacenar == ATRAS:
            return id

        tweet_normalizado = normalizar(tweet_a_almacenar)

        if tweet_normalizado == "":
            print(INPUT_INVALIDO)
            continue

        # dado que tweet es valido, es almacenado en ambos dicts:

        tweets[id] = tweet_a_almacenar

        for token in tokenizar(tweet_normalizado, len_tokenizacion):

            # si token ya fue almacenado antes, sumarle un nuevo id
            if token in tweets_normalizados_tokenizados:
                tweets_normalizados_tokenizados[token].append(id)

            # si token nunca fue almacenado antes,
            # guardarlo como clave con su respectivo id
            else:
                tweets_normalizados_tokenizados[token] = [id]

        print(f"OK {id}")

        return id + 1


def normalizar(tweet):

    acentos_y_otros = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ñ": "n",
        "ü": "u",
    }

    lista_caracteres = list(tweet.lower())

    # se realizan las comparaciones por cada elemento en la lista
    for posicion in range(len(lista_caracteres)):

        # si caracter en posicion =! num o letra o espacio, elimina dicho caracter
        if not (
            lista_caracteres[posicion].isalnum() or lista_caracteres[posicion] == " "
        ):
            lista_caracteres[posicion] = ""

        # reemplaza caracteres con tilde por su version sin
        lista_caracteres[posicion] = acentos_y_otros.get(
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

    # convierte la lista en una cadena
    tweet_normalizado = "".join(lista_caracteres)

    # si solo tiene espacios devuelve una cadena vacia
    if tweet_normalizado.strip() == "":
        return ""

    return tweet_normalizado


def tokenizar(tweet_normalizado, len_tokenizacion):

    tweet_tokenizado = []

    lista_de_palabras = tweet_normalizado.split(" ")

    for palabra in lista_de_palabras:

        # si longitud palabra menor que LEN_TOKENIZACION (= 3), se almacena directo
        if len(palabra) < len_tokenizacion:
            if palabra not in tweet_tokenizado:
                tweet_tokenizado.append(palabra)
            continue

        for inicio in range(len(palabra)):

            for fin in range(inicio + len_tokenizacion, len(palabra) + 1):
                segmento = palabra[inicio:fin]

                # para cada caracter en una palabra, almacena tokens desde su posicion
                # hasta su posicion +3, +4, ..., +n hasta llegar al final de la palabra
                # si inicio + 3 (o sea fin) >= len(palabra) + 1 --> range() crea rango
                # vacio, por lo tanto no se almacenan tokens con len < 3

                # no volver a almacenar segmentos ya almacenados
                if segmento not in tweet_tokenizado:
                    tweet_tokenizado.append(segmento)

    return tweet_tokenizado


# -----------------------------------------------------------------------------


def buscar_tweet(tweets, tweets_normalizados_tokenizados, len_tokenizacion):
    """
    Pide input al usuario, lo normaliza y lo tokeniza.
    Si la busqueda se puede hacer (es decir, el input es valido) imprime tweets
    originales que coiciden o NO_ENCONTRADOS si no hay coicidencias.
    Devuelve lista de ids que coiciden con la busqueda.
    """

    while True:
        texto_a_buscar = input(INGRESE_BUSQUEDA)

        if texto_a_buscar == ATRAS:
            return []

        busqueda_normalizada = normalizar(texto_a_buscar)
        if busqueda_normalizada == "":
            print(INPUT_INVALIDO)
            continue

        ids_comunes = obtener_ids_tweets_coincidentes(
            busqueda_normalizada, tweets_normalizados_tokenizados, len_tokenizacion
        )

        if not ids_comunes:
            print(NO_ENCONTRADOS)
            return []

        print(RESULTADOS_BUSQUEDA)
        for id in sorted(ids_comunes):  # se imprimen resultados ordenados
            print(f"{id}. {tweets[id]}")

        return ids_comunes


def obtener_ids_tweets_coincidentes(
    busqueda_normalizada, tweets_normalizados_tokenizados, len_tokenizacion
):
    busqueda_tokenizada = tokenizar(busqueda_normalizada, len_tokenizacion)

    # va a ser una lista de listas donde cada sublista
    # contiene a los ids asociados a cada token
    listas_de_ids = []

    # si no hay coincidencias devolver lista vacia
    # si las hay, almacenar lista de ids asociados a token coincidente
    for token in busqueda_tokenizada:
        ids = tweets_normalizados_tokenizados.get(token)
        if ids is None:
            return []
        listas_de_ids.append(ids)

    # se devuelve una nueva lista donde solo son validos
    # los ids que coiciden con todos los tokens ingresados
    ids_comunes = set(listas_de_ids[0])

    # interseccion entre primer lista y todas las demas
    for lista in listas_de_ids[1:]:
        ids_comunes = ids_comunes & set(lista)

    return list(ids_comunes)


# -----------------------------------------------------------------------------


def eliminar_tweets(tweets, tweets_normalizados_tokenizados, len_tokenizacion):
    """
    Llama a buscar_tweet() y almacena lista de ids coincidentes con la busqueda
    Pide ids a eliminar y verifica que estos sean validos (es decir, que el
    input sea valido y que los ids ingresados coicidan con el resultado
    de la busqueda) No devuelve nada, solo modifica diccionario
    """

    while True:

        ids_coincidentes = buscar_tweet(
            tweets, tweets_normalizados_tokenizados, len_tokenizacion
        )

        # si ATRAS (en buscar_tweet) o si no hay resultados de busqueda, vuelve al menu
        if not ids_coincidentes:
            return

        while True:
            ids_a_eliminar = input(INGRESE_TWEETS_ELIMINAR).split(",")

            if ids_a_eliminar[0] == ATRAS:
                return

            # se devuelve lista de ids solo si input es valido
            lista_de_ids = listar_ids(ids_a_eliminar)

            # si INPUT_INVALIDO o NO_ENCONTRADO, volver a pedir numeros de tweets a eliminar
            if not validar_ids_seleccionados(lista_de_ids, ids_coincidentes):
                continue

            lista_de_ids.sort()

            ids_eliminados = eliminar_ids_de_tweets(
                lista_de_ids, tweets, tweets_normalizados_tokenizados, len_tokenizacion
            )

            print(TWEETS_ELIMINADOS)
            for id_eliminado in ids_eliminados:
                print(f"{id_eliminado}. {tweets[id_eliminado]}")

            return


def listar_ids(ids_a_eliminar):
    """
    Recibe el input (la lista de ids a eliminar), verifica que la lista de
    ids contenga unicamente numeros o rangos; a los rangos los separa en
    numeros y devuelve una lista ordenada de ids
    """

    lista_ids = []
    error = None

    for numero_o_rango in ids_a_eliminar:
        numero_o_rango = numero_o_rango.strip()
        if not numero_o_rango:  # si elemento de la lista vacio --> input invalido
            error = INPUT_INVALIDO
            break

        if numero_o_rango.isdigit():  # si es un unico numero
            lista_ids.append(int(numero_o_rango))
            continue

        if "-" in numero_o_rango:  # si es un rango
            partes = numero_o_rango.split("-")
            if len(partes) != 2:  # verifica que sea rango con inicio y fin
                error = INPUT_INVALIDO
                break

            # verifica que inicio y fin sean numeros
            inicio, fin = partes[0].strip(), partes[1].strip()
            if not inicio.isdigit() or not fin.isdigit():
                error = INPUT_INVALIDO
                break

            inicio, fin = int(inicio), int(fin)
            if inicio > fin:
                error = INPUT_INVALIDO
                break

            # almacena un id por cada numero de range(inicio, fin)
            for id in range(inicio, fin + 1):
                lista_ids.append(id)

        else:  # si se ingresa cualquier cosa que no sea un numero
            error = INPUT_INVALIDO
            break

    if error:  # si hubo algun error, devolver []
        return []
    return lista_ids


def validar_ids_seleccionados(lista_de_ids, ids_coincidentes):
    """
    Recibe una lista ordenada de ids y verifica que estos coicidan con
    los resultados de busqueda; devuelve True si la lista de ids es valida,
    sino, devuelve False
    """

    if lista_de_ids == []:
        print(INPUT_INVALIDO)
        return False

    # si la lista de ids no coincide con los resultados de busqueda, entonces error
    for id in lista_de_ids:
        if id not in ids_coincidentes:
            print(NUMERO_INVALIDO)
            return False

    return True


def eliminar_ids_de_tweets(
    lista_de_ids, tweets, tweets_normalizados_tokenizados, len_tokenizacion
):
    """
    Crea un set para evitar repetir eliminaciones, y llama
    borrar_id_asociado_a_token() (quien efectivamente borra
    ids y tokens)
    """
    eliminados = set()  # para no tratar de eliminar tweets ya eliminados

    for id in lista_de_ids:
        if id in eliminados:
            continue
        eliminados.add(id)

        tweet = tweets[id]

        # borra todos los ids del tweet asociados a tokens y si el unico id
        # asociado era el eliminado, tambien elimina token
        borrar_id_asociado_a_token(
            id, tweet, tweets_normalizados_tokenizados, len_tokenizacion
        )

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

# Esta parte del código se ejecuta al final, asegurando que se ejecute el programa
# mediante la terminal correctamente y permitiendo que se puedan realizar
# los tests de forma automática y aislada.

if __name__ == "__main__":

    args = sys.argv[1:]  # ignora nombre del archivo

    if len(args) > 1:  # verifica que se haya pasado 1 parametro
        print(TOKENIZACION_INVALIDA)
        sys.exit(1)

    if len(args) == 0:
        arg = LEN_DEFAULT_TOKENIZACION  # 3
    else:
        # verifica que el parametro sea valido
        try:
            arg = int(args[0])
            if arg < 1:
                raise ValueError

        except ValueError:
            print(TOKENIZACION_INVALIDA)
            sys.exit(1)

    main(arg)
