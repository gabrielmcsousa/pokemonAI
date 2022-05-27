% Átomos
:- localization/2,
   visited/2,
   pokeballs/1,
   mapa/3,
   mapType/3,
   points/1,
   pokemon/2,
   orientation/1,
   recover/1,
   pokemonsCaptured/1,
   mapPoints/3,
   goWalk/1,
   log/1. 

orientation(0). % 0=baixo , 1 = direita, 2 = cima, 3 = esquerda
localization(19, 24).
visited(19, 24).
pokeballs(25). %quantidade total de pokebolas
score(0).
pokemonsCaptured(0).
recover(1).
log([]).

registerLog(X) :- retract(log(A)), assert(log(X | A)), !. %registro do log

addPoints(X) :-
  retract(points(Points)), %remove a informação points
  P is Points + X, %is força a somatória dos pontos, atualizando os pontos
  assert(points(P)). % add a informação points passando os pontos atualizados


addPokemonsRecovered(X) :-
   retract(pokemonsCaptured(Num)),
   R is Num + X,
   assert(pokemonsCaptured(R))

addPokeballs(X) :-
    retract(pokeballs(Pokeballs)),
    B is Pokeballs + X,
    assert(pokeballs(B)).

visit(X,Y) :- visited(X,Y), !.
visit(X,Y) :- assert(visited(X,Y)),!.

changeLocalization(X,Y) :-
 retract(localization(Line, Column)),
 L is Line + X,
 C is Column + Y,
 assert(localization(L,C)).

% Movimentação do agente

 turnRight :-
  orientation(Position),
  Turning is (Position + 3) mod 4,
  retract(orientation(Position)),
  assert(orientation(Turning)),
  addPoints(-1),
  registerLog('Virou para direita').

  turnLeft :-
   orientation(Position),
   Turning is(Position + 1) mod 4,
   retract(orientation(Position)),
   assert(orientation(Position)),
   addPoints(-1),
   registerLog('Virou para esquerda').

   moveForward :- orientation(0), changeLocalization(1,0), addPoints(-1), registerLog('Moveu para frente.'),!.
   moveForward :- orientation(1), changeLocalization(0,1), addPoints(-1), registerLog('Moveu para frente.'),!.
   moveForward :- orientation(2), changeLocalization(-1,0), addPoints(-1), registerLog('Moveu para frente.'),!.
   moveForward :- orientation(3), changeLocalization(0,-1), addPoints(-1), registerLog('Moveu para frente.'),!.

   turnUp :- orientation(0), turnRight, turnRight, !.
   turnUp :- orientation(1), turnLeft,!.
   turnUp :- orientation(2),!.
   turnUp :- orientation(3),turnLeft, turnLeft, !.

   moveUp :- turnUp, moveForward.
   
   turnDown :- orientation(0),!.
   turnDown :- orientation(1), turnRight,!.
   turnDown :- orientation(2), turnRight, turnRight,!.
   turnDown :- orientation(3), turnLeft,!.

   moveDown :- turnDown, moveForward.

%   0=baixo ,    1 = direita,    2 = cima,     3 = esquerda
   turnRight :- orientation(0), turnLeft,!.
   turnRight :- orientation(1), !.
   turnRight :- orientation(2), turnRight, !.
   turnRight :- orientation(3), turnRight, turnRight,!.

   moveRight :- turnRight, moveForward.

   turnLeft :- orientation(0), turnRight,!.
   turnLeft :- orientation(1), turnRight, turnRight, !.
   turnLeft :- orientation(2), turnLeft,!.
   turnLeft :- orientation(3),!.

   moverLeft :- turnLeft, moveForward.

   recoverPokemons :-
   localization(X,Y),
   mapType(X,Y, centerPokemon),
   retract(recover(Recover)),
   assert(recover(1)),
   addPoints(-100),
   registerLog('Recuperou os Pokemons no Centro Pokémon'),!.

   battle :- hurt(1), addPoints(-1000),!.
   battle :- hurt(0), addPoints(150), retract(hurt(1)), assert(hurt(0)),!.

   BattleTrainer :-
   localization(X,Y),
   mapType(X,Y, trainer),
   battle,
   retract(mapType(X,Y,trainer)),
   assert(mapType(X,Y,empty)),
   registerLog('Enfrentou um treinador!').

   NeedcatchPokeballs :-
   pokeballs(Balls),
   pokemonsCaptured(Num),
   SumBalls is Balls + Num,
   SumBalls < 150.
   
   catchPokeballs :-
   localization(X,Y),
   NeedcatchPokeballs,
   retract(mapType(X,Y,store)),
   assert(mapType(X,Y,empty)),
   addPokeballs(25),
   addPoints(-10),
   registerLog('Pegou 25 Pokebolas na Loja!').

   WalkType(Pokemon) :-
   canWalk('Water'),
   canWalk('Mountain'),
   canWalk('Volcano'),
   canWalk('Cave'),!
   
   WalkType(Pokemon) :-
   pokemon(Pokemon,Types),
   type('Water',Types),
   canWalk('Água'). 

   WalkType(Pokemon) :-
   pokemon(Pokemon, Types),
   type('Water',Types),
   not(canWalk('Water')),
   assert(canWalk('Water')).

   WalkType(Pokemon) :-
   pokemon(Pokemon,Types),
   type('Fire',Types),
   canWalk('Volcano'). 

   WalkType(Pokemon) :-
   pokemon(Pokemon, Types),
   type('Fire',Types),
   not(canWalk('Volcano')),
   assert(canWalk('Volcano')).

   WalkType(Pokemon) :-
   pokemon(Pokemon,Types),
   type('Flying',Types),
   canWalk('Mountain'). 

   WalkType(Pokemon) :-
   pokemon(Pokemon, Types),
   type('Flying',Types),
   not(canWalk('Mountain')),
   assert(canWalk('Mountain')).

   
   WalkType(Pokemon) :-
   pokemon(Pokemon,Types),
   type('Electric',Types),
   canWalk('Cave'). 

   WalkType(Pokemon) :-
   pokemon(Pokemon, Types),
   type('Electric',Types),
   not(canWalk('Cave')),
   assert(canWalk('Cave')).

   
   