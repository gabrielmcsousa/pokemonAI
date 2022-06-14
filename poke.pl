%Regras
:- dynamic localization/2,
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
   canWalk/1,
   log/1. 

%Fatos
orientation(0). % 0=baixo , 1 = direita, 2 = cima, 3 = esquerda
localization(19,24).
visited(19,24).
pokeballs(25). %quantidade total de pokebolas
points(0).
pokemonsCaptured(0).
recover(1).
log([]).

%registro do log utilizando retract e assert para atualização do registro
registerLog(X) :- retract(log(A)), assert(log([X | A])), !. %registro do log

%Regra para adicionar os custos das ações
addPoints(X) :-
  retract(points(Points)), %remove a informação points
  P is Points + X, %is força a somatória dos pontos, atualizando os pontos
  assert(points(P)). % add a informação points passando os pontos atualizados

%Regra para atualizar a quantidade de pokemons recuperados
addPokemonsRecovered(X) :-
   retract(pokemonsCaptured(Num)),
   R is Num + X,
   assert(pokemonsCaptured(R)).

%Regra para atualizar a quantidade de pokebolas do agente
addPokeballs(X) :-
    retract(pokeballs(Pokeballs)),
    B is Pokeballs + X,
    assert(pokeballs(B)).

%Regra para atualizar os locais visitados pelo agente
visit(X,Y) :- visited(X,Y), !.
visit(X,Y) :- assert(visited(X,Y)),!.

%Regra para atualizar a localização do agente
changeLocalization(X,Y) :-
 retract(localization(Line, Column)),
 L is Line + X,
 C is Column + Y,
 assert(localization(L,C)),
 visit(L, C).

% Movimentação do agente
 %regra para virar o agente para a direita 
 turnRight :-
  orientation(Position),
  Turning is (Position + 3) mod 4,
  retract(orientation(Position)),
  assert(orientation(Turning)),
  addPoints(-1),
  registerLog('Virou para direita').

  %regra para virar o agente para a esquerda
  turnLeft :-
   orientation(Position),
   Turning is(Position + 1) mod 4,
   retract(orientation(Position)),
   assert(orientation(Turning)),
   addPoints(-1),
   registerLog('Virou para esquerda').
   
   %regra para atualizar o
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
   
   %regra para recuperar os pokemons
   recoverPokemons :-
   localization(X,Y),
   mapType(X,Y, pokeCenter),
   retract(recover(Recover)),
   assert(recover(0)),
   addPoints(-100),
   registerLog('Recuperou os Pokemons no Centro Pokémon'),!.
   
   %regra para mudança do estado do pokemon após a batalha
   battle :- recover(1), addPoints(-1000),!.
   battle :- recover(0), addPoints(150), retract(recover(1)), assert(recover(0)),!.
   
   %regra para remoção do treinador pokemon do prolog 
   battleTrainer :-
   localization(X,Y),
   mapType(X,Y, trainer),
   battle,
   retract(mapType(X,Y,trainer)),
   assert(mapType(X,Y,empty)),
   registerLog('Enfrentou um treinador!').
    
   %regra para se identificar a necessidade de se pegar mais pokebolas  
   needCatchPokeballs :-
   pokeballs(Balls),
   pokemonsCaptured(Num),
   SumBalls is Balls + Num,
   SumBalls < 150.
    
   %regra para pegar mais 25 pokebolas
   catchPokeballs :-
   localization(X,Y),
   needCatchPokeballs,
   retract(mapType(X,Y,store)),
   assert(mapType(X,Y,empty)),
   addPokeballs(25),
   addPoints(-10),
   registerLog('Pegou 25 Pokebolas na Loja!').
    
   %Regras relacionadas ao tipo de terreno

   %Regra relacionada aos tipos de terreno existentes que o agente pode percorrer 
   walkType(Pokemon) :-
   canWalk('Water'),
   canWalk('Mountain'),
   canWalk('Volcano'),
   canWalk('Cave'),!.
   
   %regras para atrelar o tipo do pokemon ao tipo de terreno
   walkType(Pokemon) :-
   pokemon(Pokemon,Types),
   type('Water',Types),
   canWalk('Water'). 

   walkType(Pokemon) :-
   pokemon(Pokemon, Types),
   type('Water',Types),
   not(canWalk('Water')),
   assert(canWalk('Water')).

   walkType(Pokemon) :-
   pokemon(Pokemon,Types),
   type('Fire',Types),
   canWalk('Volcano'). 

   walkType(Pokemon) :-
   pokemon(Pokemon, Types),
   type('Fire',Types),
   not(canWalk('Volcano')),
   assert(canWalk('Volcano')).

   walkType(Pokemon) :-
   pokemon(Pokemon,Types),
   type('Flying',Types),
   canWalk('Mountain'). 

   walkType(Pokemon) :-
   pokemon(Pokemon, Types),
   type('Flying',Types),
   not(canWalk('Mountain')),
   assert(canWalk('Mountain')).

   
   walkType(Pokemon) :-
   pokemon(Pokemon,Types),
   type('Electric',Types),
   canWalk('Cave'). 

   walkType(Pokemon) :-
   pokemon(Pokemon, Types),
   type('Electric',Types),
   not(canWalk('Cave')),
   assert(canWalk('Cave')),!.
   
   %Regra para atualizar o tipo de terreno 
   walkType(Pokemon) :- !.

   %Regra para capturar os pokemons 
   catch :-
   localization(X,Y),
   string_concat('Pokemon in ',X,Log),
   string_concat(Log,X,Logg),
   registerLog(Logg),
   pokeballs(Balls),
   Balls>0,
   retract(mapType(X,Y,pokemon(Pokemon,Types))),
   assert(mapType(X,Y,empty)),
   assert(pokemon(Pokemon,Types)),
   walkType(Pokemon),
   addPokeballs(-1),
   addPokemonsRecovered(1),
   addPoints(-5),
   string_concat('Catched ', Pokemon,Log),
   registerLog(Log).
  
   calculateDistance(X1, Y1, X2, Y2, Distance) :-
   DX is abs(X1 - X2),
   DY is abs(Y1 - Y2),
   Distance is DX + DY.
   
   %Regra para locais não visitados 
   unknown(L,C) :-
   mapa(X,Y, _),
   not(visited(X,Y)),
   L is X,
   C is Y,!.

   canMove(X, Y) :- mapa(X, Y, 'Gram'),!.
   canMove(X, Y) :- mapa(X, Y, T), canWalk(T),!.
    
   verifyBlock(X, Y) :- retract(mapPoints(X,Y, _)).

   verifyBlock(X, Y) :- not(canMove(X,Y)), assert(mapPoints(X, Y, -1)),!.

   frontBlock(X, Y) :-
   orientation(0),
   localization(Line, Column),
   LPO is Line + 1,
   X =:= LPO,
   Y =:= Column,!.

   frontBlock(X, Y) :-
   orientation(1),
   localization(Line, Column),
   CPO is Column + 1,
   X =:= Line,
   Y =:= CPO,!.

   frontBlock(X, Y) :-
   orientation(2),
   localization(Line, Column),
   LMO is Line - 1,
   X =:= Column,!.

   frontBlock(X, Y) :-
   orientation(3),
   localization(Line, Column),
   CMO is Column - 1,
   X =:= Line,
   Y =:= CMO,!.

   sideBlock(X, Y) :-
   (orientation(0); orientation(2)),
   localization(Line, Column),
   CMO is Column + 1,
   CMO is Column - 1,
   X =:= Line,
   (Y =:= CPO; Y=:= CMO),!.

   sideBlock(X, Y) :-
   (orientation(1), orientation(3)),
   localization(Line, Column),
   LPO is Line + 1,
   LMO is Line - 1,
   (X =:= LPO; X =:= LMO),
   Y =:= Column,!.

   verifyBlock(X, Y) :-
   canMove(X, Y),
   mapType(X, Y, pokemon(Pokemon, _)),
   pokeballs(Balls),
   Balls > 0,
   assert(mapPoints(X, Y, 200)),!.

   verifyBlock(X, Y) :-
   canMove(X, Y),
   mapType(X, Y, store),
   needCatchPokeballs,
   assert(mapPoints(X, Y, 150)),!.

   verifyBlock(X, Y) :-
   canMove(X, Y),
   mapType(X, Y, pokeCenter),
   recover(1),
   assert(mapPoints(X, Y, 140)),!.

   verifyBlock(X, Y) :-
   canMove(X, Y),
   mapType(X, Y, trainer),
   pokemon(_, _),
   recover(0),
   assert(mapPoints(X, Y, 130)),!.

   verifyBlock(X, Y) :-
   canMove(X, Y),
   not(visited(X, Y)),
   assert(mapPoints(X, Y, 120)),!.

   verifyBlock(X, Y) :-
   canMove(X, Y),
   canWalk('Water'),
   canWalk('Volcano'),
   canWalk('Mountain'),
   canWalk('Cave'),
   mapType(W, Z, pokemon(_, _)),
   calculateDistance(X, Y, W, Z, Distance),
   Points is 110 - Distance,
   assert(mapPoints(X, Y, Points)),!.

   verifyBlock(X, Y) :-
   canMove(X, Y),
   canWalk('Water'),
   canWalk('Volcano'),
   canWalk('Mountain'),
   canWalk('Cave'),
   unknown(W, Z),
   calculateDistance(X, Y, W, Z, Distance),
   Points is 110 - Distance,
   assert(mapPoints(X, Y, Points)),!.

   verifyBlock(X, Y) :-
   canMove(X, Y),
   frontBlock(X, Y),
   random(60, 90, Rand),
   assert(mapPoints(X, Y, 90)),!.

   verifyBlock(X, Y) :-
   canMove(X, Y),
   sideBlock(X, Y),
   random(50, 90, Rand),
   assert(mapPoints(X, Y, Rand)),!.

   verifyBlock(X, Y) :-
   canMove(X, Y),
   random(40, 90, Rand),
   assert(mapPoints(X, Y, Rand)),!.


   moviment(A, B, C, D) :- A >= B, A >= C, A >= D, moveDown,!.
   moviment(A, B, C, D) :- B >= A, B >= C, B >= D, moveUp,!.
   moviment(A, B, C, D) :- C >= A, C >= B, C >= D, moveRight,!.
   moviment(A, B, C, D) :- D >= A, D >= B, D >= C, moverLeft,!.

   move :-
   localization(Line, Column),
   LPO is Line + 1,
   LMO is Line - 1,
   CPO is Column + 1,
   CMO is Column - 1,
   verifyBlock(LPO, Column),
   verifyBlock(LMO, Column),
   verifyBlock(Line, CPO),
   verifyBlock(Line, CMO),
   mapPoints(LPO, Column, P1),
   mapPoints(LMO, Column, P2),
   mapPoints(Line, CPO, P3),
   mapPoints(Line, CMO, P4),
   moviment(P1, P2, P3, P4).


  %Regra action que comporta todas as principais regras que serão executadas pelo agente 
  action :- catch,!.
  action :- catchPokeballs,!.
  action :-  recover(1),  recoverPokemons,!.
  action :- recover(0), pokemon(_, _),  battleTrainer,!.
  action :- move,!.

   
   