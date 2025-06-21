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
    tweet_normalizado = "".join(lista_caracteres).strip()

    # si solo tiene espacios devuelve una cadena vacia
    if tweet_normalizado == "":
        return ""

    return tweet_normalizado


def tokenizar(tweet_normalizado, len_tokenizacion):
    """Tokeniza el tweet_normalizado con la longitud dada por el parametro.
    Si la longitud palabra es menor a len_tokenizacion, se almacena directo.
    Caso contrario para cada caracter en una palabra, almacena tokens desde
    su posicion hasta su posicion +len_tokenizacion, +(len_tokenizacion+1),
    ..., +(len_tokenizacion+n) hasta llegar al final de la palabra.
    si inicio + len_tokenizacion (o sea fin) >= len(palabra) + 1 --> range()
    crea rango vacio, por lo tanto no se almacenan tokens con
    len < len_tokenizacion"""

    tweet_tokenizado = []

    lista_de_palabras = tweet_normalizado.split(" ")

    for palabra in lista_de_palabras:

        if len(palabra) < len_tokenizacion:
            if palabra not in tweet_tokenizado:
                tweet_tokenizado.append(palabra)
            continue

        for inicio in range(len(palabra)):

            for fin in range(inicio + len_tokenizacion, len(palabra) + 1):
                segmento = palabra[inicio:fin]

                if segmento not in tweet_tokenizado:
                    tweet_tokenizado.append(segmento)

    return tweet_tokenizado
