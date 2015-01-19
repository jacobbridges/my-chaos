class array:
    
    def __init__(self, length, value=None):
        self.__data = range(length)
        for index in range(length):
            self.__data[index] = value
            
    def __len__(self):
        return len(self.__data)
    
    def __getitem__(self, key):
        return self.__data[key]
    
    def __setitem__(self, key, value):
        self.__data[key] = value
        
    def __delitem__(self, key):
        self.__data[key] = None
        
    def __iter__(self):
        return iter(self.__data)
    
    def __contains__(self, value):
        return value in self.__data

class matrix:
    
    def __init__(self, rows, columns, value=None):
        self.__data = array(rows)
        for index in range(rows):
            self.__data[index] = array(columns, value)
            
    def __len__(self):
        return len(self.__data) * len(self.__data[0])
    
    def __getitem__(self, key):
        return self.__data[key]
    
    def __setitem__(self, key, value):
        pass
    
    def __delitem__(self, key):
        self.__data[key] = array(len(self.__data[key]))
        
    def __iter__(self):
        return iter(self.__data)
    
    def __contains__(self, value):
        for item in self.__data:
            if value in item:
                return True
        return False
