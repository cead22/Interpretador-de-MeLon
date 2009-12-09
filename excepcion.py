import sys
class ParametrosError(Exception):
    def __init__(self,messg):
        self.messg = messg

