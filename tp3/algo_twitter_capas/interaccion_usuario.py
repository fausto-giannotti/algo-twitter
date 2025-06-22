import os

from logica import (
    crear_tweet,
    buscar_tweet,
    eliminar_tweets,
    importar_tweets,
    exportar_tweets,
)

from manejo_cadenas import normalizar, parsear_ids_ingresados

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
INGRESE_RUTA_IMPORTAR = "Ingrese la/s ruta/s de donde importar:\n"
INGRESE_RUTA_EXPORTAR = "Ingrese el archivo donde exportar:\n"

ATRAS = "**"
FIN = "Finalizando..."
INPUT_INVALIDO = "Input invalido."

NO_ENCONTRADOS = "No se encontraron tweets."
RESULTADOS_BUSQUEDA = "Resultados de la busqueda:"
TWEETS_ELIMINADOS = "Tweets eliminados:"
ERROR_IMPORTACION = "El/los archivos a importar deben existir y ser .txt válidos"
DIRECCION_ERRONEA = "No se pudo exportar a esa dirección."
NUMERO_INVALIDO = "Numero de tweet invalido."


# --------------------------------------------------------------------------
"""Todo lo relacionado a pedir input, validarlo y mostrar por pantalla."""
# --------------------------------------------------------------------------


def llamar_funciones(len_tokenizacion, tweets, tweets_normalizados_tokenizados, id):
    """Muestra menu, pide input y coordina las llamadas a las funciones."""

    while True:

        user_input = pedir_numero_menu()

        if user_input == CREAR_TWEET:
            id = pedir_y_guardar_tweet(
                id, tweets, tweets_normalizados_tokenizados, len_tokenizacion
            )

        elif user_input == BUSCAR_TWEET:
            pedir_busqueda_y_buscar(
                tweets, tweets_normalizados_tokenizados, len_tokenizacion
            )

        elif user_input == ELIMINAR_TWEET:
            buscar_y_eliminar(tweets, tweets_normalizados_tokenizados, len_tokenizacion)

        elif user_input == IMPORTAR_TWEET:
            id = pedir_rutas_e_importar(
                id, tweets, tweets_normalizados_tokenizados, len_tokenizacion
            )

        elif user_input == EXPORTAR_TWEET:
            pedir_ruta_y_exportar(tweets)

        elif user_input == FINALIZAR:
            imprimir_fin()
            break

        else:
            imprimir_input_invalido()


# -------------------------interfaz-guardar--------------------------


def pedir_y_guardar_tweet(
    id, tweets, tweets_normalizados_tokenizados, len_tokenizacion
):
    """Llama a pedir_y_validar_tweet() que devuelve un tweet valido
    y llama a crear_tweet(). Luego imprime el id del tweet creado."""

    tweet = pedir_y_validar_tweet()

    if tweet is None:
        return id

    id = crear_tweet(
        id,
        tweet,
        tweets,
        tweets_normalizados_tokenizados,
        len_tokenizacion,
    )

    imprimir_ok_id(id - 1)  # dado que crear devuelve ultimo id + 1

    return id


def pedir_y_validar_tweet():
    """Pide al usuario un tweet y lo valida. Si es invalido vuelve
    a pedir hasta que lo sea excepto en el caso de ATRAS que devuelve
    None."""

    while True:
        tweet_a_almacenar = pedir_tweet()

        if tweet_a_almacenar == ATRAS:
            return None

        tweet_normalizado = normalizar(tweet_a_almacenar)

        if tweet_normalizado == "":
            imprimir_input_invalido()
            continue
        break

    return tweet_a_almacenar


# -------------------------interfaz-buscar--------------------------


def pedir_busqueda_y_buscar(tweets, tweets_normalizados_tokenizados, len_tokenizacion):
    """Llama a pedir_y_validar_busqueda() que devuelve una lista
    vacia si el usuario ingresa ATRAS (y vuelve al menu) o el texto
    a buscar. Ahi llama a buscar_tweet que devuelve una lista de ids
    que coinciden. Si no hay coincidencias se imprime NO_ENCONTRADOS
    y si las hay se imprime cada una de ellas."""

    texto_a_buscar = pedir_y_validar_busqueda()

    if not texto_a_buscar:
        return []

    ids_comunes = buscar_tweet(
        texto_a_buscar,
        tweets,
        tweets_normalizados_tokenizados,
        len_tokenizacion,
    )

    if not ids_comunes:
        imprimir_no_encontrados()
        return []

    imprimir_resultados_busqueda()

    for i in sorted(ids_comunes):
        imprimir_tweets(i, tweets)

    return ids_comunes


def pedir_y_validar_busqueda():
    """Pide una texto a buscar y verifica que sea valida. Si no lo
    es vuelve a pedir (excepto en el caso de ATRAS). Devuelve el
    texto a buscar"""

    while True:
        texto_a_buscar = pedir_busqueda()

        if texto_a_buscar == ATRAS:
            return []

        busqueda_normalizada = normalizar(texto_a_buscar)
        if busqueda_normalizada == "":
            imprimir_input_invalido()
            continue

        break

    return texto_a_buscar


# -------------------------interfaz-eliminar--------------------------


def buscar_y_eliminar(tweets, tweets_normalizados_tokenizados, len_tokenizacion):
    """Llama a pedir_busqueda_y_buscar() que devuelve una lista de ids. Le
    pasa la lista a pedir_ids_a_eliminar() que devuelve la lista de ids que
    el usuario quiere eliminar. Llama a eliminar_tweets() que elimina y
    devuelve lista de tweets eliminados que son mostrados por pantalla."""

    ids_eliminables = pedir_busqueda_y_buscar(
        tweets, tweets_normalizados_tokenizados, len_tokenizacion
    )

    ids_a_eliminar = pedir_ids_a_eliminar(ids_eliminables)

    lista_tweets_eliminados = eliminar_tweets(
        ids_a_eliminar,
        tweets,
        tweets_normalizados_tokenizados,
        len_tokenizacion,
    )

    if not lista_tweets_eliminados:
        return

    imprimir_tweets_eliminados()
    imprimir_cada_tweet_eliminado(lista_tweets_eliminados)
    return


def pedir_ids_a_eliminar(ids_eliminables):
    """Recibe una lista de ids. Si esta vacia devuelve una lista vacia.
    Si no, pide al usuario ids a eliminar y los valida. Devuelve una lista
    de ids a ser eliminados."""

    if not ids_eliminables:
        return []

    while True:
        ids_a_eliminar = pedir_tweets_a_eliminar()

        if ids_a_eliminar[0] == ATRAS:
            return []

        # se devuelve lista de ids solo si input es valido
        lista_de_ids = parsear_ids_ingresados(ids_a_eliminar)

        # si INPUT_INVALIDO o NO_ENCONTRADO, volver a pedir numeros de tweets a eliminar
        if not validar_ids_seleccionados(lista_de_ids, ids_eliminables):
            continue

        return sorted(lista_de_ids)


def validar_ids_seleccionados(lista_de_ids, ids_eliminables):
    """Recibe una lista ordenada de ids y verifica que estos coicidan con
    los resultados de busqueda; devuelve True si la lista de ids es valida,
    sino, devuelve False"""

    if lista_de_ids == []:
        imprimir_input_invalido()
        return False

    # si la lista de ids no coincide con los resultados de busqueda, entonces error
    for id in lista_de_ids:
        if id not in ids_eliminables:
            imprimir_numero_invalido()
            return False

    return True


# -------------------------interfaz-importar--------------------------


def pedir_rutas_e_importar(
    id, tweets, tweets_normalizados_tokenizados, len_tokenizacion
):
    """Llama a pedir_y_validar_rutas() que devuelve rutas validas. Llama a
    importar_tweets() e imprime el numero de tweets almacenados."""

    id_inicial = id

    archivos_validos = pedir_y_validar_rutas()

    if archivos_validos is None:
        return id

    id = importar_tweets(
        id,
        archivos_validos,
        tweets,
        tweets_normalizados_tokenizados,
        len_tokenizacion,
    )

    numero_tweets_almacenados = id - id_inicial

    imprimir_ok_numero(numero_tweets_almacenados)

    return id


def pedir_y_validar_rutas():
    """Pide rutas hasta verificar que sean validas. Devuelve
    una lista de archivos validos."""

    while True:
        rutas = pedir_rutas_importar()
        if rutas == ATRAS:
            return None

        rutas_separadas = separar_y_validar_rutas(rutas)

        if rutas_separadas is None:
            imprimir_error_importacion()
            continue

        archivos_validos = validar_archivos(rutas_separadas)

        if archivos_validos is None:
            imprimir_error_importacion()
            continue

        if not archivos_validos:
            return []

        return archivos_validos


def separar_y_validar_rutas(rutas):
    """Verifica que se ingresen archivo/s y/o ruta/s validas.
    Devuelve una lista vacia si alguna es invalida y una lista
    de rutas si todas son validas"""

    if rutas.strip() == "":
        return None

    rutas_separadas = rutas.split(" ")

    for archivo_o_dir in rutas_separadas:
        if not os.path.exists(archivo_o_dir):
            return None

    return rutas_separadas


def validar_archivos(rutas_separadas):
    """Para una lista de rutas, valida cada una. Devuelve
    una lista o None (para diferenciar de archivos invalidos
    adentro de un dir y archivos invalidos ingresados directamente)."""

    archivos_validos = []

    for ruta in rutas_separadas:
        if os.path.isdir(ruta):
            lista_archivos_de_dir = listar_archivos(ruta)
            for archivo in lista_archivos_de_dir:
                if es_txt(archivo) and archivo_valido(archivo):
                    archivos_validos.append(archivo)

        if not os.path.isdir(ruta):
            if es_txt(ruta) and archivo_valido(ruta):
                archivos_validos.append(ruta)
            else:
                return None

    return archivos_validos


def listar_archivos(ruta):
    """Recibe un directorio y recorre todas las rutas, almacenando
    todos los .txt validos e ignorando el resto. Si alguna de las rutas
    en el directorio es otro directorio hace una llamada recursiva y asi
    sucesivamente hasta que haya solo archivos (o nada) y va devolviendo
    los .txt validos.
    Caso base: no hay ningun directorio/archivo en la ruta actual"""

    archivos = []

    for nombre in os.listdir(ruta):
        ruta_total = os.path.join(ruta, nombre)

        if os.path.isdir(ruta_total):
            archivos += listar_archivos(ruta_total)
        else:
            if not es_txt(ruta_total):
                continue
            archivos.append(ruta_total)

    return archivos


def archivo_valido(archivo):
    try:
        with open(archivo, "r"):
            pass
    except (IOError, OSError, UnicodeDecodeError):
        return False

    return True


def es_txt(archivo):
    return archivo.lower().endswith(".txt")


# -------------------------interfaz-exportar--------------------------


def pedir_ruta_y_exportar(tweets):
    """Pide una ruta hasta que sea valida. Llama a exportar_tweets
    e imprime el numero de tweets exportados"""

    while True:
        ruta = pedir_ruta_exportar()

        if ruta == ATRAS:
            return

        if not validar_ruta_exportar(ruta):
            continue

        break

    num_tweets_exportados = exportar_tweets(ruta, tweets)

    imprimir_ok_numero(num_tweets_exportados)


def validar_ruta_exportar(ruta):

    if not es_txt(ruta):
        imprimir_direccion_erronea()
        return ""

    partes_ruta = ruta.rsplit("/", 1)

    if len(partes_ruta) > 1:
        dir = partes_ruta[0]

        if not os.path.exists(dir) or not os.path.isdir(dir):
            imprimir_direccion_erronea()
            return ""

    return ruta


# -------------------------Pedidos-de-input--------------------------


def pedir_numero_menu():
    numero_menu = input(MENU)
    return numero_menu


def pedir_tweet():
    tweet = input(INGRESE_TWEET)
    return tweet


def pedir_busqueda():
    busqueda = input(INGRESE_BUSQUEDA)
    return busqueda


def pedir_tweets_a_eliminar():
    tweets = input(INGRESE_TWEETS_ELIMINAR).split(",")
    return tweets


def pedir_rutas_importar():
    rutas = input(INGRESE_RUTA_IMPORTAR)
    return rutas


def pedir_ruta_exportar():
    ruta = input(INGRESE_RUTA_EXPORTAR)
    return ruta


# -------------------------imprimir-mensajes--------------------------


def imprimir_fin():
    print(FIN)


def imprimir_input_invalido():
    print(INPUT_INVALIDO)


def imprimir_ok_id(id):
    print(f"OK {id}")


def imprimir_no_encontrados():
    print(NO_ENCONTRADOS)


def imprimir_resultados_busqueda():
    print(RESULTADOS_BUSQUEDA)


def imprimir_tweets(id, tweets):
    print(f"{id}. {tweets[id]}")


def imprimir_tweets_eliminados():
    print(TWEETS_ELIMINADOS)


def imprimir_numero_invalido():
    print(NUMERO_INVALIDO)


def imprimir_cada_tweet_eliminado(lista_tweets_eliminados):
    for tweet in lista_tweets_eliminados:
        print(tweet)


def imprimir_error_importacion():
    print(ERROR_IMPORTACION)


def imprimir_ok_numero(numero):
    print(f"OK {numero}")


def imprimir_direccion_erronea():
    print(DIRECCION_ERRONEA)
