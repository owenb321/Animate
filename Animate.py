import math
import random
import lightpack
import ConfigParser
import os
import threading
import time

class Animate:
    def __init__(self):
        self.loadConfig()
        self.ConnectToLightpack()
        self.getLedMap()
        self.getCylonMap()
        
        self.animFunctions = {
            1: self.Animation1,
            2: self.Animation2,
            3: self.SnakeAnimation,
            4: self.CylonAnimation
        }
        self.i = 0 #init animation index
        random.seed()
        print 'init'
        
    def loadConfig(self):
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.scriptDir + '/Animate.ini')
        self.animType = self.config.getint('Animation', 'type')
        
    def ConnectToLightpack(self):
        try:
            self.host = self.config.get('Lightpack', 'host')
            self.port = self.config.getint('Lightpack', 'port')
            self.lpack = lightpack.lightpack(self.host, self.port)
            self.lpack.connect()
            return True
        except: return False

    def dispose(self):
        self.timeranim.stop()
        del self.timeranim
        self.lpack.unlock()

    def run(self):
        if self.lpack.lock() :
            self.lpack.turnOn()
            self.onAnimationChange()
            while True:
                self.animFunctions[self.animType]()
                time.sleep(self.animInterval)
            print 'run'
        
    def stop(self):
        self.timeranim.stop()
        self.lpack.unlock()
        
    def getCylonMap(self):
        try:
            map = self.config.get('Lightpack', 'cylonmap')
            ledGroups = [group.strip() for group in map.split(';')]
            self.cylonMap = []
            for group in ledGroups:
                self.cylonMap.append([int(n) for n in group.split(',')])
        except ConfigParser.NoOptionError:
            self.cylonMap = [ [1,2,3], [4,5], [6,7], [8,9,10] ]
        
    def getLedMap(self):
        try:
            map = self.config.get('Lightpack', 'ledmap')
            self.ledMap = [int(n) for n in map.split(',')]
        except ConfigParser.NoOptionError:
            self.ledMap = self.defaultMap()

    def defaultMap(self):
        try:
            leds = self.lpack.getCountLeds()
            map = [n for n in range (1, leds+1)]
        except Exception, e:
            print(str(e))
            map = [1,2,3,4,5,6,7,8,9,10]
        return map

    def Animation1(self):
        try:
            self.i = self.i+1
            leds = self.lpack.getCountLeds()
            for k  in range (0, leds):
                t = float(self.i/4 - k*2)/10
                r = int((math.sin(t)+1)*127)
                g = int((math.cos(t*0.7)+1)*127)
                b = int((math.cos(1.3 + t*0.9)+1)*127)
                self.lastFrame[self.ledMap[k]-1]=[r,g,b]
            self.lpack.setFrame(self.lastFrame)
            self.i += 1
        except Exception, e:
            print(str(e))

    def Animation2(self):
        try:
            self.i = self.i+1
            self.lastFrame
            newFrame = self.lastFrame
            leds = self.ledsCount
            att = 0.95
            for k  in range (0, leds):
                if random.randrange(100) < 10 :
                    r = random.randrange(255)
                    g = random.randrange(255)
                    b = random.randrange(255)
                else :
                    r = int(newFrame[k][0] * att)
                    g = int(newFrame[k][1] * att)
                    b = int(newFrame[k][2] * att)

                newFrame[k] = [r,g,b]
            self.lpack.setFrame(newFrame)
            self.lastFrame = newFrame
            self.i += 1
        except Exception, e:
            print(str(e))

    def SnakeAnimation(self):
        for k in range (0, self.ledsCount) :    
            idx = (self.i+k) % self.ledsCount
            if k < 3 :
                self.lastFrame[self.ledMap[idx]-1]=[255,0,0]
            else :
                self.lastFrame[self.ledMap[idx]-1]=[0,0,125]
        self.lpack.setFrame(self.lastFrame)
        self.i += 1

    def CylonAnimation(self):
        for k in self.cylonMap: 
            idx = self.cylonMap.index(k)
            cyclePhase = self.i % self.cylonCycleLength 
            if (cyclePhase > self.cylonWidth-1 and idx == 2*(self.cylonWidth-1) - cyclePhase) or (idx == cyclePhase):
                for i in k:
                    self.lastFrame[i-1]=[255,0,0]
            else:
                for i in k:
                    self.lastFrame[i-1]=[0,0,0]
        self.lpack.setFrame(self.lastFrame)
        self.i += 1

    def onAnimationChange(self):
        self.ledsCount = int(self.lpack.getCountLeds())
        self.lastFrame=[ [0,0,0] for k in range(0, self.ledsCount)]
        if self.animType == 1: #Animation1
            self.animInterval = 0.07
            self.i=self.ledsCount*2 + random.randrange(20000)

        elif self.animType == 2: #Animation2
            self.animInterval = 0.2

        elif self.animType == 3: #SnakeAnimation
            self.animInterval = 0.2

        elif self.animType == 4: #CylonAnimation
            self.animInterval = 0.2
            self.cylonWidth = len(self.cylonMap)
            self.cylonCycleLength = self.cylonWidth*2 - 2
        """ default function """

animate = Animate()
animate.run()