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

from DebugLog import log
turn_number = 0
turns_ahead = 20 #for gain
extra_ships = 1 #1 more than neccessary to take over a planet

def DoTurn3(pw):
  global turn_number
  turn_number += 1
  try:
    #if turn_number == 1:
      #if FirstTurn.doFirstTurn(pw):
      #  return
    
    #for each of my planets
      #for each of the other planets
      
        #find the total number of fleets when we could get there from our planet, then determine the best planet to attack
    
    orders = []
    allGains = {}
    availableShips = {}
    
    for my_planet in pw.MyPlanets():
      
      availableShips[my_planet.PlanetID()] = max(0, my_planet.NumShips() - extra_ships)
      
      gains = []
      for other_planet in pw.Planets():
        if other_planet.GrowthRate() == 0: # not worth taking over
          continue
        if my_planet.PlanetID() == other_planet.PlanetID(): #same planet
          continue
        
        shipsAtArriveTime, time = pw.GetShipsAtArriveTime(my_planet.PlanetID(), other_planet.PlanetID())
        if shipsAtArriveTime[1] == 1:
          # we will have control of that planet, don't bother with it
          pass
        else:
          # should we try to take over?
          gain = 0 if time >= turns_ahead else (turns_ahead - time) * other_planet.GrowthRate() * (1 if shipsAtArriveTime == 0 else 2)
          
          gains.append((shipsAtArriveTime[0] + extra_ships, gain, other_planet.PlanetID()))
      
      allGains[my_planet.PlanetID()] = sorted(gains)
    
    log.debug('got all gains')
    
    orders = getBestOrders2(allGains, availableShips, pw)
    log.debug('got orders from getBestOrders1(): \n' + '\n'.join([str(x) for x in orders]))
    
    log.debug('Starting to issue all orders')
    for order in orders:
      try:
        pw.IssueOrder(order[0], order[1], order[2])
      except Exception, e:
        log.exc(e)
    log.debug('done issueing orders')
    
  except Exception, e:
    log.exc(e)
  
def getBestOrders1(gains, availableShips, pw):
  log.start()
  #gains: dict, key = planetId, list of (ships required, gain, other planetID())
  #available ships: dict, key = planetId, int of available ships for attacking
  orders = [] #list of (source planetId, destinationPlanetId, number of attackers)
  
  for planet in availableShips:
    log.debug('planet: ' + str(planet) + '   available ships: ' + str(availableShips[planet]))
    log.debug('gains: \n' + '\n'.join([str(x) for x in gains[planet]]))
    
    if availableShips[planet] == 0:
      continue
    # should probably do some recursive optimization crazyness here...
    if gains[planet][0][0] < availableShips[planet]:
      orders.append((planet, gains[planet][0][2], gains[planet][0][0]))
  
  log.debug('getBestOrders1 returning : ' + str(orders))
  log.stop()
  return orders

def getBestOrders2(gains, availableShips, pw):
  log.start()
  #gains: dict, key = planetId, list of (ships required, gain, other planetID())
  #available ships: dict, key = planetId, int of available ships for attacking
  orders = [] #list of (source planetId, destinationPlanetId, number of attackers)
  
  
  for planet in availableShips:
    log.debug('planet: ' + str(planet) + '   available ships: ' + str(availableShips[planet]))
    log.debug('gains: \n' + '\n'.join([str(x) for x in gains[planet]]))
    
    if len(gains[planet]) == 0:
      log.debug('no planets left to conquer?')
      continue
    
    if availableShips[planet] == 0:
      continue
    # should probably do some recursive optimization crazyness here...
    if gains[planet][0][0] < availableShips[planet]:
      previousDistance = orderAlreadyPlaced(orders, gains[planet][0][2], pw)
      log.debug('orders: ' + str(orders))
      log.debug('order to place: ' + str((planet, gains[planet][0][2], gains[planet][0][0])))
      log.debug('previous distance: ' + str(previousDistance))
      if previousDistance is None:
        orders.append((planet, gains[planet][0][2], gains[planet][0][0]))
        
      #if there has already been an order placed, choose the one that's closest
      if previousDistance < pw.Distance(planet, gains[planet][0][2]):
        # do nothing, the previous one is better
        pass
      else:
        # replace the order to be sent from the current planet, with the current fleet size(since it may vary due to different distance)
        for i in range(len(orders)):
          if orders[i][1] == gains[planet][0][2]:
            orders[i] = (planet, gains[planet][0][2], gains[planet][0][0])
  
  log.debug('getBestOrders2 returning : ' + str(orders))
  log.stop()
  return orders
    
def orderAlreadyPlaced(orders, destination, pw):
  """returns the distance if the order has been placed, else None"""
  for order in orders:
    if order[1] == destination:
      return pw.Distance(destination, order[0])
      
  return None
    
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
      log.stop()
      pw = PlanetWars(map_data)
      DoTurn3(pw)
      pw.FinishTurn()
      map_data = ''
      log.start()
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
