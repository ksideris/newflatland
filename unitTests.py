import math
import game.vector as vector
import game.environment as environment
import cPickle as pickle
import json
import time

def TestVector():
	tvector = vector.Vector2D((10,10))
	
	assert(tvector.length==math.sqrt(100+100))
	tnorm = tvector.norm()
	assert(tnorm[0]==10/math.sqrt(100+100) and tnorm[1]==10/math.sqrt(100+100) )

def TestEnvironment():
	tenv = environment.Environment()
	for i in range(10):
		tenv.createPlayer(1)
	
	for i in range(10):
		tenv.createBuilding(1)
	start = time.time()
	
	s= tenv.ccSerialize()
	middle = time.time()
	print len(s),len(s.split('$'))-1
	for i in range(len(s.split('$'))-1):
		print s.split('$')[i]
	
	end = time.time()
	print 'serialization:',middle-start
	print 'deserialization:',end-middle

def TestAll():
	TestVector()




if __name__=="__main__":
	TestEnvironment()
