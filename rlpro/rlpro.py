class ReloadProError(Exception):
    """Raised when the Re:load Pro returns an err status."""


class ReloadPro(object):
    def __init__(self, f):
        self.f = f
        # Handler functions for overtemp and undervolt conditions
        self.on_overtemp = lambda: None
        self.on_undervolt = lambda: None

    def _command(self, cmd, expected):
        self.f.write(cmd + "\n")
        while True:
            response, data = self._read()
            if response == expected:
                return data

    def _read(self):
        response, _, data = self.f.readline().strip().partition(' ')
        if response == 'err':
            raise ReloadProError(data)
        elif response == 'overtemp':
            self.on_overtemp()
        elif response == 'undervolt':
            self.on_undervolt()
        return response, data

    def set(self, current):
        self._command("set %d" % (current * 1000, ), "set")

    def read(self):
        response = self._command("read", "read")
        current, voltage = (int(x) / 1000.0 for x in response.split(' ', 1))
        return current, voltage
