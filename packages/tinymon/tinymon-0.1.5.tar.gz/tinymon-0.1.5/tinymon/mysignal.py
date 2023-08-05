import signal

class MySignal():
    handler = {}
    def __init__(self):
        self.register_all_signal()

    def register_handler(self, signum, func):
        self.handler[signum] = func

    def sighandler(self, signum, frame):
        try :
            sig = signal.Signals(signum)
            self.handler[signum]()
        except KeyError:
            print(f"unregistered signal {sig.name} {signum} {frame}")
        else:
            raise Exception(f"Signal.{sig.name}")
            
    def register_all_signal(self):
        for x in dir(signal):
            if not x.startswith("SIG"):
                continue
            try:
                signum = getattr(signal, x)
                signal.signal(signum, self.sighandler)
            except:
                print('Skipping the signal : %s' % x)
                continue
    

if __name__ == '__main__':

    sig = MySignal()
    f = lambda : print('sig test')
    sig.register_handler(signal.SIGINT, f)

    while True:
        pass