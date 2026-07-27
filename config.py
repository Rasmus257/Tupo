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
    "CompressOnly": False,  # Disable all options below except for `Executable` and `Minifier` | mostly just for people who want to use PyHide to compress and minimize their executable
    "Tupo": {
        "ProgressBar": True,  # Enable progress bar | Default: True
    },
    "Obfuscation": {
        # Enable/Disable Obfuscation
        "Enabled": True,
        # Encrypts the bytecode with secret key record in a .pyd so the key would be hidden in binary | recommended to keep this on since it drastically improves security
        "EncryptBytecode": True,
        # Obfuscates strings, integers, etc. Also puts all constants in a shuffled list located at the top | Example: "Hello World" -> "48656c6c6f20576f726c64"
        "ConstantShuffler": True,
        # Replaces datatypes with more complex ones | Example: "True" -> "(()==())"
        "ReplaceTypes": True,
        # Rename variables, functions, classes, etc. | Example: "variable = "hello"" -> "곦𞤸𞹢ࢭ𰓆ﲳᩆ𣪅ﶄࢡ𧲆ﰈ𪟍ﳊ = "hello""
        "RenameIdentifiers": True,
        # The type of shuffling it will use for the option above
        # Supported types: 'normal', 'nonlatin', 'mini' | Default: 'nonlatin'
        "RenameIdentifiersType": "mini",
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
        # Removes unused code such as variables, functions, classes, etc. | Example: "variable = "hello"" -> "" | Default: True
        "RemoveUnused": True,
        # Removes pass statements | Example: "pass" -> "" | Default: True
        "RemovePass": True,
        # Removes literal statements | Example: "ye = True; if ye is True: ..." -> "if True is True: ..." | Default: True
        "RemoveLiteralStatements": False,
        # Combines adjacent import statements | Example: "import a;import b" -> "import a,b" | Default: True
        "CombineImports": False,
        # Removes object as a base class | Example: "class A(object):pass" -> "class A:pass" | Default: True
        "RemoveObjectBase": False,
        # Converts posargs to keyword args | Example: "def f(a,b):pass" -> "def f(a,b=None):pass" | Default: True
        "ConvertPosargsToArgs": False,
    },
    "DeadCode": {
        # Enable/Disable Dead Code injection | Default: False
        "Enabled": True,
        # adds random useless code | Default: False
        "AddRandomCode": False,
        # Minimum amount of dead code | Default: 1
        "MinAmount": 1,
        # Maximum amount of dead code | Default: 50
        "MaxAmount": 50,

        # Note: The min and max amount represents the number of lines
    },
    "Protectors": {
        "Enabled": False,  # Enable/Disable Protectors
        # Makes it much harder to disassemble the exe and get the obfuscated code | Default: True
        "AntiDecompile": True,
        # Adds a anti-vm and anti-debugger to the original source | Default: True
        "AntiDebug": False,
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
        # request elevation upon execution (Windows Only) | Default: False
        "RequestElevation": False,
        "Path": "./",  # path output where the executable will be saved | Example: "./output" | Default: "./"
        "Version": "1.0.0",  # version of the executable | Example: "69.420.0" | Default: "1.0.0"
        # description of the executable | Example: "LOL!" | Default: "file obfuscated with Tupo"
        "Description": "file obfuscated with Tupo",
        # copyright of the executable | Example: "https://website.com" | Default: "Tupo"
        "Copyright": "Tupo",
    }
}
