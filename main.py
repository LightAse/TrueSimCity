

class Celda:
    x = -1
    y = -1
    celdaNor = None
    celdaSur = None
    celdaEst = None
    celdaOes = None

    def __init__(self, y, x):
        self.x = x
        self.y = y


class Terreno(Celda):
    icono = ""
    costeConstruir = 0
    valor = 0

    def __init__(self, x, y):
        super().__init__(x, y)

    def tostring(self):
        return "terreno"


class Vacio(Terreno):
    icono = " "

    def __init__(self, x, y):
        super().__init__(x, y)

    def tostring(self):
        return "vacio"


class Calle(Terreno):
    icono = "+"
    costeConstruir = 5

    def __init__(self, x, y):
        super().__init__(x, y)

    def tostring(self):
        return "calle"


class Residencial(Terreno):
    icono = None
    valor = None
    costeConstruir = None

    def __init__(self, x, y):
        super().__init__(x, y)

    def recaudar(self):
        return self.valor


class Baja(Residencial):
    icono = "1"
    valor = 5
    costeConstruir = 15

    def __init__(self, x, y):
        super().__init__(x, y)

    def tostring(self):
        return "resl"


class Media(Residencial):
    icono = "2"
    valor = 10
    costeConstruir = 30

    def __init__(self, x, y):
        super().__init__(x, y)

    def tostring(self):
        return "resm"


class Alta(Residencial):
    icono = "3"
    valor = 20
    costeConstruir = 60

    def __init__(self, x, y):
        super().__init__(x, y)

    def tostring(self):
        return "resh"


class Map:
    rows = 5
    column = 5
    map = ''
    celdaMap = [Vacio(0, 0)]

    def insertarcelda(self, nue, old):

        for i in range(len(self.celdaMap)):
            if self.celdaMap[i] == old:
                self.celdaMap.pop(i)
                self.celdaMap.append(nue)
                self.actualizarmapa(nue)
                break

    def loadMap(self):
        pass

    def createMap(self):
        self.celdaMap.clear()
        for i in range(self.rows):
            for j in range(self.column):
                self.map += "| "
                self.celdaMap.append(Vacio(j, i))
            self.map += "|\n"

    def encontrarcelda(self, a, b):
        for i in self.celdaMap:
            if i.x == int(a) and i.y == int(b):
                return i

    def actualizarmapa(self, nue):
        val_x = 0
        val_y = 0
        ltemp = []
        for i in range(len(self.map)):
            if self.map[i] == "|":
                val_x += 1

            if val_x == nue.x and val_y == nue.y:
                ltemp = list(self.map)
                ltemp[i + 1] = nue.icono
                break

            if val_x > 6:
                val_y += 1
                val_x = 0
        self.map = "".join(ltemp)
        print(self.map)

    def __init__(self):
        pass


class Partida:
    nombrePartida = "noone"
    fechaCreada = "00/00/0000"
    diasPass = 0
    porcentajeImpositivo = 0
    dinero = 100
    map = Map()

    def __init__(self, cargar, name=None, mapx=None, mapy=None):
        if (cargar):
            pass
        else:
            self.crearpartida(name, mapx, mapy)

    def crearpartida(self, name, mapx=None, mapy=None):
        self.nombrePartida = name

        if mapx is not None and mapy is not None:
            self.map.rows = mapx
            self.map.column = mapy
        elif mapx is not None:
            self.map.rows = mapx
        elif mapy is not None:
            self.map.column = mapy

        self.map.createMap()

    def mostrarjuego(self):
        print(self.map.map)
        print("\nDinero: " + str(self.dinero))
        print("Dias: " + str(self.diasPass))
        print("Tax: " + str(self.porcentajeImpositivo))

    def checksyntaxis(self):
        teclado = ""
        while teclado != "/exit":
            teclado = input()
            if teclado == "/exit":
                return teclado
            elif teclado == "/help":
                self.mostrarayuda()
            elif teclado == "/map":
                self.mostrarjuego()
            elif teclado.find("/build") > -1:
                self.construir(teclado)
            elif teclado.find("/destroy") > -1:
                self.destruir(teclado)
            elif teclado == "/pass":
                self.pasar()
            elif teclado.find("/upgrade") > -1:
                self.upgrade(teclado)
            elif teclado.find("/tax") > -1:
                self.actualizatax(teclado)
            else:
                print("\n command not found. Try again or try /help for more information about commands")

    def actualizatax(self, teclado):
        alt = self.encontrarnumero0a9(teclado, teclado.find("tax")+2)
        if alt != -1:
            t1 = teclado.find(alt)+1
            alt2 = self.encontrarnumero0a9(teclado, t1)
            if alt2 != -1:
                nue = alt + alt2
                t2 = t1+1
                alt3 = self.encontrarnumero0a9(teclado, t2)
                if alt3 != -1:
                    nue += alt3
                    if int(nue) == 100:
                        self.porcentajeImpositivo = 1.00
                        print("added tax")
                    else:
                        print("tax is too high")
                else:
                    self.porcentajeImpositivo = int(nue) / 100
                    print("added tax")
            else:
                print(alt)
                self.porcentajeImpositivo = int(alt) / 100
                print("added tax")

    def upgrade(self, teclado):
        alt = self.encontrarnumero(teclado, teclado.find("upgrade") + 6)
        alt1 = 0
        if alt != -1:
            temp = teclado.find(alt) + 1
            alt1 = self.encontrarnumero(teclado, temp)
            if alt1 != -1:
                tipe = self.map.encontrarcelda(alt, alt1)
                if tipe.tostring() != "vacio" or "calle":
                    if tipe.tostring() == "resl":
                        nueva = Media(int(alt), int(alt1))
                    elif tipe.tostring() == "resm":
                        nueva = Alta(int(alt), int(alt1))
                    else:
                        print("The building cannot be upgrade")
                        return

                    if self.dinero - nueva.costeConstruir >= 0:
                        self.dinero -= nueva.costeConstruir
                        self.map.insertarcelda(nueva, tipe)
                        print("The building has been upgraded")
                    else:
                        print("not enough money.")
                else:
                    print("the place cannot be upgrade")

    def pasar(self):
        cantrec = 0
        for i in self.map.celdaMap:
            if i.tostring() == "resl" or "resm" or "resh":
                cantrec += i.valor + (i.valor * self.porcentajeImpositivo)
        self.dinero += cantrec
        self.diasPass += 1
        print("A day has pass and you recoleted $" + str(cantrec))

    def destruir(self, teclado):
        alt = self.encontrarnumero(teclado, teclado.find("destroy") + 6)
        alt1 = 0
        if alt != -1:
            temp = teclado.find(alt) + 1
            alt1 = self.encontrarnumero(teclado, temp)
            if alt1 != -1:
                tipe = self.map.encontrarcelda(alt, alt1)
                if tipe.tostring() != "vacio":
                    nueva = Vacio(int(alt), int(alt1))
                    if self.dinero - 10 >= 0:
                        self.dinero -= 10
                        self.map.insertarcelda(nueva, tipe)
                        print("The building has been destroyed")
                    else:
                        print("not enough money. Destroy price is 10")
                else:
                    print("the place is already empty")

    def construir(self, teclado):

        if teclado.find("resl") > -1:
            temp = teclado.find("resl") + 3
            tipo = 0
        elif teclado.find("resm") > -1:
            temp = teclado.find("resm") + 3
            tipo = 1
        elif teclado.find("resh") > -1:
            temp = teclado.find("resh") + 3
            tipo = 2
        elif teclado.find("str") > -1:
            temp = teclado.find("str") + 3
            tipo = 3
        else:
            print("command incorrect")
            return

        alt = self.encontrarnumero(teclado, temp)
        alt1 = 0
        if alt != -1:
            temp = teclado.find(alt) + 1
            alt1 = self.encontrarnumero(teclado, temp)
            if alt1 != -1:
                tipe = self.map.encontrarcelda(alt, alt1)
                if tipe.tostring() == "vacio":
                    nueva = self.crearcelda(tipo, tipe)
                    if self.dinero - nueva.costeConstruir >= 0:
                        self.dinero -= nueva.costeConstruir
                        self.map.insertarcelda(nueva, tipe)
                        print("the building has been built")
                    else:
                        print("not enough money")
                else:
                    print("the place is being occupied")

    def crearcelda(self, tipo, tipe):

        if tipo == 0:
            return Baja(tipe.x, tipe.y)
        elif tipo == 1:
            return Media(tipe.x, tipe.y)
        elif tipo == 2:
            return Alta(tipe.x, tipe.y)
        elif tipo == 3:
            return Calle(tipe.x, tipe.y)
        else:
            print("error in crearcelda()")

    def encontrarnumero(self, teclado, temp):
        found = False
        while not found:
            if temp >= len(teclado):
                return -1
            if chr(48) <= teclado[temp] <= chr(52):
                return teclado[temp]
            temp += 1


    def encontrarnumero0a9(self, teclado, temp):
        found = False
        while not found:
            if temp >= len(teclado):
                return -1
            if chr(48) <= teclado[temp] <= chr(57):
                return teclado[temp]
            temp += 1


    def mostrarayuda(self):
        print(
            "\n --Help--\nFunction /build [Type] [Location X] [Location Y] => build a type of building in  location X and location Y\n"
            "Function /map => writes the map\nFunction /destroy [Location X] [Location Y] => destroys a building in a designated location\n"
            "Function /pass => Pass from one day to another\nFunction /exit => exits the game without saving\nFunction /save => saves the actual game\n"
            "Function /upgrade [Location X] [Location Y] => upgrades a building to the next level\nFunction /tax [Range from 0 to 100] => allows to modify tax from 0% to 100%\n"
            "--Build Types--\n"
            "resl => low residence\n"
            "resm => medium residence\n"
            "resh => high residence\n"
            "str => street")


def main():
    game = Partida(False)
    game.mostrarjuego()
    game.checksyntaxis()


main()
