INPUT_INVALIDO = "Input invalido."


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
    ..., +(len_tokenizacion+n) hasta llegar al final de la palabra."""

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


def parsear_ids_ingresados(ids_a_eliminar):
    """
    Recibe la lista de ids a eliminar, verifica que la lista de
    ids contenga unicamente numeros o rangos; a los rangos los separa en
    numeros y devuelve una lista ordenada de ids
    """

    lista_ids = []
    error = False

    for numero_o_rango in ids_a_eliminar:
        numero_o_rango = numero_o_rango.strip()
        if not numero_o_rango:  # i.e. elemento de la lista vacio
            error = True
            break

        if numero_o_rango.isdigit():
            lista_ids.append(int(numero_o_rango))
            continue

        if "-" in numero_o_rango:  # si es un rango
            partes = numero_o_rango.split("-")
            if len(partes) != 2:
                error = True
                break

            inicio, fin = partes[0].strip(), partes[1].strip()
            if not inicio.isdigit() or not fin.isdigit():
                error = True
                break

            inicio, fin = int(inicio), int(fin)
            if inicio > fin:
                error = True
                break

            # almacena un id por cada numero de range(inicio, fin)
            for id in range(inicio, fin + 1):
                lista_ids.append(id)

        else:  # si se ingresa cualquier otra cosa
            error = True
            break

    if error:
        return []

    return lista_ids
