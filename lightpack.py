import socket, time, imaplib, re, sys

class lightpack:

#    host = '127.0.0.1'    # The remote host
#    port = 3636              # The same port as used by the server
#    apikey = 'key'          # Secure API key which generates by Lightpack software on Dev tab
#    ledMap = [1,2,3,4,5,6,7,8,9,10]     #mapped LEDs
    
    def __init__(self, _host, _port, _ledMap = None, _apikey = None):
        self.host = _host
        self.port = _port
        self.ledMap = _ledMap if _ledMap is not None else []
        self.apikey = _apikey        
    
    def __readResult(self):    # Return last-command API answer  (call in every local method)
        total_data=[]
        data = self.connection.recv(8192)
        total_data.append(data)
        return ''.join(total_data)
        
    def getProfiles(self):
        cmd = 'getprofiles\n'
        self.connection.send(cmd)
        profiles = self.__readResult()
        return profiles.split(':')[1].rstrip(';\n').split(';')        
        
    def getProfile(self):
        cmd = 'getprofile\n'
        self.connection.send(cmd)
        profile = self.__readResult()
        profile = profile.split(':')[1]
        return profile
        
    def getStatus(self):
        cmd = 'getstatus\n'
        self.connection.send(cmd)
        status = self.__readResult()
        status = status.split(':')[1]
        return status

    def getCountLeds(self):
        cmd = 'getcountleds\n'
        self.connection.send(cmd)
        count = self.__readResult()
        count = count.split(':')[1]
        return int(count)
        
    def getLeds(self):
        cmd = 'getleds\n'
        self.connection.send(cmd)
        leds = self.__readResult()
        leds = leds.split(':')[1].split(';')
        leds2=[]
        self.ledMap[:] = []
        for led in leds:
            if led.isspace():
                continue
            leds2.append(led)
            self.ledMap.append(int(led.split('-')[0]))
        return leds2
        
    def getLedMap(self):
        cmd = 'getleds\n'
        self.connection.send(cmd)
        leds = self.__readResult()
        leds = leds.split(':')[1].split(';')
        self.ledMap[:] = []
        for led in leds:
            if led.isspace():
                continue
            self.ledMap.append(int(led.split('-')[0]))
        return self.ledMap
    
    def getScreenSize(self):
        cmd = 'getscreensize\n'
        self.connection.send(cmd)
        screen = self.__readResult()
        screen = screen.split(':')[1]
        return screen
    
    def getAPIStatus(self):
        cmd = 'getstatusapi\n'
        self.connection.send(cmd)
        status = self.__readResult()
        status = status.split(':')[1]
        return status
        
    def sendApikey(self):
        if self.apikey is not None:
            cmd = 'apikey:' + str(self.apikey) + '\n'
        else:
            cmd = 'apikey:\n'
        self.connection.send(cmd)
        return self.__readResult()
        
    def connect (self):
        try:     #Try to connect to the server API
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.host, self.port))            
            self.__readResult()
            self.sendApikey()
            self.getLeds()
            return 0
        except:
            print 'Lightpack API server is missing'
            print sys.exc_info()[0]
            return -1
        
    def setColor(self, n, r, g, b):     # Set color to the define LED        
        cmd = 'setcolor:{0}-{1},{2},{3}\n'.format(n, r, g, b)
        self.connection.send(cmd)
        self.__readResult()
        
    def setColorToAll(self, r, g, b):     # Set one color to all LEDs
        cmdstr = ''
        for i in self.ledMap:
            cmdstr = str(cmdstr) + str(i) + '-{0},{1},{2};'.format(r,g,b)        
        cmd = 'setcolor:' + cmdstr + '\n'            
        self.connection.send(cmd)
        self.__readResult()
        
    def updateColors(self, leds):
        cmdstr = ''
        for led in leds:
            index = led[0]
            rgb = led[1]
            cmdstr = str(cmdstr) + str(index) + '-{0},{1},{2};'.format(rgb[0], rgb[1], rgb[2])
        cmd = 'setcolor:' + cmdstr + '\n'            
        self.connection.send(cmd)
        self.__readResult()
        
    #for compatibility with older plugins
    #replaced QColor objects with an int list
    def setFrame(self, leds):
        cmdstr = ''
        for i, led in enumerate(leds):
            cmdstr = str(cmdstr) + str(i+1) + '-{0},{1},{2};'.format(led[0], led[1], led[2])
        cmd = 'setcolor:' + cmdstr + '\n'            
        self.connection.send(cmd)
        self.__readResult()

    def setGamma(self, g):
        cmd = 'setgamma:{0}\n'.format(g)
        self.connection.send(cmd)
        self.__readResult()        
        
    def setSmooth(self, s):
        cmd = 'setsmooth:{0}\n'.format(s)
        self.connection.send(cmd)
        self.__readResult()

    def setBrightness(self, s):
        cmd = 'setbrightness:{0}\n'.format(s)
        self.connection.send(cmd)
        self.__readResult()

    def setProfile(self, p):
        #cmd = 'setprofile:{0}\n'.format(p)
        cmd = 'setprofile:%s\n' % p
        self.connection.send(cmd)        
        self.__readResult()
        
    def lock(self):
        cmd = 'lock\n'
        self.connection.send(cmd)
        result = self.__readResult()
        result = result.strip()
        return result == 'lock:success'
        
    def unlock(self):
        cmd = 'unlock\n'
        self.connection.send(cmd)    
        result = self.__readResult()
        result = result.strip()
        return result == 'unlock:success'
    
    def turnOn(self):
        cmd = 'setstatus:on\n'        
        self.connection.send(cmd)
        self.__readResult()
    
    def turnOff(self):
        cmd = 'setstatus:off\n'
        self.connection.send(cmd)
        self.__readResult()        

    def disconnect(self):
        self.unlock()
        self.connection.close()
        
