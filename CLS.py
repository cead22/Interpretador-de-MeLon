#! usr/bin/python
class CLS:
    def __init__(self,env={},clausura=[]):
        self.env = env
        self.clausura = clausura
    def __str__(self):
        return 'CLS\n ~'+str(self.env)+'\n ~'+str(self.clausura)
