#!/usr/bin/env python
#

"""
// The DoTurn function is where your code goes. The PlanetWars object contains
// the state of the game, including information about all planets and fleets
// that currently exist. Inside this function, you issue orders using the
// pw.IssueOrder() function. For example, to send 10 ships from planet 3 to
// planet 8, you would say pw.IssueOrder(3, 8, 10).
//
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own. Check out the tutorials and articles on the contest website at
// http://www.ai-contest.com/resources.
"""
    
from PlanetWars import PlanetWars
import FirstTurn

from DebugLog import log
log.stop()
turn_number = 0
turns_ahead = 20 #for gain
extra_ships = 1 #1 more than neccessary to take over a planet

def DoTurn(pw):
  try:
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(pw.MyFleets()) >= 3:
      log.debug('Returning since more than 2 fleets are out')
      return
    # (2) Find my strongest planet.
    source = -1
    source_score = -999999.0
    source_num_ships = 0
    my_planets = pw.MyPlanets()
    for p in my_planets:
      score = float(p.NumShips())
      if score > source_score:
        source_score = score
        source = p.PlanetID()
        source_num_ships = p.NumShips()
  
    # (3) Find the weakest enemy or neutral planet.
    dest = -1
    dest_score = -999999.0
    not_my_planets = pw.NotMyPlanets()
    for p in not_my_planets:
      score = 1.0 / (1 + p.NumShips())
      if score > dest_score:
        dest_score = score
        dest = p.PlanetID()
  
    # (4) Send half the ships from my strongest planet to the weakest
    # planet that I do not own.
    if source >= 0 and dest >= 0:
      num_ships = source_num_ships / 2
      pw.IssueOrder(source, dest, num_ships)
  except Exception, e:
    log.error(str(e))
  
def filterOrders(orders, distanceFunc):
  try:
    destinations = {}
    removeIndeces =[]
    for index, (source, destination, fleet) in enumerate(orders):
      if destinations.has_key(destination):
        distance1 = distanceFunc(source, destination)
        distance2 = distanceFunc(destinations[destination][0][0], destinations[destination][0][1])
        if distance1 < distance2:
          removeIndeces.append(destinations[destination][1])
        else:
          removeIndeces.append(index)          
      else:
        destinations[destination] = ((source, destination, fleet), index)
    
    log.debug('orders: ' + str(orders))
    log.debug('remove indeces: ' + str(removeIndeces))
    for index in sorted(removeIndeces, reverse = True):
      orders.pop(index)
    
    log.debug('orders after: ' + str(orders))
          
  except Exception, e:
    log.exc(e)
    
def FleetIsEnRoute(sourceId, destinationId, myFleets):
  for fleet in myFleets:
    if fleet.SourcePlanet() == sourceId and fleet.DestinationPlanet() == destinationId:
      # should check that there are enough on the way to claim the planet
      return True
  
  return False
    
def PlanetWorthinessToTakeOver(myPlanet, otherPlanet, minFleetSize, distance):
  try:
    enemyLoss = int(otherPlanet.Owner() == 2) * otherPlanet.GrowthRate()
    growthRate = otherPlanet.GrowthRate()
    
    log.debug('enemy loss: ' + str(enemyLoss))
    log.debug('growth rate: ' + str(growthRate))
    log.debug('min fleet size: ' + str(minFleetSize))
    
    result = 1.0 * (growthRate + enemyLoss) / (minFleetSize * ( 1.0 + distance)**2.0)
    
    log.debug('result of planet worthiness: ' + str(result))
    
    return result
  except Exception, e:
    log.exc(e)
    log.error('due to error, PlanetWorthinessToTakeOver() will return 0')
    return 0.0
  
def main():
  map_data = ''
  while(True):
    current_line = raw_input()
    if len(current_line) >= 2 and current_line.startswith("go"):
      log.startTurn()
      pw = PlanetWars(map_data)
      DoTurn(pw)
      pw.FinishTurn()
      map_data = ''
      log.debug('finished turn')
    else:
      map_data += current_line + '\n'


if __name__ == '__main__':
  try:
    import psyco
    psyco.full()
  except ImportError:
    pass
  try:
    main()
  except KeyboardInterrupt:
    print 'ctrl-c, leaving ...'
