import os
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
INGRESE_RUTA_IMPORTAR = "Ingrese la/s ruta/s de donde importar:\n"
INGRESE_RUTA_EXPORTAR = "Ingrese el archivo donde exportar:\n"

LEN_DEFAULT_TOKENIZACION = 3


def main(args=None):

    len_tokenizacion = validar_argumentos(args)

    if len_tokenizacion is None:
        print(TOKENIZACION_INVALIDA)
        sys.exit(1)

    tweets = {}
    tweets_normalizados_tokenizados = {}

    id = inicializar_db(tweets, tweets_normalizados_tokenizados, len_tokenizacion)

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

        elif user_input == IMPORTAR_TWEET:
            id = importar_tweets(
                id, tweets, tweets_normalizados_tokenizados, len_tokenizacion
            )

        elif user_input == EXPORTAR_TWEET:
            exportar_tweets(tweets)

        elif user_input == FINALIZAR:
            print(FIN)
            break

        else:
            print(INPUT_INVALIDO)


# -----------------------------------------------------------------------------


def validar_db():
    """Verifica que DB_PATH sea un dir valido. Lo mismo con cada uno de los
    archivos dentro del dir. Si hay algun error => exit(1)"""

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
    """Llama a validar_db para verificar que sea valida. Si hay tweets en la db
    los almacena en los dicts que recibe por parametros. Los archivos vacios
    (i.e. de tweets borrados) son ingorados. Devuelve el ultimo id de la
    db + 1 si hay tweets, caso contrario devuelve id = 0."""

    id_max = 0

    validar_db()

    # dado que db es valida y todos sus archivos lo son

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


# -----------------------------------------------------------------------------


def crear_tweet(id, tweets, tweets_normalizados_tokenizados, len_tokenizacion):
    """
    El usuario ingresa un tweet que se almacena con su respectivo id;
    id se recibe como parametro para poder tener en cuenta valor
    pervio del id y devolver id+1 (solo si efectivamente se guarda el
    token) caso contrario (o sea input == **) devuelve el mismo id.
    """

    while True:  # hasta recibir input valido o ATRAS

        tweet_a_almacenar = input(INGRESE_TWEET)

        if tweet_a_almacenar == ATRAS:
            return id

        tweet_normalizado = normalizar(tweet_a_almacenar)

        if tweet_normalizado == "":
            print(INPUT_INVALIDO)
            continue

        tweet_tokenizado = tokenizar(tweet_normalizado, len_tokenizacion)

        persistir_tweet(id, tweet_a_almacenar)

        almacenar_tweet(
            id,
            tweet_a_almacenar,
            tweets,
            tweets_normalizados_tokenizados,
            tweet_tokenizado,
        )

        print(f"OK {id}")

        return id + 1


def almacenar_tweet(
    id,
    tweet_a_almacenar,
    tweets,
    tweets_normalizados_tokenizados,
    tweet_tokenizado,
):
    """Recibe las 2 versiones del tweet (normalizado-tokenizado por
    un lado, y sin modificar por el otro) con su respectivo id y los dos dicts.
    Los almacena en ambos"""

    tweets[id] = tweet_a_almacenar

    for token in tweet_tokenizado:

        # si token ya fue almacenado antes, sumarle un nuevo id
        if token in tweets_normalizados_tokenizados:
            tweets_normalizados_tokenizados[token].append(id)

        # si token nunca fue almacenado antes,
        # guardarlo como clave con su respectivo id
        else:
            tweets_normalizados_tokenizados[token] = [id]


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


# -----------------------------------------------------------------------------


def buscar_tweet(tweets, tweets_normalizados_tokenizados, len_tokenizacion):
    """
    Pide input al usuario, lo normaliza y lo tokeniza. Si la busqueda se
    puede hacer (es decir, el input es valido) imprime tweets originales
    que coiciden o NO_ENCONTRADOS si no hay coicidencias. Devuelve
    lista de ids que coiciden con la busqueda.
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


def eliminar_tweets(tweets, tweets_normalizados_tokenizados, len_tokenizacion):
    """
    Llama a buscar_tweet() y almacena lista de ids coincidentes con la busqueda.
    Pide ids a eliminar y verifica que estos sean validos (es decir, que el
    input sea valido y que los ids ingresados coicidan con el resultado
    de la busqueda) No devuelve nada, solo modifica los diccionarios.
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
                del tweets[id_eliminado]

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


def importar_tweets(id, tweets, tweets_normalizados_tokenizados, len_tokenizacion):
    """Pide al usuario que ingrese las rutas de donde importar. Las valida y lee linea
    por linea cada tweet mientras los va almacenado en los dicts y guardando en la db.
    Devuelve el utlimo id almacenado + 1"""
    while True:

        numero_tweets_almacenados = 0

        rutas = input(INGRESE_RUTA_IMPORTAR)
        if rutas == ATRAS:
            return id

        rutas_separadas = validar_rutas(rutas)

        if not rutas_separadas:
            print(ERROR_IMPORTACION)
            continue

        hay_archivos, archivos_validos_txt = validar_archivos_txt(rutas_separadas)
        hay_dirs, archivos_validos_de_dir = validar_archivos_en_dirs(rutas_separadas)

        archivos_validos = archivos_validos_txt + archivos_validos_de_dir

        if hay_archivos and not archivos_validos_txt:
            print(ERROR_IMPORTACION)
            continue

        if not archivos_validos and hay_dirs:
            break

        for archivo in archivos_validos:
            with open(archivo, "r", encoding="utf8") as archivo_tweets:
                for tweet in archivo_tweets:
                    tweet = tweet.rstrip()
                    tweet_normalizado = normalizar(tweet)
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
                    numero_tweets_almacenados += 1
        break

    print(f"OK {numero_tweets_almacenados}")
    return id


def validar_rutas(rutas):
    """Verifica que se ingresen archivo/s y/o ruta/s validas.
    Devuelve una lista vacia si alguna es invalida y una lista
    de rutas si todas son validas"""

    if rutas.strip() == "":
        return []

    rutas_separadas = rutas.split(" ")

    for archivo_o_dir in rutas_separadas:
        if not os.path.exists(archivo_o_dir):
            return []

    return rutas_separadas


def validar_archivos_en_dirs(rutas_separadas):
    """Recibe una lista de rutas. Para cada ruta que sea un dir lista todos
    los archivos en el y guarda en una lista todos aquellos que
    son .txt validos. Devuelve True si hay al menos un dir, sino, False.
    Ademas, devuelve una lista con los nombres de los archivos validos, si
    no hay ninguno que lo sea devuelve una lista vacia"""

    hay_dirs = False
    archivos_validos_dirs = []
    for ruta in rutas_separadas:
        if os.path.isdir(ruta):
            hay_dirs = True
            lista_archivos_de_dir = listar_archivos(ruta)
            for archivo in lista_archivos_de_dir:
                if es_txt(archivo) and archivo_valido(archivo):
                    archivos_validos_dirs.append(archivo)

    return hay_dirs, archivos_validos_dirs


def validar_archivos_txt(rutas_separadas):
    """Recibe una lista de rutas. Para cada ruta que sea un archivo verifica
    que sea valido y lo almacena en una lista. Devuelve True si hay al menos
    un archivo, sino, False. Ademas, devuelve una lista con los nombres de
    los archivos excepto si hay al menos 1 invalido, ahi devuelve una lista
    vacia"""

    hay_archivos = False
    archivos_validos_txt = []
    for ruta in rutas_separadas:
        if not os.path.isdir(ruta):
            hay_archivos = True
            if es_txt(ruta) and archivo_valido(ruta):
                archivos_validos_txt.append(ruta)
            else:
                archivos_validos_txt = []
                break
    return hay_archivos, archivos_validos_txt


def listar_archivos(ruta):
    """Recibe un directorio y recorre todas las rutas, almacenando
    todos los .txt validos e ignorando el resto. Si alguna de las rutas
    en el directorio es otro directorio hace una llamada recursiva y asi
    sucesivamente hasta que haya solo archivos (o nada) y va devolviendo
    los .txt validos.
    Caso base: no hay ningun directorios/archivos en la ruta actual"""
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


# -----------------------------------------------------------------------------


def exportar_tweets(tweets):
    """Pide la ruta de una archivo. Si la ruta esta en un dir, verifica que el
    dir existe. Crea o sobrescribe el archivo dado por la ruta con los tweets
    almacenados en memoria (el dict 'tweets')"""

    while True:

        ruta = input(INGRESE_RUTA_EXPORTAR)

        if ruta == ATRAS:
            break

        if not es_txt(ruta):
            print(DIRECCION_ERRONEA)
            continue

        partes_ruta = ruta.rsplit("/", 1)

        if len(partes_ruta) > 1:
            dir = partes_ruta[0]

            if not os.path.exists(dir) or not os.path.isdir(dir):
                print(DIRECCION_ERRONEA)
                continue

        tweets_exportados = 0

        with open(ruta, "w", encoding="utf-8") as archivo:
            for tweet in tweets.values():
                tweet = tweet.rstrip()
                archivo.write(f"{tweet}\n")
                tweets_exportados += 1

        print(f"OK {tweets_exportados}")
        break


# -----------------------------------------------------------------------------


def validar_argumentos(args):
    """
    Si se ingresan argumentos por consola los recibe por args, sino,
    recibe args = None. Si args = None o solo se recibe 1 argumento
    (i.e. args = ["nombre_archivo"]), devuelve LEN_DEFAULT_TOKENIZACION.

    Si efectivamente se reciben mas argumentos, verifica que sea solo un
    entero positivo. Si lo es, se devuelve como int (que en main() se
    almacena como len_tokenizacion). Si no, se devuelve None (y en main()
    se ejecuta sys.exit(1)).
    """

    if args is None or len(args) == 1:
        return LEN_DEFAULT_TOKENIZACION

    if len(args) != 2 or not args[1].isdigit():
        return None

    valor = int(args[1])

    if valor <= 0:
        return None

    return valor


# -----------------------------------------------------------------------------

# Esta parte del código se ejecuta al final, asegurando que se ejecute el programa
# mediante la terminal correctamente y permitiendo que se puedan realizar
# los tests de forma automática y aislada.

if __name__ == "__main__":

    main(sys.argv)
