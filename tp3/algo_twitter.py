import sys

from logica import validar_argumentos
from interaccion_usuario import llamar_funciones
from manejo_db import inicializar_db


def main(args=None):

    len_tokenizacion = validar_argumentos(args)

    tweets = {}
    tweets_normalizados_tokenizados = {}

    id = inicializar_db(tweets, tweets_normalizados_tokenizados, len_tokenizacion)

    llamar_funciones(len_tokenizacion, tweets, tweets_normalizados_tokenizados, id)


# -----------------------------------------------------------------------------

# Esta parte del código se ejecuta al final, asegurando que se ejecute el programa
# mediante la terminal correctamente y permitiendo que se puedan realizar
# los tests de forma automática y aislada.

if __name__ == "__main__":

    main(sys.argv)
