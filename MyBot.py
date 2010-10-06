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
from Settings import *

turn_number = 0
wait_for_enemy = False

def DoTurn4(pw):
  global wait_for_enemy
  global turn_number
  turn_number += 1
  try:
    
    if turn_number == 1:
      distance_to_enemy = pw.Distance(pw.MyPlanets()[0].PlanetID(), pw.EnemyPlanets()[0].PlanetID())
      if distance_to_enemy < distance_to_wait_first_turn:
        wait_for_enemy = True
        
    if wait_for_enemy:
      if len(pw.Fleets()) > 0:
        wait_for_enemy = False
      else:
        return
    
    #for each of my planets
      #for each of the other planets
      
        #find the total number of fleets when we could get there from our planet, then determine the best planet to attack
    
    orders = []
    allGains = {}
    stayHomeGain = getAvailableShips(pw)
    availableShips = {}
    
    for my_planet in pw.MyPlanets():
      gains = []
      
      #add the gains attained by leaving ships here
      for ships in stayHomeGain[my_planet.PlanetID()]:
        gains.append((ships, stayHomeGain[my_planet.PlanetID()][ships], my_planet.PlanetID()))
        
      for other_planet in pw.Planets():
        if other_planet.GrowthRate() == 0: # not worth taking over
          continue
        if my_planet.PlanetID() == other_planet.PlanetID(): #same planet
          continue
        
        availableShips[my_planet.PlanetID()] = max(0, my_planet.NumShips() - extra_ships)
        
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
    
    orders = getBestOrders3(allGains, availableShips, pw)
    #orders += addStreamOrders(orders, availableShips, pw)
    #if turn_number == 1:
    #  orders = optimizeOrdersForTurn1(orders)
    log.debug('got orders from getBestOrders3(): \n' + '\n'.join([str(x) for x in orders]))
    
    log.debug('Starting to issue all orders')
    for order in orders:
      try:
        pw.IssueOrder(order[0], order[1], order[2])
      except Exception, e:
        log.exc(e)
    log.debug('done issueing orders')
    
  except Exception, e:
    log.exc(e)


"""
def getPlanetGains(sourcePlanet, destinationPlanet, pw):
  fleets = {}
  for turn in range(turns_ahead):
    fleets[turn] = []
    
  for fleet in pw.Fleets():
    if fleet.DestinationPlanet() == destinationPlanet.PlanetID() and fleet.TurnsRemaining < turns_ahead:
      fleets[fleet.TurnsRemaining()].append(fleet)
  
  distance = pw.Distance(sourcePlanet.PlanetID(), destinationPlanet.PlanetID())
  
  log.debug('planets ' + str(sourcePlanet) +  '   ,  ' + str(destinationPlanet))
  log.debug('distance: ' + str(distance))
  
  newFleet = 0
  shipsGains = {}
  keepLooping = True
  
  while keepLooping:
    keepLooping = False
    ships = destinationPlanet.NumShips()
    currentOwner = destinationPlanet.Owner()
    gain = 0
    
    for turn in range(turns_ahead):
      ships += planet.GrowthRate()
      
      arriving = sum([fleet.NumShips() for fleet in fleets[turn] if fleet.Owner() == 1]) - sum([fleet.NumShips() for fleet in fleets[turn] if fleet.Owner() == 2])
        #log.debug('arriving: ' + str(arriving))
      if arriving == 0:
        continue
      if arriving > 0:
        fleetOwner = 1
      else:
        fleetOwner = 2
      arriving = abs(arriving)
      
      if currentOwner == fleetOwner:
        ships += arriving
      elif ships >= arriving:
        ships -= arriving
      else:
        #planet will be changing sides
        if currentOwner == 1:
          if turn >= distance:
            keepLooping = True
            #i'm losing a planet, so there could be gain by sending additional ships here
          else:
            #gonna lose it anyways, no point in
"""
    
def addStreamOrders(orders, stayHomeGain, pw):
  new_orders = []
  for my_planet in pw.MyPlanets():
    totalOrdersSent = sum([order[2] for order in orders if order[0] == my_planet.PlanetID()])
    available = stayHomeGain[my_planet.PlanetID()]
    
    bestGainStaying = -1
    for ships in available:
      if available[ships] > bestGainStaying:
        bestGainStaying = available[ships]
        shipsLeft = my_planet.NumShips() - totalOrdersSent - ships
    
    log.debug('for planet : ' + str(my_planet))
    log.debug('total orders sent: ' + str(totalOrdersSent))
    log.debug('ships left: ' + str(shipsLeft))
    log.debug('availableShips: ' + str(available))
    
    if availableShips > 0:
      log.debug('find a potential planet to send to')
      
  return new_orders
    
def optimizeOrdersForTurn1(orders, pw):
  """removes orders where the planet being attacked is 3 or fewer turns closer to me than the opponents
  should prevent having planets sniped"""
  opponentPlanet = pw.EnemyPlanets()[0]
  index = 0
  while index < len(orders):
    order = orders[index]
    distanceToMe = pw.Distance(order[0], order[1])
    distanceToOpponent = pw.Distance(order[1], opponentPlanet)
    difference = distanceToOpponent - distanceToMe
    
    if difference >= 0 and difference <= 3:
      pass
    
  return orders
  
    

def getAvailableShips(pw):
  """
  returns a dict of {planetId, value}
  value is a dict of the number of ships required, and the gain over the next turns_ahead turns
  """
  result = {}
  
  for planet in pw.MyPlanets():
    fleets = {}
    for turn in range(turns_ahead):
      fleets[turn] = []
      
    for fleet in pw.Fleets():
      if fleet.DestinationPlanet() == planet.PlanetID() and fleet.TurnsRemaining() < turns_ahead:
        fleets[fleet.TurnsRemaining()].append(fleet)
    
    shipsRequiredGains = {}
    newStartingShips = 0
    keepLooping = True
    
    log.debug('fleet turns remaining: \n' + '\n'.join([str(fleets[turns]) for turns in range(turns_ahead)]))
    keepLoopingCount = 0
    while keepLooping:
      keepLoopingCount += 1
      
      if keepLoopingCount > turns_ahead:
        raise Exception("keep looping count is too high")
        
      #log.debug('keep looping count: ' + str(keepLoopingCount))
      startingShips = newStartingShips
      ships = startingShips
      currentOwner = 1
      keepLooping = False
      gain = 0

      for turn in range(turns_ahead):
        ships += planet.GrowthRate()
        #log.debug('ships: ' + str(ships) + ' owner: ' + str(currentOwner))
        if currentOwner == 1:
          gain += planet.GrowthRate()
        else:
          gain -= planet.GrowthRate()
          
        arriving = sum([fleet.NumShips() for fleet in fleets[turn] if fleet.Owner() == 1]) - sum([fleet.NumShips() for fleet in fleets[turn] if fleet.Owner() == 2])
        #log.debug('arriving: ' + str(arriving))
        if arriving == 0:
          continue
        if arriving > 0:
          fleetOwner = 1
        else:
          fleetOwner = 2
        arriving = abs(arriving)
          
        if currentOwner == fleetOwner:
          ships += arriving
        elif ships >= arriving:
          ships -= arriving
        else:
          #planet will be changing hands
          if currentOwner == 1:
            #im losing it
            currentOwner = 2
            
            if keepLooping: #we already have a new starting point, so just keep moving through to get the overall gain
              pass
            else:
              newStartingShips = newStartingShips + arriving - ships
              keepLooping = True
              
          else:
            #i'm getting another planet, no need to change the starting ships since this is good
            currentOwner = 1
              
          ships = arriving - ships
            
      shipsRequiredGains[startingShips] = gain
      
    #normalize gains to the 0 starting ships case
    for ships in shipsRequiredGains:
      shipsRequiredGains[ships] -= shipsRequiredGains[0]
      
    #log.debug('starting ships: planet ' + str(planet.PlanetID()) + ' with ' + str(planet.NumShips()) + ' ships:')
    #log.debug(str(shipsRequiredGains))
         
    result[planet.PlanetID()] = shipsRequiredGains
    
  return result

def getBestOrders1(gains, availableShips, pw):
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
  return orders

def getBestOrders2(gains, availableShips, pw):
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
  return orders

def getBestOrders3(allGains, allAvailableShips, pw):
  #gains: dict, key = planetId, list of (ships required, gain, other planetID())
  #available ships: dict, key = planetId, int of available ships for attacking
  
  #has the 'stay here' gains
  
  orders = [] #list of (source planetId, destinationPlanetId, number of attackers)
  
  
  for planet in allAvailableShips:
    log.debug('started planet ' + str(planet))
    availableShips = allAvailableShips[planet]
    gains = sorted(allGains[planet], reverse = True)
    
    if planet == 1:
      log.debug('planet: ' + str(planet) + '   available ships: ' + str(availableShips))
      log.debug('gains: \n' + '\n'.join([str(x) for x in enumerate(gains)]))
    
    if len(gains) == 0:
      log.debug('no planets left to conquer?')
      continue
    
    if availableShips == 0:
      continue
    
    #now recursively optimize the gain
    indeces = []
    
    strategy = optimizeFleets(gains, availableShips, [])
    
    for index in strategy[1]:
      planet_to_attack = gains[index][2]
      ships = gains[index][0]
        
      if planet_to_attack == planet:
        if ships > 0:
          log.debug('decided to leave ' + str(ships) + ' fleets at home planet')
        pass
      else:
        orders.append((planet, planet_to_attack, ships))
      
    log.debug('planet: ' + str(planet) + ' best places to attack: ' + str(strategy[1]))
    
  #log.debug('getBestOrders3 returning : ' + str(orders))
  return orders

def optimizeFleets(gains, availableShips, currentIndeces):
  startIndex = 0 if len(currentIndeces) == 0 else currentIndeces[-1] + 1
  #log.debug('optimizeFleets(), indeces: ' + str(currentIndeces) + ' startIndex: ' + str(startIndex))
  
  best = (sum([gains[index][1] for index in currentIndeces]), currentIndeces)
  for index, gain in enumerate(gains[startIndex:]):
    if gain[0] <= availableShips: # there are enough ships
      tempBest = optimizeFleets(gains, availableShips - gain[0], currentIndeces + [index + startIndex])
      if tempBest > best: # should add logic for equal, use closer or less ships or something
        best = tempBest
        
  return best
    
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
      pw = PlanetWars(map_data)
      DoTurn4(pw)
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
