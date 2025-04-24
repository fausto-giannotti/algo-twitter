# aca voy a hacer todo el desarollo

NUMERO_INVALIDO = "Numero de tweet invalido."
NO_ENCONTRADOS = "No se encontraron tweets."
INPUT_INVALIDO = "Input invalido."
FIN = "Finalizando..."
RESULTADOS_BUSQUEDA = "Resultados de la busqueda:"
TWEETS_ELIMINADOS = "Tweets eliminados:"
ATRAS = "**"


def main():
    user_input = input(
        "1. Crear Tweet \n2. Buscar Tweet \n3. Eliminar Tweet \n4. Salir\n"
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
        print("Seleccione una opción válida")

# -----------------------------------------------------------------------------


def crear_tweet():
    tweet_a_almacenar = input("Ingrese el tweet a almacenar:")
    return


def buscar_tweet():
    print("helo")


def eliminar_tweet():
    print("helo")


# -----------------------------------------------------------------------------

# Esta parte del código se ejecuta al final,
# asegurando que se ejecute el programa
# mediante la terminal correctamente y permitiendo que se puedan realizar
# los tests de forma automática y aislada.
if __name__ == "__main__":
    main()
