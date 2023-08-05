"""
Generic.py
Versatile object which behaves both likea dictionary and like a class.
Hans Buehler, ~2014
"""

class Generic(object):
    """ An object which can be used as a generic store.
        It allows 
        
        Constructions by keyword:
        
            g = Generic(a=1, b=2, c=3)
            
            
        Access by key
        
            a = g.a
            a = g['a']
            e = g.get('e',None)   # with default
            e = g('e',None)       # with default
            
            del g.e
            
    Hans Buehler, 2013
    """
    
    def __init__(self, **kwargs):
        """ Initialize object; use keyword notation such as
                Generic(a=1, b=2)
        """
        self.__dict__.update(kwargs)
    
    # make it behave like a dictionary    
    
    def __str__(self):
        return self.__dict__.__str__()
    
    def __repr__(self):
        return self.__dict__.__repr__()
    
    def __getitem__(self,key):
        return self.__dict__.__getitem__(key)
    
    def __setitem__(self,key,value):
        self.__dict__.__setitem__(key,value)
        
    def __delitem__(self,key):
        self.__dict__.delitem(key)

    def __iter__(self):
        return self.__dict__.__iter__()
    
    def __contains__(self, key):
        return self.__dict__.__contains__(key)
    
    def keys(self):
        return self.__dict__.keys()

    def get(self, key, *kargs):
        """ like dict.get() """
        if len(kargs) == 0 or key in self:
            return self[key]
        if len(kargs) != 1: raise ValueError("get(): no or one argument expected; found %ld arguments", len(kargs))
        return kargs[0]
    
    
    