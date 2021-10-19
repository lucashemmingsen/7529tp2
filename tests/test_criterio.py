from math import inf
import unittest

from src.criterio import Criterio

class TestCriterio(unittest.TestCase):
    def test_vacio(self):
        self.assertRaises(Exception,Criterio,None)
        self.assertRaises(Exception,Criterio,[])
        self.assertRaises(Exception,Criterio,[[]])

    def test_1x1(self):
        criterio = Criterio([[inf]])
        self.assertEqual(criterio.mejores, [0])

    def test_analizar_inf(self):
        self.assertEqual(Criterio.analizar([inf]), (1,inf))

    def test_analizar_inf0(self):
        self.assertEqual(Criterio.analizar([inf,0]), (1,0))

    def test_analizar_menos10inf(self):
        self.assertEqual(Criterio.analizar([-10,inf]), (1,-10))

    def test_analizar_inf20inf(self):
        self.assertEqual(Criterio.analizar([inf,20,inf]), (2,20))

    def test_analizar_inf20inf(self):
        self.assertEqual(Criterio.analizar([-6,inf,13,inf]), (2,3.5))

    def test_analisis(self):
        self.assertEqual(Criterio([ [inf,inf], [inf,inf] ]).analisis, [(2,inf),(2,inf)])
        self.assertEqual(Criterio([ [inf,inf], [inf,  9] ]).analisis, [(2,inf),(1,  9)])
        self.assertEqual(Criterio([ [  9,inf], [inf,inf] ]).analisis, [(1,  9),(2,inf)])
        self.assertEqual(Criterio([ [ -6,inf], [inf,  5] ]).analisis, [(1, -6),(1,  5)])
        self.assertEqual(Criterio([ [  1,  5], [  2,  2] ]).analisis, [(0,  3),(0,  2)])
        variosDe3 = [ [6,inf,2], [inf,inf,0], [3,5,7], [inf,inf,inf] ]
        self.assertEqual(Criterio(variosDe3).analisis, [(1,4),(2,0),(0,5),(3,inf)])

