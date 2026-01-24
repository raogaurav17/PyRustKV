class KVStore():
    """ 
    In memory key value store
    """
    
    def __init__(self, capacity: int = 100):
        super().__init__()
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        self.capacity = capacity
        self._store = {}
        
    def put(self, key, value):
        self._store[key] = value
        if len(self._store) > self.capacity:
            self._store.pop(next(iter(self._store)))   
        
    def get(self, key):
        return self._store.get(key)

    def delete(self, key):
        self._store.pop(key, None)
        
        