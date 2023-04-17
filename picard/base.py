from typing import TypeVar, Generic, Optional, List


T = TypeVar('T')


class State(Generic[T]):
    def __init__(self, init_value: T, state_collection: Optional[List] = None):
        self.value: T = init_value
        self.changed = True
        if state_collection:
            state_collection.append(self)
    
    def get(self):
        self.changed = False
        return self.value

    def set(self, new_value: T):
        # Check change
        if type(self.value) == type(new_value):
            if type(self.value) in [list, tuple]:
                if len(self.value) == len(new_value):
                    for before, after in zip(self.value, new_value):
                        if before != after:
                            self.changed = True
                            break
                else:
                    self.changed = True
            elif type(self.value) == dict:
                if len(self.value) == len(new_value):
                    for k, v in self.value.items():
                        if k not in new_value or v != new_value[k]:
                            self.changed = True
                            break
                    for k, v in new_value.items():
                        if k not in self.value:
                            self.changed = True
                            break
                else:
                    self.changed = True
            elif type(self.value) == set:
                if len(self.value) == len(new_value):
                    for before in self.value:
                        if before not in new_value:
                            self.changed = True
                            break
                    for after in new_value:
                        if after not in self.value:
                            self.changed = True
                            break
                else:
                    self.changed = True
            else:
                if new_value != self.value:
                    self.changed = True
        else:
            self.changed = True
        
        # If something changed, update the value
        if self.changed:
            self.value = new_value

