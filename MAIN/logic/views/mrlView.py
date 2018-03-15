from basicView import QuestionInterface



class MrlView(QuestionInterface):
    def __init__(self, Product, logic, childView=None, childLogic=None, buffer=''):
        super(MrlView,self).__init__(Product, logic, 
                                     childView=childView,
                                     childLogic=childLogic,
                                     buffer=buffer)

        self.logic.initQuestions()
        self.hide()




    def next(self,B):
        if type(self.logic.Q.effect[B]) is bool:
            self.logic.setState(self.logic.Q.effect[B])

        if self.logic.Q.effect[B] == 'unvollst':
            self.logic.setType(self.logic.Q.effect[B])
        elif self.logic.Q.effect[B] == 'vollst':
            self.logic.setType(self.logic.Q.effect[B])

        if self.logic.Q.effect[B] == 'harm':
            self.logic.setHarmonized(True)
        elif self.logic.Q.effect[B] == 'nichtHarm':
            self.logic.setHarmonized(False)

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
        #self.clearLayout(self.bottomLayout)
        #self.updateView(html)
        return self.logic.state, self.Product.extraDuties, html