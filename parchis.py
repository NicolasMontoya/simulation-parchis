"""Simulación de Parques para el curso de fundamentos - Edward Nicolas Montoya Arcila

Este archivo es un script, no debería importarse como modulo.


"""

import random
from itertools import cycle


class Parchis:
  """
    Parchis Game !.
    Simulation for 

    Attributes
    ----------
    DEFAULT_PACHIS_GAMEPIECES: int
      Total de fichas de parques por persona
    __ALLOW_NUM_USER: list
      Lista con el número de usuarios permitidos

    Methods
    -------
    run_sim()
      Inicializa la simulación
  """
  DEFAULT_PACHIS_GAMEPIECES = 4
  __ALLOW_NUM_USER = [4, 6, 8]
  def __init__(self, num_users):
    if (num_users not in self.__ALLOW_NUM_USER):
      raise ValueError('El parques debe ser de 4, 6 u 8 puestos')
    users = [User(i, [GamePiece(i) for i in range(Parchis.DEFAULT_PACHIS_GAMEPIECES)]) for i in range(num_users) ]
    pieces = [y for x in users for y in x.pieces]
    self.board = Board(pieces, num_users)
    self.users = users
    self.ids = [x.id for x in users]
    self.move = 0
  def run_sim(self):
    pool = cycle(range(4))
    for item in pool:
      self.move += 1
      print(f'Turno {self.move} - Jugador {item}')
      res = self.users[item].move_piece()
      if res in self.ids:
        print(f'El duró {self.move} turnos.')
        print(f'El ganador es el Jugador {res}')
        print('Gracias por jugar')
        break
      self.board.validateGame(self.users[item])
      
    
class Board:
  """
    Tablero de juego

    Attributes
    ----------
    MAX_BOARD_BOX: int
      Cantidad de casillas que tiene un tablero
    KILL_ZONE_BOX: int
      Cantidad de casillas que la ficha se encuentra en peligro
    SAVE_PLACES
  """
  MAX_BOARD_BOX = 70
  KILL_ZONE_BOX = 63
  SAVE_PLACES = []
  def __init__(self, pieces, num_users):
    self.KILL_ZONE_BOX = (num_users * 17) - 5 
    self.MAX_BOARD_BOX = self.KILL_ZONE_BOX + 8
    self.pieces = pieces
    accumulate = 0
    i = 0
    while accumulate <= (4*17) -5:
      if (i % 3 == 0):
        self.SAVE_PLACES.append(accumulate)
        accumulate += 7
      else:
        self.SAVE_PLACES.append(accumulate)
        accumulate += 5
      i += 1
  def validateGame(self, user):
    for user_piece in user.pieces:
      for piece in set(self.pieces).difference(set(user.pieces)):
        user_real_pos = (user_piece.user_id * 17) + user_piece.pos
        piece_real_pos = (piece.user_id * 17) + piece.pos
        if (user_real_pos == piece_real_pos and user_piece.pos <= self.KILL_ZONE_BOX and not(self.isSave(piece_real_pos))):
          print(f'Jugador {user_piece.user_id} POS({user_piece.pos}) REALPOS {user_real_pos} se comió al Jugador {piece.user_id} POS({piece.pos}) REALPOS {piece_real_pos}')
          piece.moveToZero()
  def isSave(self, pos):
    return pos in self.SAVE_PLACES

class User:
  def __init__(self, id, pieces):
    self._id = id
    self._pieces = pieces
    self.finish = 0
  
  @property
  def pieces(self):
    return self._pieces
  
  @property
  def id(self):
    return self._id
  
  def move_piece(self):
    move = random.randrange(1,7)
    print(f'DADO SACO -> {move}')
    for i in self._pieces:
      if(i.pos + move <= Board.MAX_BOARD_BOX):
        print(f'Ficha {self._pieces.index(i)} - posición inicial {i.pos} - posición final {i.pos + move}')
        i.move(move)
        if (i.pos == Board.MAX_BOARD_BOX):
          print (f'Ficha {self._pieces.index(i)} - CORONO')
          i.move(1)
          self.finish += 1
          if (self.finish == Parchis.DEFAULT_PACHIS_GAMEPIECES):
            return self._id
        break

class GamePiece:
  def __init__(self, user_id):
    self._user_id = user_id
    self._pos = 0
  @property
  def user_id(self):
    return self._user_id
  @property
  def pos(self):
    return self._pos
  def move(self, number_move):
    self._pos += number_move
  def moveToZero(self):
    self._pos = 0
  def __str__(self):
    return f"GamePiece -> POS:{self._pos}"

myParchis = Parchis(4)
myParchis.run_sim()