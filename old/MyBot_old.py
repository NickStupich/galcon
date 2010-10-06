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

import logging
LOG_FILENAME = 'debugLogs/log1.txt'
turn_number = 0

from PlanetWars import PlanetWars

def DoTurn(pw):
  global turn_number
  turn_number += 1
  
  logging.debug('\n\n**starting turn %d ***\n' % turn_number)
  # (1) If we currently have a fleet in flight, just do nothing.
  
  try:
    if pw.Production(1) >= pw.Production(2):
      numFleets = 1
    else:
      numFleets = 3
    
    numFleets = 3
    
    logging.debug('numFleets: ' + str(numFleets))
    
    if len(pw.MyFleets()) >= numFleets:
      logging.debug('end of turn')
      return
  except Exception, e:
    logging.error('step 1: ' + str(e))
    return 
  logging.debug('done step 1')
  
  try:
    # (2) Find my strongest planet.
    source = -1
    source_score = -999999.0
    source_num_ships = 0
    my_planets = pw.MyPlanets()
    for p in my_planets:
      score = float(p.NumShips()) / (1 + p.GrowthRate())
      if score > source_score:
        source_score = score
        source = p.PlanetID()
        source_num_ships = p.NumShips()
  except Exception, e:
    logging.error('step 2: ' + str(e))
    return
  logging.debug('done step 2')
  
  try:
    # (3) Find the weakest enemy or neutral planet.
    dest = -1
    dest_score = -999999.0
    not_my_planets = pw.NotMyPlanets()
    for p in not_my_planets:
      if p.NumShips() == 0:
        logging.debug('number of ships is 0')
        score = 1000
      else:
        score = (1.0 + p.GrowthRate()) / (1.0 + p.NumShips())
      if score > dest_score:
        dest_score = score
        dest = p.PlanetID()
  except Exception, e:
    logging.error('step 3: ' + str(e))
    return
  logging.debug('done step 3')
  
  try:
    # (4) Send half the ships from my strongest planet to the weakest
    # planet that I do not own.
    if source >= 0 and dest >= 0:
      num_ships = source_num_ships / 2
      pw.IssueOrder(source, dest, num_ships)
  except Exception, e:
    logging.error('step 4: ' + str(e))
    return
  logging.debug('done step 4')
  
  logging.debug('end of turn')

def main():
  
  logging.basicConfig(filename = LOG_FILENAME, level = logging.DEBUG)
  
  map_data = ''
  while(True):
    current_line = raw_input()
    if len(current_line) >= 2 and current_line.startswith("go"):
      pw = PlanetWars(map_data)
      DoTurn(pw)
      pw.FinishTurn()
      map_data = ''
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
