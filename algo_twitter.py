# aca voy a hacer todo el desarollo

NUMERO_INVALIDO = "Numero de tweet invalido."
NO_ENCONTRADOS = "No se encontraron tweets."
INPUT_INVALIDO = "Input invalido."
FIN = "Finalizando..."
RESULTADOS_BUSQUEDA = "Resultados de la busqueda:"
TWEETS_ELIMINADOS = "Tweets eliminados:"
ATRAS = "**"


def main():

    while True:

        # se ejecutará hasta que el usuario ingrese 4
        user_input = input(
            "1. Crear Tweet\n"
            "2. Buscar Tweet\n"
            "3. Eliminar Tweet\n"
            "4. Salir\n"
            ">>> "
        )

        if user_input == "1":
            crear_tweet()
        elif user_input == "2":
            buscar_tweet()
        elif user_input == "3":
            eliminar_tweet()
        elif user_input == "4":
            return print(FIN)
        else:
            return print(INPUT_INVALIDO)

# -----------------------------------------------------------------------------

# todos los tweets se almacenan en un dict
# cada tweet tiene un calve (id) y un valor (el tweet en si)
# --> son de la forma {id:tweet}


"""
Crear tweet: el usuario ingresa un tweet que se almacena con su respectivo
ID (que es unico e irrepetible)
Output esperado: OK id_tweet
Si tweet almacenado (i.e. normalizado) == vacío, entonces input invalido
"""


def crear_tweet():

    tweet_a_almacenar = input("Ingrese el tweet a almacenar:")

    if tweet_a_almacenar == ATRAS:
        return

    return


"""
Buscar tweet:
"""


def buscar_tweet():
    print("helo")


"""
Eliminar tweet:
"""


def eliminar_tweet():
    print("helo")


# -----------------------------------------------------------------------------

# Esta parte del código se ejecuta al final,
# asegurando que se ejecute el programa
# mediante la terminal correctamente y permitiendo que se puedan realizar
# los tests de forma automática y aislada.
if __name__ == "__main__":
    main()
