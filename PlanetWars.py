#!/usr/bin/env python
#

from math import ceil, sqrt
from sys import stdout

from DebugLog import log

class Fleet:
  def __init__(self, owner, num_ships, source_planet, destination_planet, \
   total_trip_length, turns_remaining):
    self._owner = owner
    self._num_ships = num_ships
    self._source_planet = source_planet
    self._destination_planet = destination_planet
    self._total_trip_length = total_trip_length
    self._turns_remaining = turns_remaining

  def Owner(self):
    return self._owner

  def NumShips(self):
    return self._num_ships

  def SourcePlanet(self):
    return self._source_planet

  def DestinationPlanet(self):
    return self._destination_planet
  def __repr__(self):
    return 'fleet of ' + str(self.NumShips()) + ' owned by: ' + str(self.Owner()) + ' going from ' + str(self.SourcePlanet()) + ' > ' + str(self.DestinationPlanet())

  def TotalTripLength(self):
    return self._total_trip_length

  def TurnsRemaining(self):
    return self._turns_remaining


class Planet:
  def __init__(self, planet_id, owner, num_ships, growth_rate, x, y):
    self._planet_id = planet_id
    self._owner = owner
    self._num_ships = num_ships
    self._growth_rate = growth_rate
    self._x = x
    self._y = y
    
  def __str__(self):
    return 'Planet Id: ' + str(self._planet_id) + ' with ' + (self._num_ships) + 'ships'

  def PlanetID(self):
    return self._planet_id

  def Owner(self, new_owner=None):
    if new_owner == None:
      return self._owner
    self._owner = new_owner

  def NumShips(self, new_num_ships=None):
    if new_num_ships == None:
      return self._num_ships
    self._num_ships = new_num_ships

  def GrowthRate(self):
    return self._growth_rate

  def X(self):
    return self._x

  def Y(self):
    return self._y

  def AddShips(self, amount):
    self._num_ships += amount

  def RemoveShips(self, amount):
    self._num_ships -= amount

class PlanetWars:
  def __init__(self, gameState):
    self._planets = []
    self._fleets = []
    self.ParseGameState(gameState)

  def NumPlanets(self):
    return len(self._planets)

  def GetPlanet(self, planet_id):
    return self._planets[planet_id]

  def NumFleets(self):
    return len(self._fleets)

  def GetFleet(self, fleet_id):
    return self._fleets[fleet_id]

  def Planets(self):
    return self._planets

  def MyPlanets(self):
    r = []
    for p in self._planets:
      if p.Owner() != 1:
        continue
      r.append(p)
    return r

  def NeutralPlanets(self):
    r = []
    for p in self._planets:
      if p.Owner() != 0:
        continue
      r.append(p)
    return r

  def EnemyPlanets(self):
    r = []
    for p in self._planets:
      if p.Owner() <= 1:
        continue
      r.append(p)
    return r

  def NotMyPlanets(self):
    r = []
    for p in self._planets:
      if p.Owner() == 1:
        continue
      r.append(p)
    return r

  def Fleets(self):
    return self._fleets

  def MyFleets(self):
    r = []
    for f in self._fleets:
      if f.Owner() != 1:
        continue
      r.append(f)
    return r

  def EnemyFleets(self):
    r = []
    for f in self._fleets:
      if f.Owner() <= 1:
        continue
      r.append(f)
    return r

  def ToString(self):
    s = ''
    for p in self._planets:
      s += "P %f %f %d %d %d\n" % \
       (p.X(), p.Y(), p.Owner(), p.NumShips(), p.GrowthRate())
    for f in self._fleets:
      s += "F %d %d %d %d %d %d\n" % \
       (f.Owner(), f.NumShips(), f.SourcePlanet(), f.DestinationPlanet(), \
        f.TotalTripLength(), f.TurnsRemaining())
    return s

  def Distance(self, source_planet, destination_planet):
    source = self._planets[source_planet]
    destination = self._planets[destination_planet]
    dx = source.X() - destination.X()
    dy = source.Y() - destination.Y()
    return int(ceil(sqrt(dx * dx + dy * dy)))

  def IssueOrder(self, source_planet, destination_planet, num_ships):
    stdout.write("%d %d %d\n" % \
     (source_planet, destination_planet, num_ships))
    stdout.flush()
    
  def GetShipsAtArriveTime(self, source_planet, destination_planet):
    #log.debug('start GetShipsAtArriveTime() for source: ' + str(source_planet) + ' , destination: ' + str(destination_planet))
    distance = self.Distance(source_planet, destination_planet)
    #log.debug('distance: ' + str(distance))
    
    currentShips = [self._planets[destination_planet].NumShips(), self._planets[destination_planet].Owner()]
    #log.debug('current ships_: ' + str(currentShips))
    growthRate = self._planets[destination_planet].GrowthRate()
    my_fleets = [fleet for fleet in self.MyFleets() if fleet.DestinationPlanet() == destination_planet]
    enemy_fleets = [fleet for fleet in self.EnemyFleets() if fleet.DestinationPlanet() == destination_planet]
    
    #log.debug('enemy fleets: ' + str(enemy_fleets))
    #log.debug('my fleets: ' + str(my_fleets))
    
    allFleets = {}
    for fleet in my_fleets + enemy_fleets:
      turns = fleet.TurnsRemaining()
      
      if turns > distance:
        continue
      
      ships = fleet.NumShips()
      owner = fleet.Owner()
      
      if not allFleets.has_key(turns):
        allFleets[turns] = (ships, owner)
      else:
        if allFleets[turns][1] == owner:
          allFleets[turns] = (allFleets[turns][1] + ships, owner)
        else:
          s = allFleets[turns][0] - ships
          if s < 0:
            allFleets[turns] = (-s, 1 if allFleets[turns][1] == 2 else 2)
          else:
            allFleets[turns] = (s, allFleets[turns][1])
      
    #log.debug('all Fleets: ' + str(allFleets)) 
    
    #now we get to figure out what happens once all the fleets have shown up
    # up until we can get there if we leave this turn
    #log.debug('before figuring out future of planet, currentShips = ' + str(currentShips))
    
    lastTurn = 0
    for turn in sorted(allFleets.keys()):
      fleet = allFleets[turn]
      
      turnsSinceLast = turn - lastTurn
      lastTurn = turn
      if currentShips[1] == 0:
        #planet is neutral, no growing
        pass
      else:
        #planet is either mine or enemy's, regardless grow by growthRate * turnsSinceLast
        currentShips[0] += growthRate * turnsSinceLast
      
      if fleet[1] == currentShips[1]:
        #fleet is from the owner of the planet
        currentShips[0] += fleet[0]
      else:
        currentShips[0] -= fleet[0]
        if currentShips[0] < 0:
          currentShips[1] = fleet[1]
          currentShips[0] = -currentShips[0]
          
      log.debug('after fleet ' + str(fleet) + ' showed up: ' + str(currentShips))
      
    #add the growth between the last fleet showing up and when my fleet can get there
    if currentShips[1] != 0:
      currentShips[0] += (distance - lastTurn) * growthRate
      
    #log.debug('end of getShipsAtArriveTime()')
    return currentShips, distance
    

  def IsAlive(self, player_id):
    for p in self._planets:
      if p.Owner() == player_id:
        return True
    for f in self._fleets:
      if f.Owner() == player_id:
        return True
    return False

  def ParseGameState(self, s):
    self._planets = []
    self._fleets = []
    lines = s.split("\n")
    planet_id = 0

    for line in lines:
      line = line.split("#")[0] # remove comments
      tokens = line.split(" ")
      if len(tokens) == 1:
        continue
      if tokens[0] == "P":
        if len(tokens) != 6:
          return 0
        p = Planet(planet_id, # The ID of this planet
                   int(tokens[3]), # Owner
                   int(tokens[4]), # Num ships
                   int(tokens[5]), # Growth rate
                   float(tokens[1]), # X
                   float(tokens[2])) # Y
        planet_id += 1
        self._planets.append(p)
      elif tokens[0] == "F":
        if len(tokens) != 7:
          return 0
        f = Fleet(int(tokens[1]), # Owner
                  int(tokens[2]), # Num ships
                  int(tokens[3]), # Source
                  int(tokens[4]), # Destination
                  int(tokens[5]), # Total trip length
                  int(tokens[6])) # Turns remaining
        self._fleets.append(f)
      else:
        return 0
    return 1

  def FinishTurn(self):
    stdout.write("go\n")
    stdout.flush()
