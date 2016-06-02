'''
Created on Jun 2, 2016

@author: KJNETHER
'''
import requests
import os.path
import json
import pprint

class RouteLiquor(object):
    
    def __init__(self, points):
        self.points = points
        self.routerUrl = 'https://routertst.api.gov.bc.ca/'
        self.routeToken = '539058c1a33e47d982df47c964788d6c'
        if self.routerUrl[-1] == '/':
            self.routerUrl = self.routerUrl[:-1]
        self.returnFormat = 'json'
        self.initialRoute = None
        self.initalrouteBB = None
        self.liquorStoreFile = 'liquorStoreloc.json'
        self.bbExpansionFact = 5000
        self.liquorInBB = None
        self.resultKml = 'result.kml'
        
    def calcInitialRoute(self, points, returnType=None) :
        self.points = points
        request = self.getRoute(points, returnType)
        self.initialRoute = request.json()
        #print self.initialRoute
        
    def getRoute(self, points=None, returnType=None):
        if not points:
            points = self.points
        print 'points', points
        if not returnType:
            returnType = self.returnFormat
        print 'returnType', returnType
        # convert points to strings
        strPnt = []
        for pnt in points:
            strPnt.append(str(pnt))
        #points = '{0},{1}'.format(location1,location2 )
        routeUrl = self.routerUrl + r'/route.' + returnType
        print 'points', ','.join(strPnt)
        params = {'points': ','.join(strPnt), 
                  'criteria':'fastest',
                  'distanceUnit':'km',
                  'apikey':self.routeToken,
                  'outputFormat': returnType}
        print 'routeUrl', routeUrl
        #req = requests.Request('GET',routeUrl ,params=params)
        #prepared = req.prepare()
        #print prepared

        
        
        request = requests.get(routeUrl, params=params, verify=False)
        #print 'request.text', request.text
        return request
        
    def getBB(self, buffer=None):
        if not self.initialRoute:
            self.getRoute()
        minX = 0
        minY = 0
        maxX = 0
        maxY = 0
        for point in self.initialRoute['route']:
            if not minX:
                minX = point[0]
                maxX = point[0]
                minY = point[1]
                minY = point[1]
            else:
                if point[0] <  minX:
                    minX =  point[0]
                if point[0] > maxX:
                    maxX = point[0]
                if point[1] < minY:
                    minY = point[1]
                if point[1] > minY:
                    maxY = point[1]
        bb = [minX, minY, maxX, maxY]
        print 'bb = ', bb
        self.initalrouteBB = bb
        return [minX, minY, maxX, maxY]
    
    def getMeTheLiquor(self, bb=None):
        inBB = []
        if not bb:
            bb = self.initalrouteBB
        liquoreStoreFilePath =  os.path.join('..', self.liquorStoreFile)
        if not os.path.exists(liquoreStoreFilePath):
            liquoreStoreFilePath =  os.path.join('.', self.liquorStoreFile)
        # slurp the whole file into json 
        fh = open(liquoreStoreFilePath, 'r')
        jsonObj = json.loads(fh.read())
        
        for lq in jsonObj:
            x = lq['X']
            y = lq['Y']
            if x >= bb[0] and x <= bb[2] and\
               y >= bb[1] and y <= bb[3]:
                inBB.append(lq)
        if not inBB:
            bb = [bb[0] - self.bbExpansionFact, 
                    bb[1] - self.bbExpansionFact,
                    bb[2] + self.bbExpansionFact, 
                    bb[3] + self.bbExpansionFact]
            self.getMeTheLiquor(bb)
        else:
            self.liquorInBB = inBB
            
    def getClosestLiquorStore(self):
        return self.liquorInBB[0]
    
    def getBestRoute(self, liquorStoreObj=None):
        # insert the point in betwen the first two
        newPoints = self.points
        closestLiquor = self.getClosestLiquorStore()
        x = closestLiquor['X']
        y = closestLiquor['Y']
        print 'x and y are', x, y
        newPoints.insert(2, y)
        newPoints.insert(2, x)
        print 'newPoints', newPoints
        result = self.getRoute(newPoints, returnType='kml')
        #print 'result', result
        #print 'json', result.json
        kmlPath = os.path.join('..', self.resultKml)
        print 'writing', kmlPath
        fh = open(kmlPath, 'w')
        #print 'raw', result.text
        fh.write(result.text)
        fh.close()
           

if __name__ == '__main__':
    testpoints = [-126.844567, 49.97859, -122.799997, 58.925305]
    
    #[-126.844567,51.6393772,-121.2961254,49.97859,-122.799997,58.925305]
    #testpoints = [-126.844567, 51.6393772, -125.2961254, 50.9785, -122.799997, 58.925305]
    #testpoints = [-126.844567, 49.97859, -121.2884938, 51.6623911] 

    #testpoints = [-126.844567, 49.97859, -122, 50, -122.799997, 58.9
    rl = RouteLiquor(testpoints)
    rl.calcInitialRoute(testpoints)
    rl.getBB()
    #rl.initalrouteBB = [-126.88998714588554, 49.18895827656146, -121.0050980598874, 58.916394807567855]
    rl.getMeTheLiquor()
    rl.getBestRoute()
        
        