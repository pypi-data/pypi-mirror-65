import logging


class SM:
    def __init__(self, fi, fn, logger=None):

        self.logger = logging.getLogger(name=logger)

        self.V = set()
        self.E = set()
        N = set()

        try:
            self.logger.info('[SM] [INIT] [START]')

            sns = fi()
            for v in sns:
                N.add(v)

            self.logger.info('[SM] [INIT] [DONE]')
            self.log()
            self.logger.info('[SM] [LOOP] [START]')

            while True:
                sn = N.pop()
                sns = fn(sn)

                self.V.add(sn)
                for v in sns:
                    self.E.add((sn, v))
                    if v in self.V:
                        continue
                    N.add(v)

                self.log(sn=sn, sns=sns)
        except KeyError:
            self.logger.info('[SM] [LOOP] [DONE]')
            return

    def result(self):
        return self.V, self.E

    @classmethod
    def log(self, sn=None, sns=None):
        pass
