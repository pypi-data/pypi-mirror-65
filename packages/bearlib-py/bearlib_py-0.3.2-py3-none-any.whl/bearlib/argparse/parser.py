from sys import argv


class Parser(object):
    def __init__(self, args, format="{}=", reqargs=None):
        self.args = args
        self.format = format
        self.seperator = format.split("}")[1]
        self.reqargs = reqargs

    def set_format(self, format):
        if not any(x in format for x in ["{", "}"]):
            raise ValueError("Format should contain format brackets!")
        self.format = format
        self.seperator = format.split("}")[1]

    def set_args(self, args):
        if type(args) == list:
            self.args = args
        elif args is not None:
            self.args = [args]

    def set_reqargs(self, reqargs):
        if type(reqargs) == list:
            self.reqargs = reqargs
        elif reqargs is not None:
            self.reqargs = [reqargs]

    def get_args(self):
        if not self.argdict:
            all_args = self.args
            if self.reqargs:
                all_args += self.reqargs
            argdict = {}
            for arg in argv:
                for key in all_args:
                    if self.format.format(key) in arg:
                        argdict[key] = self.seperator.join(
                            arg.split(self.seperator)[1:]
                        )
            self.argdict = argdict
            missing = []
            for arg in self.reqargs:
                if arg not in self.argdict or self.argdict[arg] is None:
                    missing.append(arg)
            if len(missing) > 0:
                raise ValueError(
                    f"Missing required arguments: {', '.join(missing)}"
                )
        return self.argdict
