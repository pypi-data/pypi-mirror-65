class SM:
    def __init__(self, fi, fn):
        N = set()
        self.V = set()
        self.E = set()

        try:
            sns = fi()
            for v in sns:
                N.add(v)

            while True:
                sn = N.pop()
                sns = fn(sn)

                self.V.add(sn)
                for v in sns:
                    self.E.add((sn, v))
                    if v in self.V:
                        continue
                    N.add(v)
        except KeyError:
            return
