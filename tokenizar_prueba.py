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
                # el rango sería range(3, 4+1) = [3, 4, 5]
                #     inicio = 0, fin = 3 => palabra[0:3] = "hol"
                #     inicio = 0, fin = 4 => palabra[0:4] = "hola"
                # desp inicio = 1:
                #     inicio = 1, fin = 4 => palabra[1:4] = "ola"
                #     inicio = 1, fin = 5 => palabra[1:5] = "ola"
                # Y así hasta con con todas las palabras

                for fin in range(inicio + 3, len(palabra) + 1):
                    segmento = palabra[inicio:fin]

                    # para cada caracter, ir desde su pos a pos+3, +4, +n hasta
                    # llegar al final de la palabra y almecenar cada
                    # combinacion

                    # no volver a almacenar segmentos ya almacenados
                    if segmento not in tweet_tokenizado:
                        tweet_tokenizado.append(segmento)

    return tweet_tokenizado


# caprese, cc, atun /roquefort pollo, jyq, humita, picante

print(tokenizar("hola soy de unit"))
print(tokenizar("autos de matias"))
