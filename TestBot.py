import os
import random
import datetime
random.seed(datetime.datetime.now())
my_bot = 'MyBot.py'

bots = ['example_bots/' + filename for filename in os.listdir(os.curdir + '/example_bots') if filename.__contains__('Bot') and filename.__contains__('.jar')]
maps = ['maps/' + filename for filename in os.listdir(os.curdir + '/maps') if filename.__contains__('.txt')]
#COMMAND_STRING = 'java -jar tools/PlayGame.jar %s 200 200 log.txt "python %s" "java -jar %s"'
COMMAND_STRING = 'java -jar tools/PlayGame.jar %s 200 200 log.txt "python %s" "%s %s"'


def runTestMulti(n):
    return runTest(n[0], n[1])

def runTest(bot, map):
    command = COMMAND_STRING % (map, my_bot, 'python' if bot.__contains__('.py') else 'java -jar' , bot) + '> playGameOutput.txt'
    #print command
    fi, fo, fe = os.popen3(command)
    #gameRecord = fo.readlines()
    lines = [line for line in fe.readlines() if len(line) > 1]
    #print lines[-3]
    #print command
    #print lines[-1]
    #print '\n'
    if lines[-1].__contains__('Player 1 Wins!'):
        result = 1
    elif lines[-1].__contains__('Player 2 Wins!'):
        result = 2
    elif lines[-1].__contains__('Draw!'):
        result = 0
    else:
        print lines
        raise Exception("unknown winner")
        
    if lines[-3].__contains__('timed out'):
        result = -1
        print 'timed out against %s on map %s' % (bot, map)
    
    fi.close()
    fo.close()
    fe.close()
    return result
    
def runWithVisualization(bot, map):
    command = COMMAND_STRING % (map, my_bot, bot) + ' | java -jar tools/ShowGame.jar' 
    os.system(command)
    
def successTest(count):
    global bots
    global maps

    global my_bot
    folder = 'temp\\' + str(datetime.datetime.now()).replace(':', '_').replace(' ', '_').split('.')[0] 
    my_bot = folder + '\\' + my_bot
    print 'MD \\' + folder
    os.system('MD ' + folder)
    os.system('copy *.py ' + folder)
    
    wins = 0
    losses = 0
    timeouts = 0
    ties = 0
    
    #maps = ['maps/map%s.txt' % i for i in [22,26,30,44,61,84,88]]
    
    bots.remove('example_bots/RandomBot.jar')
    bots.remove('example_bots/ProspectorBot.jar')
    bots.remove('example_bots/BullyBot.jar')
    #bots = ['example_bots/RageBot.jar']
    
    #bots += ['MyBot1.py', 'MyBot2.py']
    results = {}
    for bot in bots:
        results[bot] = {}
    
    i=0
    
    for bot in bots:
        for map in maps:
            i+=1
            result = runTest(bot, map)
            results[bot][map] = result
            if result == 1:
                wins +=1
            elif result == 2:
                losses += 1
            elif result == -1:
                timeouts += 1
            elif result == 0:
                ties += 1
                
            if i % 5 == 0:
                print i
            
    f = open(folder + '\\bot-map-results.txt', 'w')
    
    for bot in results:
        success = 100.0 * sum([1 if results[bot][map] == 1 else 0 for map in results[bot]]) / len(results[bot])
        print bot, success
        f.write(bot + ' : ' + str(success) + '\n')
        
    print 'wins: ', wins
    print 'losses: ', losses
    print 'timeouts: ', timeouts
    print 'ties: ', ties
    
    f.write('wins: ' + str(wins) + '\n')
    f.write('losses: ' + str(losses) + '\n')
    f.write('timeouts: ' + str(timeouts) + '\n')
    f.write('ties: ' + str(ties) + '\n')
    
    for bot in results:
        for map in results[bot]:
            f.write('\t'.join([bot.split('/')[-1].split('.')[0], map.split('/')[-1].split('.')[0], str(results[bot][map])]) + '\n')
    f.close()
    
def test(botName, mapId):
    map = maps[mapId]
    bot = 'example_bots/' + botName + '.jar'
    
    command = COMMAND_STRING % (map, my_bot, bot) + '> playGameOutput.txt'
    os.system(command)
#    fi, fo, fe = os.popen3(command)
 #   lines = [line for line in fe.readlines() if len(line) > 1]
  #  print lines
  
def multiTest():
    global bots
    global maps
    
    bots.remove('example_bots/RandomBot.jar')
    
    from multiprocessing import Pool
    pool = Pool(processes = 6)
    results = pool.map(runTestMulti, [(bot, map) for bot in bots for map in maps])
    wins = sum([1 if r == 1 else 0 for r in results])
    losses = sum([1 if r == 2 else 0 for r in results])
    timeouts = sum([1 if r == -1 else 0 for r in results])
    ties = sum([1 if r == 0 else 0 for r in results])
    
    print 'wins: ', wins
    print 'losses: ', losses
    print 'timeotus: ', timeouts
    print 'ties: ', ties
    
def main():
    #runTest(bots[random.randint(0, len(bots)-1)], maps[random.randint(0, len(maps)-1)])
    #runWithVisualization(bots[1], maps[10])
    successTest(100)
    #multiTest()
    
if __name__ == "__main__":
    main()