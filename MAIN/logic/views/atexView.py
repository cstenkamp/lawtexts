from basicView import QuestionInterface



class AtexView(QuestionInterface):
    def __init__(self, Product, logic, childView=None, childLogic=None, buffer='',parentLogic=None):
        super(AtexView,self).__init__(Product, logic, 
                                      childView=childView, 
                                      childLogic=childLogic,
                                      buffer=buffer,
                                      parentLogic=parentLogic)


    def next(self,b):
        if self.logic.Q.effect[b]=='extra':
            self.logic.setUserRole(self.logic.Product.role, extraDuties=True)
            self.startYesNoQuestions(self.logic.QA)
        elif self.logic.Q.effect[b]=='False':
            self.logic.setState(False)
            self.finalize()
        else:
            if self.logic.Q.effect[b]=='True':
                self.logic.setState(True)
            self.logic.effects.append([self.logic.Q.effect[b]])
            if b == 'y':
                self.logic.Q = self.logic.Q.posChild
            elif b == 'n':
                self.logic.Q = self.logic.Q.negChild
            if self.logic.Q is None:
                self.finalize()
            else:
                self.updateView(self.logic.Q.text)



if __name__ == '__main__':


    directiveParser = directivePARSER()
    directiveParser.secondaries = ['<p class="ti-grseq-1".+>\d\.[^\d]']
    directiveParser.secondaryExtractor = '>((\d\.){1,1}|[A-Z]\.)'

    directiveParser.tertiaries = ['<p class="ti-grseq-1".+>(\d\.){2,2}[^\d].*<spa']
    directiveParser.tertiaryExtractor = '((\d\.){2,2})'

    directiveParser.quaternaries = ['<p class="ti-grseq-1".+>(\d\.){3,3}[^\d].*<spa']
    directiveParser.quaternaryExtractor = '((\d\.){3,3})'

    directiveParser.qStart = 4
    directiveParser.qEnd = 6

    text = directiveParser.getHtml(p='html_resources/directives/atex.html')
    atexArticle = directiveParser.parseArticles(text)
    atexAppendice = directiveParser.parseAppendices(text)

    ARTICLES = {'ATEX':atexArticle
               }
    APPENDICES = {'ATEX':atexAppendice
                 }


    dictParser = dictPARSER(APPENDICES,ARTICLES)



    jsonPath = 'json/__exampleMachine.json'

    jparser = jPARSER()
    machineData = jparser.parse(jsonPath)
    Product = Machine()

    configurator = Configurator(Product)
    configurator.configure(machineData)

    atex = ATEX(Product, dictParser)
    questions = Questions()

    app = QApplication(sys.argv)
    MG = AtexView(atex,questions)