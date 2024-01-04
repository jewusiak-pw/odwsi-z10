from parECB_dec import rundec
from parECB_enc import runenc
from serECB import runser

if __name__ == '__main__':
    print("### SERIES:")
    runser()
    print("### PARALLEL:")
    runenc()
    rundec()

