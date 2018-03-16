from basicView import QuestionInterface



class NsrView(QuestionInterface):
    def __init__(self, Product, logic, childView=None, childLogic=None, buffer=''):
        super(NsrView,self).__init__(Product, logic, 
                                     childView=childView, 
                                     childLogic=childLogic,
                                     buffer=buffer)

    def next(self,B):
        if type(self.logic.Q.effect[B]) == bool:
            self.logic.state = self.logic.Q.effect[B]
        if B == 'y':
            self.logic.Q = self.logic.Q.posChild
        elif B == 'n':
            self.logic.Q = self.logic.Q.negChild
        if self.logic.Q is None:
            self.finalize()

