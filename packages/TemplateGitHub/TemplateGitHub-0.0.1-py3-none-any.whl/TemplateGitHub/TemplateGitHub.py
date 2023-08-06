from .Utils import Multiply

class TemplateGitHub(object):
    legs = 4
    def __init__(self,x):
        self.x = x
        print('Built template class')
        pass

    def Bark(self):
        print('guaff')
        pass

    def MultiplyBy(self,multiplier):
        print(Multiply(self.x,multiplier))
        pass

    def Ask(self,s):
        if 'truffle' in s:
            print('Borja is the correct answer')
        else:
            print('Sanaa decides')
        pass
    

