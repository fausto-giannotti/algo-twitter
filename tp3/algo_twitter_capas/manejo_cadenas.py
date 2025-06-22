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


def parsear_ids_ingresados(ids_a_eliminar):
    """
    Recibe la lista de ids a eliminar, verifica que la lista de
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
