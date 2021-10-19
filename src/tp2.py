import sys

from src.lector import Lector
from src.johnson import Johnson

class TP2Error(Exception):
    pass


class TP2:
    def __init__(self,args):
        self.recomendaciones = None
        if 1 != len(args):
            self.imprimirAyuda()

        try:
            self.procesar(args[0])
            self.imprimir()

        except Exception as ex:
            if isinstance(ex, FileNotFoundError):
                print("El archivo es inexistente o inaccesible.")
            elif isinstance(ex, TP2Error):
                print(str(ex))
                return
            else:
                print("Se produjo un error inesperado.\n")
            print("Error original:"+str(ex),file=sys.stderr)
            return

    def procesar(self,archivo):
            lector = Lector(archivo)
            if lector.grafo.cantidadArcos()<1:
                raise TP2Error("El achivo no contiene arcos (aristas): "+archivo+"\n")
            self.johnson = Johnson(lector.grafo)
            self.matriz = self.johnson.matriz
            self.grafo = lector.grafo
            self.ids = [0]
            self.alias = list(map(lambda id: lector.grafo.alias(id=id), self.ids))

    def imprimir(self):
        texto = "Ubicación recomendada" if 1==len(self.ids) else "Ubicaciones recomendadas"
        texto += ": " + ", ".join(self.alias)
        cabecera = "\t".join(self.grafo.alias())
        print(texto+"\n\t" + cabecera)
        for id in range(self.grafo.cantidadNodos()):
            nombreFila = self.grafo.alias(id=id)
            valores = map(lambda x: str(x), self.matriz[id])
            celdas = "\t".join(valores)
            print(nombreFila+":\t"+celdas)

    def imprimirAyuda(self):
        margen = "            "
        print("Por favor, ingrese el nombre del archivo a procesar como primer parámetro del script.")
        print("Por ejemplo:")
        print(margen+"python -m src.tp2 depositos.csv\n\n")
        print("El archivo debe contener una ruta por línea; con origen, destino y costo separados por coma.")
        print("Por ejemplo:")
        print(margen+"A,B,54\n"+margen+"A,D,-3,\n"+margen+"B,C,8\n")

if "__main__" == __name__:
    TP2(sys.argv[1:])
