"""Test Python sample"""
import pycan

class ParentClass:
    _parentclass:bool = False
    def __init__(self, parentClassInit:bool = False):
        self._parentclass = parentClassInit
        pass

class derivedClassFromParent(ParentClass):
    def __init__(self, parentClassInit = False):
        super().__init__(parentClassInit)

class Reverse:
    def __init__(self, data: str=""):
        self._data = data
        self.len = len(data)
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.len == 0:
            raise StopIteration
        self.len = self.len - 1
        return self._data[self.len]
    
def main():
    itr = Reverse("Hello")
    print(itr)
    for i in itr:
        print(i)
    
if __name__ == "__main__":
    main()
