#
# True = On
# False = Off
#
# Leave non-bool options blank if you don't want to use them.
# Only applies to:
#     - Version
#     - Description
#     - Copyright

conf = {
    "CompressOnly": False,  # Disable all options below except for `Executable` | mostly just for people who want to use PyHide to compress and minimize their executable
    "Obfuscation": {
        # Enable/Disable Obfuscation
        "Enabled": True,
        # Encrypts the bytecode with secret key record in a .pyd so the key would be hidden in binary | recommended to keep this on since it drastically improves security
        "EncryptBytecode": False,
        # Uses strings hexcode representation | Example: "Hello World" -> "0x48656c6c6f20576f726c64"
        "HexStrings": False,
        # Rename variables, functions, classes, etc. | Example: "variable = "hello"" -> "곦𞤸𞹢ࢭ𰓆ﲳᩆ𣪅ﶄࢡ𧲆ﰈ𪟍ﳊ = "hello""
        "RenameTypes": False,
        # Replaces datatypes with more complex ones | Example: "True" -> "(()==())"
        "ReplaceTypes": False,
        # Transforms code into python byte code | Example: "print('Hello World')" -> "\x17\x17\x00Z\ne\nd\x18\x17\x00Z\x0be\x0bd\x19\x17\x00Z\x0ce\"
        "Marshal": False,
        # Abstract Syntax Tree transformation | Example "print('Hello World')" -> "__=lambda _:type(*_);_0_=str;_0=lambda _0:_0.__code__.co_argcount;_=None;___=__([_0_()((2**2+(1**2+2))*((1**2+2)**2+2**2))"
        "ASTObfuscation": True,
        # layer adding, will use a random layer method which all are unique making it harder to reverse | Default: False
        "LayerObfuscation": False,
        # amount of layers to add to the obfuscation, more layers = slower runtime but harder to deobfuscation | Default: 1
        "LayersAmount": 1,
    },
    "Minifier": {
        # Enable/Disable Minifier
        "Enabled": True,
        # Remove Comments, docstrings, shebangs, etc... | Default: True
        "RemoveComments": True,
        # Transforms large integers to a power of 2 or 10. | Example: 10000000000 -> 10**10 | Default: True
        "IntegerToPower": True,
        # Transform a function to a lambda assigned to a variable with the same name reducing it with a few characters | Default: False
        # This options is UNSAFE. Lambda is NOT a function object, (e.g it doesn't have __name__ attribute, annotations, decorators etc..)
        "FunctionToLambda": True,
    },
    "DeadCode": {
        # Enable/Disable Dead Code | Default: False
        "Enabled": False,
        # Minimum amount of dead code | Default: 1
        "MinAmount": 1,
        # Maximum amount of dead code | Default: 50
        "MaxAmount": 50,
    },
    "Protectors": {
        "Enabled": False,  # Enable/Disable Protectors
        "AntiDecompile": True,  # Makes it much harder to disassemble the exe and get the obfuscated code | Default: True
        "AntiDebug": False,  # Adds a anti-vm and anti-debugger to the original source | Default: True
    },
    "Executable": {
        "Enabled": True,  # Enable/Disable if a executable is generated | Default: True
        "PyinstallerOptions": [  # Pyinstaller Options, read more on https://pyinstaller.org/ | Default: ["--onefile", "--noconsole", "--clean", "--key" "%KEY%"] (recommend keeping these options)
            "--onefile",
            "--noconsole",
            "--clean",
            "--key",
            # Generate random key. For custom key, replace %KEY% with your key, this will encrypt the bytecode with AES, not hard to decrypt tho | Default: "%KEY%"
            "%KEY%"
        ],
        "SignExecutable": False,  # Signs the executable with a certificate | Default: False
        "RequestElevation": False,  # request elevation upon execution (Windows Only) | Default: False
        "Path": "./",  # path output where the executable will be saved | Example: "./output" | Default: "./"
        "Version": "1.0.0",  # version of the executable | Example: "69.420.0" | Default: "1.0.0"
        "Description": "file obfuscated with PyHide",  # description of the executable | Example: "LOL!" | Default: "file obfuscated with PyHide"
        "Copyright": "PyHide",  # copyright of the executable | Example: "https://microsoft.com" | Default: "PyHide"
    }
}
