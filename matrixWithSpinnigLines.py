# Drives 16 x 16  matrix using an algoritm that adds random lines 
# The background gets moved off to one edge
#
#

flagPi = True
flagInit = True


import math
import random
import time
if flagPi:
    from dotstar import Adafruit_DotStar


# ----------------------------------------------------------

def dot(v,w):
    x,y,z = v
    X,Y,Z = w
    return x*X + y*Y + z*Z
  
def length(v):
    x,y,z = v
    return math.sqrt(x*x + y*y + z*z)
  
def vector(b,e):
    x,y,z = b
    X,Y,Z = e
    return (X-x, Y-y, Z-z)
  
def unit(v):
    x,y,z = v
    mag = length(v)
    return (x/mag, y/mag, z/mag)
  
def distance(p0,p1):
    return length(vector(p0,p1))
  
def scale(v,sc):
    x,y,z = v
    return (x * sc, y * sc, z * sc)
  
def add(v,w):
    x,y,z = v
    X,Y,Z = w
    return (x+X, y+Y, z+Z)

#
# http://www.fundza.com/vectors/point2line/index.html
# Given a line with coordinates 'start' and 'end' and the
# coordinates of a point 'pnt' the proc returns the shortest 
# distance from pnt to the line and the coordinates of the 
# nearest point on the line.
#
# 1  Convert the line segment to a vector ('line_vec').
# 2  Create a vector connecting start to pnt ('pnt_vec').
# 3  Find the length of the line vector ('line_len').
# 4  Convert line_vec to a unit vector ('line_unitvec').
# 5  Scale pnt_vec by line_len ('pnt_vec_scaled').
# 6  Get the dot product of line_unitvec and pnt_vec_scaled ('t').
# 7  Ensure t is in the range 0 to 1.
# 8  Use t to get the nearest location on the line to the end
#    of vector pnt_vec_scaled ('nearest').
# 9  Calculate the distance from nearest to pnt_vec_scaled.
# 10 Translate nearest back to the start/end line. 
# Malcolm Kesson 16 Dec 2012
  
def pnt2line(pnt, start, end):
    line_vec = vector(start, end)
    pnt_vec = vector(start, pnt)
    line_len = length(line_vec)
    line_unitvec = unit(line_vec)
    pnt_vec_scaled = scale(pnt_vec, 1.0/line_len)
    t = dot(line_unitvec, pnt_vec_scaled)    
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = scale(line_vec, t)
    dist = distance(nearest, pnt_vec)
    nearest = add(nearest, start)
#    return (dist, nearest)
    return (dist)
    

# ----------------------------------------------------------

numpixels = 3*300+255+256 # Number of LEDs in strip + disk + square
#for i in range( numpixels ):
#    pixels.append( 0 )

maxLEDintensity = 64;
mindist = 0.5 # Min distance for LED relative to line function that is ysed to set intensity 0.1 to 1 is reasonable

 
 
if flagPi:        
    strip   = Adafruit_DotStar(numpixels, 4000000) # 4 MHz is more reliable
    strip.begin()           # Initialize pins for output
    strip.setBrightness(maxLEDintensity) # Limit brightness to ~1/4 duty cycle




# Set up xy positions of each point
matrixLEDxy = []
matrixLEDintensity = []
matrixLEDcurrent = []

ll = [-7.5,-6.5,-5.5,-4.5,-3.5,-2.5,-1.5,-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5]
for i in range(16):
    for j in range(16):
        matrixLEDintensity.append( 0 )
        matrixLEDcurrent.append( 0 )
        matrixLEDxy.append( [ll[i],ll[j],0] )
        
# Set up the LED APA102 index corresponding to the matrix
# Must take account of snake pattern
matrixLEDindexOffset = 3*300+255
matrixLEDindex = []
for i in range(16):
    for j in range(16):
        if (i%2)==0: # Take account of snake pattern
            matrixLEDindex.append( matrixLEDindexOffset + i*16+j )
        else:
            matrixLEDindex.append( matrixLEDindexOffset + i*16+(15-j) )



# RINGS SETUP

rings = [
    [254,254],  #0 - Center point
    [248,253],  #1
    [236,247],  #2
    [216,235],  #3
    [192,215],  #4
    [164,191],  #5
    [132,163],  #6
    [92,131],   #7
    [48,91],    #8
    [0,47],     #9 - Outer-most ring
]


#
## Set up xy positions of each point
#matrixLEDxy = []
#matrixLEDintensity = []
#matrixLEDcurrent = []
#
#ll = [-7.5,-6.5,-5.5,-4.5,-3.5,-2.5,-1.5,-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5]
#for i in range(16):
#    for j in range(16):
#        matrixLEDintensity.append( 0 )
#        matrixLEDcurrent.append( 0 )
#        matrixLEDxy.append( [ll[i],ll[j],0] )
#



              
                            
                                          
                                                        
                                                                      
                                                                                                  
# Use this variable to cycle global colors                
colscale = 1 # 1, 256 or 256^2 to set b , r, or g  



# ===============================================================


while True:
    
        
    if random.random()>0.998: # Change global color every ~2000 cycles
        # print "Set Color"
        colscale = colscale * 256
        if colscale > 256*256:
            colscale = 1
                
                
# --------------------------------------------------------
# 16 x 16 MATRIX
# --------------------------------------------------------
                                
    # Move the current LED levels one to the left, and decrease the intensity level
    if True: # Rolls downwards
        for i in range(16):
            for j in range(15,0,-1):
                matrixLEDcurrent[16*i+j] = max(  0 , int(math.floor( 0.9 * matrixLEDcurrent[16*(i)+(j-1)] )) ) # Decrease intensity
                # matrixLEDcurrent[16*i+j] = max(  0 ,  matrixLEDcurrent[16*(i)+(j-1)] -10 ) # Decrease intensity
            j=0
            matrixLEDcurrent[ 16*i+j ] = 0
    else: # Rolls upwards
        for i in range(16):
            for j in range(15):
                matrixLEDcurrent[16*i+j] = max(  0 , int(math.floor( 0.5 * float( matrixLEDcurrent[16*(i)+(j+1)] ) )) ) # Decrease intensity
                # matrixLEDcurrent[16*i+j] = max(  0 ,  matrixLEDcurrent[16*(i)+(j+1)] -10 ) # Decrease intensity
            j=15
            matrixLEDcurrent[ 16*i+j ] = 0


    if random.random() < 1.0 : # Determined how often new line comes in x% of time  
        if False: # True - random position, 
            # Pick a line with two random end points
            start = [ 16.*random.random()-8. , 16.*random.random()-8. , 0 ] 
            end = [ 16.*random.random()-8. , 16.*random.random()-8. , 0 ]

        elif True: # True - random position on larger canvas, 
            # Pick a line with two random end points
            start = [ 32.*random.random()-16. , 32.*random.random()-16. , 0 ] 
            end = [ 32.*random.random()-16. , 32.*random.random()-16. , 0 ]

        else: # Simple Diagonal  - fixed line/simple diagnonal
            start = [ -7.5 , -7.5 , 0 ] 
            end = [ 7.5 , 7.5 , 0 ]
                        
        # Create LED intensity map based on distance from line
        for i in range(16):
            for j in range(16):
                d = max(mindist , pnt2line( matrixLEDxy[16*i+j] , start, end ) ) 
                matrixLEDintensity[16*i+j] = int( math.floor( float(maxLEDintensity) * pow( mindist / d , 2. ) ))
    else:
        # Don't add anything new
        for i in range(16):
            for j in range(16):
                matrixLEDintensity[16*i+j] = 0
        
    
    # Add the line intensity to the map and display it
    for i in range(16):
        for j in range(16):
            matrixLEDcurrent[16*i+j] = matrixLEDcurrent[ 16*i+j ] +  matrixLEDintensity[ 16*i+j ] # Store current values
            ## pixels( matrixLEDindex[ 16*i+j] ) = matrixLEDcurrent[ 16*i+j ]
            if flagPi:
                # strip.setPixelColor( matrixLEDindex[ 16*i+j ] , 0 , 0 , matrixLEDcurrent[16*i+j] ) # Write to pixel o/p, g,r,b
                strip.setPixelColor( matrixLEDindex[ 16*i+j ] , colscale * matrixLEDcurrent[16*i+j] ) # Write to pixel o/p, g,r,b
 
# --------------------------------------------------------
# DISK
# --------------------------------------------------------




# --------------------------------------------------------
# STRIP
# --------------------------------------------------------


 #----- Rest of Strip
    pixstart = 0
#    pixstop = pixstart+3*300  # Just strip
    pixstop = pixstart+3*300+255 # Strip and disk 
    pixlistall = list( range(pixstart,pixstop) )
    pixlistbad = [593,594]
    pixlistgood = [item for item in pixlistall if item not in pixlistbad ] # Remove bad pixels

    for i in [item for item in range(pixstart,pixstop,1) if item not in pixlistbad]:
        x = 5 + int(math.floor(pow( random.random() , 20. )  * float(maxLEDintensity) ))
        x = min( maxLEDintensity , x )
        # strip.setPixelColor(i, 0 , 0 , x ) # blue
        strip.setPixelColor(i, colscale * x ) # blue

 
#    print matrixLEDcurrent    
    if flagPi:
        strip.show()                     # Refresh strip
    else:
        print "----------"
        print matrixLEDcurrent    

    time.sleep(0.01 )    
