class MissingPackageError(Exception):
    def __init__(self, pkg):
        d = {'PDF': 'PDF results processing'}
        m = ('Missing required package for {0}. To use this functionality, re-install ' +
             'hivemind-util using the command "pip install hivemind-util[{1}]".').format(d.get(pkg), pkg)
        self.message = m

    def __str__(self):
        return self.message
