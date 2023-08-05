from copy import copy, deepcopy

class Stack():
    def __init__(self):
        self._stack = []

    '''
    Return True is stack is empty; False otherwise
    '''
    def is_empty(self):
        return self._stack == []
    
    '''
    Pop item from the top of stack and return
    '''
    def pop(self):
        if not self.is_empty():
            return self._stack.pop()
        else:
            return None

    '''
    Push item onto stack. Always goes to the top
    '''
    def push(self,item):
        self._stack.append(item)

    '''
    Return item at top of stack. Does not remove from stack
    '''
    def peek(self):
        if not self.is_empty():
            return self._stack[-1]
        else:
            return None

    def __len__(self):
         return len(self._stack)

    # Taken from: https://stackoverflow.com/questions/1500718/how-to-override-the-copy-deepcopy-operations-for-a-python-object
    def __deepcopy__(self,memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k,v in self.__dict__.items():
            setattr(result,k,deepcopy(v,memo))
        return result