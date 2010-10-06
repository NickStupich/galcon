import math

def getDistance(mapId):
    filename = 'maps/map%s.txt' % str(mapId)
    f = open(filename)
    
    for line in f:
        parts = line.split()
        if parts[3] == '1':
            planet1 = (float(parts[1]), float(parts[2]))
        elif parts[3] == '2':
            planet2 = (float(parts[1]), float(parts[2]))
            
    f.close()
    
    distance = math.ceil(math.sqrt((planet1[0] - planet2[0]) ** 2.0 + (planet1[1] - planet2[1]) ** 2.0))
    
    return distance

def main():
    distances = []
    for i in range(1, 101):
        distance = getDistance(i)
        distances.append(distance)
        if distance < 10:
            print i, distance
        
    print '\n'
    print 'mean distance: ' + str(1.0 * sum(distances) / len(distances))
    print 'min : ' + str(min(distances))
    print 'max : ' + str(max(distances))
    
    

    
if __name__ == "__main__":
    main()