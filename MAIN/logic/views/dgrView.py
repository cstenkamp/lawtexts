from basicView import QuestionInterface


class DgrView(QuestionInterface):
    def __init__(self, Product, logic, childView=None, childLogic=None, buffer='',parentLogic=None):
        super(DgrView,self).__init__(Product, logic, 
                                     childView=childView,
                                     childLogic=childLogic,
                                     buffer=buffer,
                                     parentLogic=parentLogic)

        self.logic.initQuestions()
        self.hide()

    def next(self,B):
        if type(self.logic.Q.effect[B]) is bool:
            self.logic.setState(self.logic.Q.effect[B])

        if (B == 'y'):
            self.logic.Q = self.logic.Q.posChild
        elif (B == 'n') :
            self.logic.Q = self.logic.Q.negChild

        if not self.logic.Q is None:
            self.updateView(self.logic.Q.text)
        else:
            self.finalize() 


    def finalize(self):
        self.close()
        html = self.logic.finalize()