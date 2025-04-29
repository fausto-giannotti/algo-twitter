# aca voy a hacer todo el desarollo

NUMERO_INVALIDO = "Numero de tweet invalido."
NO_ENCONTRADOS = "No se encontraron tweets."
INPUT_INVALIDO = "Input invalido."
FIN = "Finalizando..."
RESULTADOS_BUSQUEDA = "Resultados de la busqueda:"
TWEETS_ELIMINADOS = "Tweets eliminados:"
ATRAS = "**"

# errores validacion 1-10, 15-44, 46-52, 54, 55, 57-67
# resolver lo de poder eliminar con comas (o sea que 1, 2, 3, 7-10) funcione


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
            resultado = crear_tweet(id, tweets, tweets_normalizados_tokenizado)

            # si tweet es valido actualiza id con ultimo valor:
            try:
                id = int(resultado.split()[1])

            # si tweet no es valido, valor de id se mantiene es decir, se ejecuta return id
            # en ese caso, al intentar usar .split() para un int, ocurrira AttributeError
            except AttributeError:
                continue

            print(resultado)  # de la forma "OK {id}"
        elif user_input == "2":
            texto_a_buscar = input("Ingrese la/s palabra/s clave a buscar:\n>>> ")
            buscar_tweet(tweets, tweets_normalizados_tokenizado, texto_a_buscar)
        elif user_input == "3":
            busqueda_para_eliminar = input("Ingrese el tweet a eliminar:\n >>> ")
            if busqueda_para_eliminar == ATRAS:
                continue
            lista_de_ids_limpia = validar_ids_eliminar(
                tweets, tweets_normalizados_tokenizado, busqueda_para_eliminar
            )

            if lista_de_ids_limpia == ATRAS or lista_de_ids_limpia is None:
                continue

            eliminar_tweet(tweets, tweets_normalizados_tokenizado, lista_de_ids_limpia)

        elif user_input == "4":
            return print(FIN)
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

    tweet_a_almacenar = input("Ingrese el tweet a almacenar:")

    if tweet_a_almacenar == ATRAS:
        return id  # se devuelve el mismo id sin sumar

    tweet_normalizado = normalizar(tweet_a_almacenar)

    if tweet_normalizado == "":
        print(INPUT_INVALIDO)
        return id  # se devuelve el mismo id sin sumar

    # tweet_normalizado_tokenizado = tokenizar(tweet_normalizado)

    # dado que tweet es valido, es almacenado en ambos dicts:

    tweets[id] = tweet_a_almacenar

    for token in tokenizar(tweet_normalizado):

        # si token ya fue almacenado antes, sumarle un nuvevo id
        if token in tweets_normalizados_tokenizado:
            tweets_normalizados_tokenizado[token].append(id)

        # si token nunca fue almacenado antes,
        # guardarlo como clave con su respectivo id

        else:
            tweets_normalizados_tokenizado[token] = [id]

    id += 1

    return f"OK {id}"  # se devuelve el id+=1


def normalizar(tweet):

    acentos_y_enie = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n"}

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

    return tweet_normalizado


def tokenizar(tweet_normalizado):

    tweet_tokenizado = []

    lista_de_palabras = tweet_normalizado.split(" ")

    # para tokenizar con n = 3, se tiene que ir almacenando por segmentos
    # o sea desde pos a pos+3, desde pos a pos+4 y asi sucesivamente
    # cuando se llega al final de las combinaciones para pos,
    # se hace lo mismo para pos+1
    # por ej: "buenas" --> "bue", "buen", "buena", "buenas", "uen",
    # "uena", "uenas", "ena", "enas", "nas"
    # si alguna combinacion ya esta almacenada, no almacenar de vuelta
    # si len(palabra) <= 3 se almacena directamente la palabra

    # se accede a una palaba
    for palabra in lista_de_palabras:

        # si longitud palabra menor igual que 3, se almacena directo
        if len(palabra) <= 3:
            tweet_tokenizado.append(palabra)
        else:

            # para cada elemnto de la palabra:
            for inicio in range(len(palabra)):

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

                for fin in range(inicio + 3, len(palabra) + 1):
                    segmento = palabra[inicio:fin]

                    # para cada caracter, ir desde su pos a pos+3, +4, +n hasta
                    # llegar al final de la palabra; desp arranca desde pos+3+1
                    # y repite hasta almecenar cada combinacion

                    # no volver a almacenar segmentos ya almacenados
                    if segmento not in tweet_tokenizado:
                        tweet_tokenizado.append(segmento)

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


def buscar_tweet(tweets, tweets_normalizados_tokenizado, texto_a_buscar):

    if texto_a_buscar == ATRAS:
        return None

    busqueda_normalizada = normalizar(texto_a_buscar)

    # si se buscan caracteres que dados los tweets normaliazdos no existen
    # devolver input invalido

    if busqueda_normalizada == "":
        print(INPUT_INVALIDO)
        return None

    # se tokeniza texto normalizado para permitir su comparacion
    busqueda_tokenizada = tokenizar(busqueda_normalizada)

    # donde se almacenaran todos los id que coincidan
    ids_coincidentes = []

    # para cada token en texto ingresado para buscar:
    for token in busqueda_tokenizada:

        # se ejecuta si token existe como clave en el dict.
        if token in tweets_normalizados_tokenizado:

            # para cada id que coincide con el token
            for id in tweets_normalizados_tokenizado[token]:

                # si id nunca coincidio y fue almacenado antes, se almacena
                if id not in ids_coincidentes:
                    ids_coincidentes.append(id)

                # si id ya fue almacenado antes, se ignora
                else:
                    continue

    if ids_coincidentes == []:
        print(NO_ENCONTRADOS)
        return NO_ENCONTRADOS

    print("Resultado de la busqueda:")

    # para cada id coincidente, se imprime su tweet original correspondiente
    for id in ids_coincidentes:
        print(f"{id}. {tweets[id]}")

    return ids_coincidentes


"""
Validar ids a eliminar:
esta funcion llama a buscar_tweets para buscar coincidencias con input;
en base a dichas coincidencias, pide al usuario que ingrese ids a eliminar
verifica que esos ids sean numeros o rangos y que coicidan con el resultado
de la busqueda --> devuelve lista de ids eliminables

Eliminar tweet: llama a la fu
"""


def validar_ids_eliminar(
    tweets, tweets_normalizados_tokenizado, busqueda_para_eliminar
):

    # donde se almacenan id sin rangos
    # ej: si input 3-5 se almacena 3, 4, 5
    lista_de_ids_limpia = []

    ids_coincidentes = buscar_tweet(
        tweets, tweets_normalizados_tokenizado, busqueda_para_eliminar
    )

    # si buscar no encuentra coicidencias, terminar funcion
    if ids_coincidentes == NO_ENCONTRADOS:
        return None

    ids_a_eliminar = input("Ingrese los numeros de tweets a eliminar:\n>>> ")

    lista_ids_a_eliminar = ids_a_eliminar.split(",")

    # comprobamos que los valores sean nums o rangos
    for numero_o_rango in lista_ids_a_eliminar:

        numero_o_rango = numero_o_rango.strip()  # eliminar espacios de mas

        # if not (numero_o_rango.isdigit() or "-" in numero_o_rango):
        #    print(INPUT_INVALIDO)
        #    return None

        if numero_o_rango.isdigit():  # si es un num, se agrega a la lista

            id = int(numero_o_rango)

            if id not in ids_coincidentes:
                print(NUMERO_INVALIDO)
                return None

            lista_de_ids_limpia.append(id)

        elif (
            "-" in numero_o_rango
        ):  # si es un rango se agregan todos los nums. del rango a ella
            inicio, fin = numero_o_rango.split("-")

            for id in range(int(inicio), int(fin) + 1):
                lista_de_ids_limpia.append(id)

        else:
            print(INPUT_INVALIDO)
            return None

        return lista_de_ids_limpia


def eliminar_tweet(tweets, tweets_normalizados_tokenizado, lista_de_ids_limpia):

    # se elimnan todos los tweets para los ids indicados
    # pero antes se confirma que existen
    # si se intenta acceder a una clave inexsitente = KeyError

    for id in lista_de_ids_limpia:

        tweet = tweets[id]

        # try:
        #    tweet = tweets[id]
        # except KeyError:
        #    print(NUMERO_INVALIDO)
        #    return NUMERO_INVALIDO

        # si todos los id existen, se elimnan los tweets correspondinetes

        del tweets[id]

        # si el tweet existe, eliminamos los tokens asociados en el dict
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


# -----------------------------------------------------------------------------

# Esta parte del código se ejecuta al final,
# asegurando que se ejecute el programa
# mediante la terminal correctamente y permitiendo que se puedan realizar
# los tests de forma automática y aislada.
if __name__ == "__main__":
    main()
