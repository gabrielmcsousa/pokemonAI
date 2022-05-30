from pyswip import Prolog
from functools import reduce
from game import Game
from IPython.display import clear_output


class BaseQuery:
    def __init__(self, base_name="poke.pl"):
        self.prolog = Prolog()
        self.prolog.retractall('visited(__, _)')
        self.prolog.retractall('log(_)')
        self.prolog.consult(base_name)
        self.prolog.retractall('pokemon(_, _)')
        self.prolog.retractall('mapTypes(_,_,_)')
        self.prolog.retractall('mapPoints(_, _, _)')
        self.prolog.retractall('mapa(_, _, _)')
        self.prolog.retractall('types(_, _)')
        self.prolog.retractall('canWalk(_)')

    def insert_fact(self, fact):
        list(self.prolog.query(f"not({fact}), assert({fact})"))

    def print_list(self, list):
        for item in list:
            for key in item:
                print(key, "=", item[key])

    def query(self, query, print=False):
        result = list(self.prolog.query(query))
        if print:
            self.print_list(result)
            return result

    def insert_map_facts(self):
        for i in range(42):
            for j in range(42):
                if gameMap.matrix[i][j] == 'W':
                    self.insert_fact(f"mapa({i},{j}, 'WATER')")
                elif gameMap.matrix[i][j] == 'G':
                    self.insert_fact(f"mapa({i},{j}, 'GRAM')")
                elif gameMap.matrix[i][j] == 'C':
                    self.insert_fact(f"mapa({i},{j}, 'CAVE')")
                elif gameMap.matrix[i][j] == 'V':
                    self.insert_fact(f"mapa({i},{j},'VOLCANO')")
                elif gameMap.matrix[i][j] == 'M':
                    self.insert_fact(f"mapa({i},{j},'MOUNTAIN'")

    def insert_member_fact(self, i, j):
        if(i < 42 and j < 42 and len(self.query(f"mapType({i}, {j}, _)")) == 0):
            typeFloor = (i, j)
            member = gameMap.dict.get(typeFloor, "EMPTY")

            if member == 'P':
                base.insert_fact(f"mapType({i}, {j}, pokeCenter)")
            elif member == 'S':
                base.insert_fact(f"mapType({i}, {j}, store)")
            elif member == 'C':
                base.insert_fact(f"mapType({i}, {j}, coach)")
            elif isinstance(member, int):
                name = gameMap.pokemons[member]["name"]
                types = map(
                    lambda pokeType: f"'{pokeType}", gameMap.pokemons[member]["type"])
                types = f"[{', '.join(types)}]"
                base.insert_fact(
                    f"mapType({i}, {j}, pokemon('{name}', {types}))")
            else:
                base.insert_fact(f"mapType({i}, {j}, empty)")

            def insert_entity_fact_title(self):
                locale = self.query("localization(Line,Column)")[0]
                self.insert_entity_fact(locale["Line"] + 1, locale["Column"])
                self.insert_entity_fact(locale["Line"] + -1, locale["Column"])
                self.insert_entity_fact(locale["Line"], locale["Column"] + 1)
                self.insert_entity_fact(locale["Line"], locale["Column"] - 1)

            def locale(self):
                locale = self.query("localization(Line, Column)")[0]
                gameMap.print((locale["Line"], locale["Column"]))

            def localeText(self):
                self.query("localization(Line, Column)", True)

            def pokemons(self):
                pokemons = self.query("pokemon(Pokemon, Types)")
                pokemon = ""
                count = 0
                words_break = 0
                for pokemon in pokemons:
                    name = pokemon["Pokemon"]
                    types = ', '.join(
                        list(map(lambda pokeType: str(poke_type), pokemon["Types"])))
                    count += 1
                    words_break += len(pokemon["Types"]) + 1

                if(count == 150):
                    pokemon += f"({name}, Types:[{types}])."
                else:
                    pokemon += f"({name}, Types:[{types}])."
                if(words_break / 8 > 1):
                    words_break = 0
                    pokemon += "\n"

            print(pokemon)

            def score(self):
                self.query("pontos(Score)", True)

            def scoreCalc(self):
                locale = base.query("localization(Line, Column)")[0]
                line = locale["Line"]
                column = locale["Column"]

                self.query(f"mapPoints({line - 1}, {column}, Up )", True)
                self.query(f"mapPoints({line + 1}, {column}, Back )", True)
                self.query(f"mapPoints({line}, {column + 1}, Right)", True)
                self.query(f"mapPoints({line}, {column - 1}),Left", True)

            def pokeballs(self):
                self.query("pokeballs(Balls)", True)

            def pokemonsCount(self):
                return self.query("pokemonsRecovered(PokeCount)", True)[0]["PokeCount"]

            def canWalk(self):
                self.query("canWalk(canWalkTrue", True)

            def log(self):
                action = list(map(lambda action: str(action),
                              base.query("log(Action)")[0]["Actions"]))
                for i in range(len(action)):
                    print(f"{i + 1}a - {action[len(action) - i - 1]} ")

            def run(self, to_print=True):
                i = 0
                while self.pokeCount() < 150:
                    self.insert_entity_fact_title()
                    self.localeText()
                    self.score()
                    self.scoreCalc()
                    self.pokeballs()
                    self.pokemonsCount()
                    self.canWalk()

                    if to_print:
                        self.locale()
                    elif to_print == False and i % 20:
                        clear_output(True)
                    i = i + 1
                    self.query("Action")
                    self.score()
                    print("Congrats!!!")
                    print('GAME OVER')

    gameMap = Game.map
    base.insert_map_facts()
    base.run(True)
    base = BaseQuery()
