from pyswip import Prolog
from functools import reduce
from game import Game
from IPython.display import clear_output
from center import PokeCenter
from mart import PokeMart
from trainer import Trainer
from mon import Pokemon
from player import Player, PlayerOri
import pygame
import config


class BaseQuery:
    def __init__(self, mapType, mapE, base_name="poke.pl"):
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
        self.matrix = mapType
        self.mapElements = mapE

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
                if self.matrix[i][j] == 'W':
                    self.insert_fact(f"mapa({i},{j}, 'WATER')")
                elif self.matrix[i][j] == 'G':
                    self.insert_fact(f"mapa({i},{j}, 'GRAM')")
                elif self.matrix[i][j] == 'C':
                    self.insert_fact(f"mapa({i},{j}, 'CAVE')")
                elif self.matrix[i][j] == 'V':
                    self.insert_fact(f"mapa({i},{j},'VOLCANO')")
                elif self.matrix[i][j] == 'M':
                    self.insert_fact(f"mapa({i},{j},'MOUNTAIN')")

    def insert_member_fact(self, i, j):
        if(i < 42 and j < 42 and len(self.query(f"mapType({i}, {j}, _)")) == 0):
            typeFloor = (i, j)
            member = self.mapElements[i][j]

            if type(member) is PokeCenter:
                self.insert_fact(f"mapType({i}, {j}, pokeCenter)")
            elif type(member) is PokeMart:
                self.insert_fact(f"mapType({i}, {j}, store)")
            elif type(member) is Trainer:
                self.insert_fact(f"mapType({i}, {j}, coach)")
            elif type(member) is Pokemon:
                name = member.name
                types = member.type
                types = f"[{', '.join(types)}]"
                self.insert_fact(
                    f"mapType({i}, {j}, pokemon('{name}', {types}))")
            else:
                self.insert_fact(f"mapType({i}, {j}, empty)")

    def insert_entity_fact_title(self):
        print("salda", self.query("localization(Line, Column)"))
        locale = self.query("localization(Line, Column)")[0]
        self.insert_member_fact(locale["Line"] + 1, locale["Column"])
        self.insert_member_fact(locale["Line"] + -1, locale["Column"])
        self.insert_member_fact(locale["Line"], locale["Column"] + 1)
        self.insert_member_fact(locale["Line"], locale["Column"] - 1)

    def locale(self):
        locale = self.query("localization(Line, Column)")[0]
   #     gameMap.print((locale["Line"], locale["Column"]))

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
                list(map(lambda pokeType: str(pokeType), pokemon["Types"])))
            count += 1
            words_break += len(pokemon["Types"]) + 1

        if(count == 150):
            pokemon += f"({name}, Types:[{types}])."
        else:
            pokemon += f"({name}, Types:[{types}]),"
        if(words_break / 8 > 1):
            words_break = 0
            pokemon += "\n"

        print(pokemon)

    def score(self):
        self.query("points(Score)", True)

    def scoreCalc(self):
        locale = self.query("localization(Line, Column)")[0]
        line = locale["Line"]
        column = locale["Column"]

        self.query(f"mapPoints({line - 1}, {column}, Up )", True)
        self.query(f"mapPoints({line + 1}, {column}, Back )", True)
        self.query(f"mapPoints({line}, {column + 1}, Right)", True)
        self.query(f"mapPoints({line}, {column - 1},Left)", True)

    def pokeballs(self):
        self.query("pokeballs(Balls)", True)

    def pokeCount(self):
        return self.query("  pokemonsCaptured(PokeCount)", True)[0]["PokeCount"]

    def canWalk(self):
        self.query("canWalk(canWalkTrue)", True)

    def log(self):
        action = list(map(lambda action: str(action),
                          self.query("log(action)")[0]["action"]))
        for i in range(len(action)):
            print(f"{i + 1}a - {action[len(action) - i - 1]} ")

    def run(self,  game, to_print=True):
        i = 0
        # while self.pokeCount() < 150:
        pygame.init()

        pygame.display.set_caption("PrologMon")

        clock = pygame.time.Clock()
        for j in range(10000):
            self.insert_entity_fact_title()
            self.localeText()
            self.score()
            self.scoreCalc()
            self.pokeballs()
            self.pokeCount()
            self.canWalk()
            clock.tick(50)
            game.update()
            pygame.display.flip()
            if to_print:
                self.locale()
            elif to_print == False and i % 20:
                clear_output(True)
            i = i + 1
            self.query("action")
            self.score()
            print("Congrats Master Pokemon!!!")
            print('GAME OVER')
