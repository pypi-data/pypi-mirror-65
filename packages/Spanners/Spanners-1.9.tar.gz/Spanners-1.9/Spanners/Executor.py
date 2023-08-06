#!/usr/bin/env python3

import os,re,sys

from time import sleep
from functools import wraps

#_________________________________________________
def getRoot(fn):
    #print 'fn=', fn, ', name=', fn.__name__
    while hasattr(fn,'func_closure') and fn.func_closure:
        #print 'fn.func_closure=', fn.func_closure
        if len(fn.func_closure) == 0:
            break
        fn = fn.func_closure[0].cell_contents
    return fn
    
#_________________________________________________
class Executor(object):
    '''
    execution helpers:
    executor = Executor()
    '''
    
    def retry(self,*oargs,**okwargs):
        '''
        retry the enclosed function:
        
        @executor.retry(timeout=5)
        def fnToRetry():   
        '''

        timeout = getattr(okwargs,'timeout',5)
        
        def _wrapit(fn):
            fn = getRoot(fn)
            
            @wraps(fn)
            def _wrapper(*args, **kwargs):
                # execution
                while True:
                    try:
                        return fn(*args,**kwargs)
                        break
                    except:
                        sys.stderr.write('%s\n'%sys.exc_info()[0])
                        sleep(timeout)
                        
            return _wrapper
                
        if len(oargs) == 0:
            '''
            handle no parentheses
            '''
            def _actualWrapper(fn):
                return _wrapit(fn)
            return _actualWrapper
        else:
            '''
            handle with parentheses
            '''
            fn = oargs[0]
            return _wrapit(fn)

def main():
	global counter
	counter = 5

	executor = Executor()
	
	@executor.retry(timeout=1)
	def increment():
		global counter
		print('counter=%d'%counter)
		counter -= 1
		if counter > 0:
			raise Exception('loop')

	increment()
	
	return

if __name__ == '__main__': main()
