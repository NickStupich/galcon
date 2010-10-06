from DebugLog import log

def doFirstTurn(pw):
  try:
    log.debug('Start of doFirstTurn()')
    myPlanets = pw.MyPlanets()
    if len(myPlanets) != 1:
      raise Exception("should always have 1 planet on turn on")
    myPlanet = myPlanets[0]
    if myPlanet.NumShips() != 100:
      raise Exception("should always have 100 ships on initial planet")
      
    availableShips = 99 # leave 5 behind minimum
      
    planets = []
    #try to get as much growth as possible, while also minimizing distance to planets, (and possible fleet loss)
    for planet in pw.NeutralPlanets():
      growthRate = planet.GrowthRate()
      distance = pw.Distance(myPlanet.PlanetID(), planet.PlanetID())
      minShips = planet.NumShips() + 1
      
      planets.append((minShips, growthRate, distance, planet))
    
    #log.debug('before sort: ' + '\n'.join([str(p) for p in planets]))
    planets.sort(cmp = distanceSort)
    #log.debug('after sort: ' + '\n'.join([str(p) for p in planets]))
    
    #not sure if the next line should be commented, or changed in some way
    planets = planets[:len(planets)/3]
      
    #log.debug('planets to actually consider: ' + '\n'.join([str(p) for p in planets]))

    planetsToConquer = getPlanetsToGoToFirst(planets, availableShips)
    
    for planet in planetsToConquer:
        log.debug('issueing order: planetId: ' + str(planet[0].PlanetID()) + ' with ' + str(planet[1]) + ' ships')
        pw.IssueOrder(myPlanet.PlanetID(), planet[0].PlanetID(), planet[1])
        
    log.debug('end of doFirstTurn()')
    return True
  except Exception, e:
    log.exc(e)
    return False
  
def distanceSort(x, y):
  if x[2] > y[2]:
    return 1
  elif x[2] < y[2]:
    return -1
  return 0
  
def fleetSizeSort(x, y):
  if x[0] > y[0]:
    return -1
  elif x[0] < y[0]:
    return 1
  return 0

bestIndeces = []
  
def getPlanetsToGoToFirst(planetTuples, availableShips):
  """
  takes a list of the physically closest planets to the home
  returns a list of planets that should immediately be attacked
  """
  
  planetTuples.sort(cmp = fleetSizeSort)
  
  #sorted with the largets fleet first, recursively keep adding fleets until you run out of space
  #if it gets the most growth, keep track of it
  
  #log.debug('planets sorted by fleet size: \n' + '\n'.join([str(x) for x in planetTuples]))
  
  log.debug('before recursiveIndexFinder()')
  best = recursiveIndexFinder(planetTuples, [], availableShips)
  #planetsToAttack = 
  
  log.debug('best planets to go to first: ' + str(best))
  
  result = [] # list of planet, number of ships
  for index in best[0]:
    result.append((planetTuples[index][3], planetTuples[index][0]))
  
  return result


def getShipsRequired(planetTuples, indeces):
    return sum([planetTuples[index][0] for index in indeces])
  
def getGrowthRate(planetTuples, indeces):
    return sum([planetTuples[index][1] for index in indeces])
  
def recursiveIndexFinder(planetTuples, currentIndeces, availableShips):
    """planet Tuples: [((minShips, gain, distance, planet))]
    current Indeces = [planetToAttack]
    availableShips = int
    """
    
    best = (currentIndeces, getGrowthRate(planetTuples, currentIndeces), getShipsRequired(planetTuples, currentIndeces))
    
    #log.debug('best so far: ' + str(best))
    for index, tuple in enumerate(planetTuples):
        if not currentIndeces.__contains__(index):
            requiredShips = getShipsRequired(planetTuples, currentIndeces + [index])
            if requiredShips <= availableShips:
                growthRate = getGrowthRate(planetTuples, currentIndeces + [index])
                #log.debug('trying ' + str(currentIndeces + [index]) + ' -> ships: ' + str(requiredShips) + ' growth rate: ' + str(growthRate))
                #if growthRate > best[1] or (growthRate == best[1] and requiredShips < best[2]):
                #    best = recursiveIndexFinder(planetTuples, currentIndeces + [index], availableShips)
                
                subBest = recursiveIndexFinder(planetTuples, currentIndeces + [index], availableShips)
                if subBest[1] > best[1] or (subBest[1] == best[1] and subBest[2] < best[2]):
                    best = subBest
    
    return best
                