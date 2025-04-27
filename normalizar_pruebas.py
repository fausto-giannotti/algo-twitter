"""tweet = " HOLAAA soy una string @))#()@()#(@)#)(@()) con acentos  áé í ó ú"
lista_caracteres = list(tweet.lower())

acentos_y_enie = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n"}

for posicion in range(len(lista_caracteres)):
    if not (lista_caracteres[posicion].isalnum() or lista_caracteres[posicion] == " "):
        lista_caracteres[posicion] = ""

    lista_caracteres[posicion] = acentos_y_enie.get(
        lista_caracteres[posicion], lista_caracteres[posicion]
    )

    if (
        posicion > 0
        and lista_caracteres[posicion] == " "
        and lista_caracteres[posicion - 1] == " "
    ):
        lista_caracteres[posicion] = ""

    if lista_caracteres[0] == " ":
        lista_caracteres[0] = ""

    if lista_caracteres[-1] == " ":
        lista_caracteres[-1] = ""

tweet_normalizado = "".join(lista_caracteres)

# print(tweet_normalizado)"""


def normalizar(tweet):

    acentos_y_enie = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n"}

    lista_caracteres = list(tweet.lower())

    for posicion in range(len(lista_caracteres)):
        if not (
            lista_caracteres[posicion].isalnum() or lista_caracteres[posicion] == " "
        ):
            lista_caracteres[posicion] = ""

        lista_caracteres[posicion] = acentos_y_enie.get(
            lista_caracteres[posicion], lista_caracteres[posicion]
        )

        if (
            posicion > 0
            and lista_caracteres[posicion] == " "
            and lista_caracteres[posicion - 1] == " "
        ):
            lista_caracteres[posicion] = ""

        if lista_caracteres[0] == " ":
            lista_caracteres[0] = ""

        if lista_caracteres[-1] == " ":
            lista_caracteres[-1] = ""

    tweet_normalizado = "".join(lista_caracteres)

    return tweet_normalizado


print(normalizar("!!!"))
print(normalizar(" asdasdaas!!!sadasdasd"))
print(normalizar(" HOLAAA soy una string @))#()@()#(@)#)(@()) con acentos  áé í ó ú"))
print(normalizar("quiero NORMALIZAR este tweet"))
