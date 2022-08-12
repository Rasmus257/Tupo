class UnstableSyntaxError(SyntaxWarning):
    """
    Raised when a module differs from the original one in an unexpected way.

    """

    def __init__(self, e):
        self.exception = e

    def __str__(self):
        return 'Unstable Obfuscation! Please create an issue at https://github.com/Rdimo/Tupo/issues'


class InvalidOption(RuntimeError):
    """
    Raised when an invalid option has been set.

    """

    def __init__(self, e, opt):
        self.exception = e
        self.option = opt

    def __str__(self):
        return f'{self.exception}\n\nUnknown option: {self.option}'


class VersionError(RuntimeError):
    """
    Raised when a users python version is not compatible with Tupo.
    """

    def __init__(self, e):
        self.exception = e

    def __str__(self):
        return f'{self.exception}\n\nTupo requires Python 3.8+'
