import builtins
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

inbuilts = dir(builtins) + ['__builtins__', '__file__', '__cwd__']
inbuilt_types = [
    abs, aiter, all, anext, any, ascii, bin, bool, breakpoint, bytearray, bytes, callable, chr,
    classmethod, compile, complex, copyright, credits, delattr, dict, dir, divmod, enumerate, eval,
    exec, exit, filter, float, format, frozenset, getattr, globals, hasattr, hash, help, hex, id, input,
    int, isinstance, issubclass, iter, len, license, list, locals, map, max, memoryview, min, next, object,
    oct, open, ord, pow, print, property, quit, range, repr, reversed, round, set, setattr, slice, sorted,
    staticmethod, str, sum, super, tuple, type, vars, zip, Ellipsis, None, True, False,

    ArithmeticError, AssertionError, AttributeError, BaseException, BlockingIOError, BrokenPipeError,
    BufferError, BytesWarning, ChildProcessError, ConnectionAbortedError, ConnectionError, ConnectionRefusedError,
    ConnectionResetError, DeprecationWarning, EOFError, EncodingWarning, EnvironmentError, Exception, FileExistsError,
    FileNotFoundError, FloatingPointError, FutureWarning, GeneratorExit, Warning, WindowsError, ZeroDivisionError,
    IOError, ImportError, ImportWarning, IndentationError, IndexError, InterruptedError, IsADirectoryError,
    KeyError, KeyboardInterrupt, LookupError, MemoryError, ModuleNotFoundError, NameError, NotADirectoryError,
    NotImplemented, NotImplementedError, OSError, OverflowError, PendingDeprecationWarning, PermissionError, ProcessLookupError,
    RecursionError, ReferenceError, ResourceWarning, RuntimeError, RuntimeWarning, StopAsyncIteration, StopIteration,
    SyntaxError, SyntaxWarning, SystemError, SystemExit, TabError, TimeoutError, TypeError, UnboundLocalError,
    UnicodeDecodeError, UnicodeEncodeError, UnicodeError, UnicodeTranslateError, UnicodeWarning, UserWarning, ValueError,

    __build_class__, __import__, __loader__, __name__, __package__, __spec__, __builtins__, __file__,
]

# Attribute/method names that belong to built-in types (list.append, dict.keys,
# str methods, dunders, ...). The obfuscator must NOT rename these — it can't
# rename their definition to match, so renaming would break the call.
builtin_members = set()
for _t in (object, list, dict, set, frozenset, tuple, str, bytes, bytearray,
           int, float, complex, bool, type, range, enumerate, zip, map, filter):
    builtin_members.update(dir(_t))

########################################################################################################################
allowed_shuffle_types = ['normal', 'nonlatin', 'mini']

antivm_code = """import os
import socket
import getpass
import platform
import threading
import subprocess
import psutil
class AntiDebug:
    inVM = False
    def __init__(self):
        self.processes = list()
        self.blackListedUsers = ["WDAGUtilityAccount", "Abby", "Peter Wilson", "hmarc", "patex", "JOHN-PC", "RDhJ0CNFevzX", "kEecfMwgj", "Frank",
            "8Nl0ColNQ5bq","Lisa", "John", "george", "PxmdUOpVyx", "8VizSM", "w0fjuOVmCcP5A", "lmVwjj9b", "PqONjHVwexsS", "3u2v9m8", "Julia", "HEUeRzl"]
        self.blackListedPCNames = [
            "BEE7370C-8C0C-4", "DESKTOP-NAKFFMT", "WIN-5E07COS9ALR", "B30F0242-1C6A-4", "DESKTOP-VRSQLAG", "Q9IATRKPRH", "XC64ZB", "DESKTOP-D019GDM", "DESKTOP-WI8CLET", "SERVER1",
            "LISA-PC", "JOHN-PC", "DESKTOP-B0T93D6", "DESKTOP-1PYKP29", "DESKTOP-1Y2433R", "WILEYPC", "WORK", "6C4E733F-C2D9-4", "RALPHS-PC", "DESKTOP-WG3MYJS", "DESKTOP-7XC6GEZ",
            "DESKTOP-5OV9S0O", "QarZhrdBpj", "ORELEEPC", "ARCHIBALDPC", "JULIA-PC", "d1bnJkfVlH"]
        self.blackListedHWIDS = ["7AB5C494-39F5-4941-9163-47F54D6D5016", "032E02B4-0499-05C3-0806-3C0700080009", "03DE0294-0480-05DE-1A06-350700080009",
                                 "11111111-2222-3333-4444-555555555555", "6F3CA5EC-BEC9-4A4D-8274-11168F640058", "ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548",
                                 "4C4C4544-0050-3710-8058-CAC04F59344A", "00000000-0000-0000-0000-AC1F6BD04972", "79AF5279-16CF-4094-9758-F88A616D81B4",
                                 "5BD24D56-789F-8468-7CDC-CAA7222CC121", "49434D53-0200-9065-2500-65902500E439", "49434D53-0200-9036-2500-36902500F022",
                                 "777D84B3-88D1-451C-93E4-D235177420A7", "49434D53-0200-9036-2500-369025000C65", "B1112042-52E8-E25B-3655-6A4F54155DBF",
                                 "00000000-0000-0000-0000-AC1F6BD048FE", "EB16924B-FB6D-4FA1-8666-17B91F62FB37", "A15A930C-8251-9645-AF63-E45AD728C20C",
                                 "67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3", "C7D23342-A5D4-68A1-59AC-CF40F735B363", "63203342-0EB0-AA1A-4DF5-3FB37DBB0670",
                                 "44B94D56-65AB-DC02-86A0-98143A7423BF", "6608003F-ECE4-494E-B07E-1C4615D1D93C", "D9142042-8F51-5EFF-D5F8-EE9AE3D1602A",
                                 "49434D53-0200-9036-2500-369025003AF0", "8B4E8278-525C-7343-B825-280AEBCD3BCB", "4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27"]
        self.system = platform.system()
        for func in [self.listCheck, self.specsCheck, self.vmCheck]:
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
    def run_cmd(self, cmd):
        try:
            kwargs = {"stderr": subprocess.DEVNULL}
            if self.system == "Windows":
                kwargs["creationflags"] = 0x08000000
            return subprocess.check_output(cmd, **kwargs).decode(errors="ignore")
        except Exception:
            return ""
    def get_hwid(self):
        if self.system == "Windows":
            out = self.run_cmd("wmic csproduct get uuid")
            lines = [line.strip() for line in out.splitlines() if line.strip()]
            return lines[1] if len(lines) > 1 else ""
        if self.system == "Linux":
            for path in ("/sys/class/dmi/id/product_uuid", "/etc/machine-id", "/var/lib/dbus/machine-id"):
                try:
                    with open(path) as handle:
                        value = handle.read().strip()
                    if value:
                        return value
                except OSError:
                    continue
            return ""
        if self.system == "Darwin":
            out = self.run_cmd(["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"])
            for line in out.splitlines():
                if "IOPlatformUUID" in line:
                    return line.split("=")[-1].strip().strip('"')
        return ""
    def listCheck(self):
        try:
            if getpass.getuser() in self.blackListedUsers:
                self.programExit()
        except Exception:
            pass
        if socket.gethostname() in self.blackListedPCNames:
            self.programExit()
        if os.getenv("COMPUTERNAME") in self.blackListedPCNames:
            self.programExit()
        if self.get_hwid().upper() in self.blackListedHWIDS:
            self.programExit()
    def specsCheck(self):
        try:
            if (os.cpu_count() or 2) <= 1:
                self.programExit()
        except Exception:
            pass
        try:
            if psutil.virtual_memory().total / 1024 ** 3 <= 2:
                self.programExit()
        except Exception:
            pass
        try:
            if psutil.disk_usage(os.getcwd()).total / 1024 ** 3 <= 50:
                self.programExit()
        except Exception:
            pass
    def vmCheck(self):
        vendors = ("vmware", "virtualbox", "vbox", "qemu", "kvm", "xen", "hyper-v", "hyperv", "parallels", "bochs", "sandbox")
        blob = ""
        if self.system == "Windows":
            blob = self.run_cmd("wmic computersystem get manufacturer,model") + self.run_cmd("wmic bios get serialnumber,version")
        elif self.system == "Linux":
            for path in ("/sys/class/dmi/id/product_name", "/sys/class/dmi/id/sys_vendor", "/sys/class/dmi/id/board_vendor", "/sys/class/dmi/id/bios_vendor"):
                try:
                    with open(path) as handle:
                        blob += " " + handle.read()
                except OSError:
                    continue
            try:
                with open("/proc/cpuinfo") as handle:
                    if "hypervisor" in handle.read().lower():
                        self.programExit()
            except OSError:
                pass
        elif self.system == "Darwin":
            blob = self.run_cmd(["system_profiler", "SPHardwareDataType"]) + self.run_cmd(["ioreg", "-l"])
        blob = blob.lower()
        for vendor in vendors:
            if vendor in blob:
                self.programExit()
if AntiDebug().inVM:
    os._exit(0)
"""
