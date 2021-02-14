
class StateMachine:
    def __init__(self):
        self.State = 0

    def SetState(self,NewState):
        self.State = NewState

    def GetState(self):
        return self.State