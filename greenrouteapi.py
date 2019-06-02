import vincenty
import math
import requests
import polyline
import json

API_KEY = "ayaya"

emissionsData = {'MidSedCV':[(-5, 2.21), (0, 3.21), (5, 6.11)], 'MidSedHEV':[(-5, 0.06), (0, 1.98), (5, 4.9)], 'SUVCV':[(-5, 3.07), (0, 4.32), (5, 8.32)], 'SUVHEV':[(-5, 0.15), (0, 3), (5, 7.03)]}

def applyAlgo(emissionsData):
    algodData = {}
    for car in list(emissionsData.keys()):
        p1, p2, p3 = [x[1] for x in emissionsData[car]]
        d = (p1*p3-p2**2)/(p3-2*p2+p1)
        c = p2-d
        a = ((p3-d)/(p2-d))**0.2
        algodData[car] = [d, c, a]
    return algodData

algodData = applyAlgo(emissionsData)

def carbonFunction(distance, slope, data):
    grade = 100*slope
    galpermile = (data[1]*data[2]**grade+data[0])/100
    return [galpermile*(distance*0.621371)*8887, 1/galpermile]

def distcarb(points, elevations, data):
    # carbonFunction = f(grade)=km/L
    lenTotal = 0
    carbon = 0
    avgmpg = 0
    # vincenty's formula with height approximation using exponential moving averages to smooth data
    lastEMA = sum([(elevations[i]-elevations[i+1])/(math.sqrt(vincenty.vincenty(points[i], points[i+1])**2+((elevations[i]-elevations[i+1])/1000)**2)*1000) for i in range(0, 3)])/3
    for i in range(0, len(points)-2):
        dist = math.sqrt(vincenty.vincenty(points[i], points[i+1])**2+((elevations[i]-elevations[i+1])/1000)**2)
        lastEMA = (elevations[i+1]-elevations[i])/(dist*1000)*(0.125)+lastEMA*(0.875)
        dcarbon, mpg = carbonFunction(dist, lastEMA, data)
        carbon += dcarbon
        avgmpg += mpg*dist
        lenTotal += dist
    return [lenTotal, carbon, avgmpg/lenTotal]

def greenroutealgo(location1, location2, carType):
    directionsAPIData = json.loads(requests.get("https://maps.googleapis.com/maps/api/directions/json?origin="+location1.replace(' ', '+')+"&destination="+location2.replace(' ', '+')+"&alternatives=true&key="+API_KEY).text)
    routes = directionsAPIData['routes']
    statistics = []
    for route in routes:
        points = route['overview_polyline']['points']
        elevationsJSON = json.loads(requests.get("https://maps.googleapis.com/maps/api/elevation/json?path=enc:"+points+"&samples="+str(int(route['legs'][0]['distance']['value']/100))+"&key="+API_KEY).text)
        elevations = [x['elevation'] for x in elevationsJSON['results']]
        carData = algodData[carType]
        pointsd = [(x['location']['lat'], x['location']['lng']) for x in elevationsJSON['results']]
        statistics.append(distcarb(pointsd, elevations, carData))

    minCarbon = 9999999999999999999
    minRoute = -1
    maxCarbon = 0
    maxcs = 0
    for each in statistics:
        minRoute += 1
        if each[1] < minCarbon:
            minCarbon = each[1]
            avgmpg = each[2]
            break
    for each in statistics:
        if each[1] > maxCarbon:
            maxCarbon = each[1]
    return {"startAddress":routes[minRoute]['legs'][0]['start_address'],\
                      "endAddress":routes[minRoute]['legs'][0]['end_address'],\
                      "distance":routes[minRoute]['legs'][0]['distance']['text'],\
                      "time":routes[minRoute]['legs'][0]['duration']['text'],\
                      "carbon":minCarbon,\
                      "averagempg":avgmpg,\
                      "maxcarbonsaved":maxCarbon-minCarbon,\
                      "directions":[x['html_instructions'] for x in routes[minRoute]['legs'][0]['steps']],\
                      "path":polyline.decode(routes[minRoute]['overview_polyline']['points'])}
