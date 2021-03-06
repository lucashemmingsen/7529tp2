import sys

from src.criterio import Criterio
from src.johnson import Johnson
from src.lector import Lector

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
                print("El archivo es inexistente o inaccesible: " + str(ex))
            elif isinstance(ex, TP2Error):
                print(str(ex))
            else:
                print("Se produjo un error inesperado: \n"+str(ex))
                raise ex
            return

    def procesar(self,archivo):
            lector = Lector(archivo)
            if lector.grafo.cantidadArcos()<1:
                raise TP2Error("El achivo no contiene arcos (aristas): "+archivo+"\n")
            self.johnson = Johnson(lector.grafo)
            if False is self.johnson.matriz:
                raise TP2Error("Se detectó un bucle negativo")
            self.matriz = self.johnson.matriz
            self.grafo = lector.grafo
            # Calcular recomendación
            self.criterio = Criterio(self.matriz)

    def imprimir(self):
        texto = self.textoRecomendacion()
        cabecera = "\t".join(self.grafo.alias())
        print(texto+"\n\t" + cabecera)
        for id in range(self.grafo.cantidadNodos()):
            nombreFila = self.grafo.alias(id=id)
            valores = map(lambda x: str(x), self.matriz[id])
            celdas = "\t".join(valores)
            print(nombreFila+":\t"+celdas)

    def textoMejores(self,prefijo,mejores):
        valores = map(self.grafo.alias, mejores)
        return prefijo + ( ", ".join(valores))

    def textoRecomendacion(self):
        singular = (None is not self.criterio.mejores) and (1 == len(self.criterio.mejores))
        texto = ("Ubicación recomendada" if singular else "Ubicaciones recomendadas") + ":"
        if (None is self.criterio.mejores):
            texto += self.textoMejores("\n * Por costo promedio:\t", self.criterio.mejoresCosto)
            texto += self.textoMejores("\n * Por nº de ciudades:\t", self.criterio.mejoresLimite)
        else:
            textosMejores = list(map(lambda id: self.grafo.alias(id=id), self.criterio.mejores))
            texto += "\t" + ( ", ".join(textosMejores) )
        texto +="\n"
        return texto

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
