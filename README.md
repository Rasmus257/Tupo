# Tupo — The ultimate Python obfuscator

Tupo turns a `.py` file into functionally-equivalent but hard-to-read Python,
and can optionally package the result into a standalone executable.

## Features

Every transform is toggleable in [`config.py`](config.py):

- **Identifier renaming** — variables, functions and classes renamed with
  non-Latin / minimal unicode names.
- **Constant shuffling** — strings and ints are hex-encoded and pulled from a
  shuffled list at the top of the file.
- **Type replacement** — e.g. `True` → `(()==())`, `None` → `exec(str())`.
- **AST obfuscation** — the source is rewritten and wrapped in a
  zlib/lzma-compressed `exec`.
- **Dead-code injection** — random junk declarations.
- **Minification** — remove `pass`, combine imports, strip literal statements,
  drop the `object` base, etc. (via [python-minifier](https://pypi.org/project/python-minifier/)).
- **Marshal packing** — compile to a marshalled code object.
- **Anti-VM / anti-debug protector** — optional, prepends cross-platform
  (Windows / Linux / macOS) sandbox-detection code to the output.

## Requirements

- **Python 3.9+**
- Runs on **Windows, Linux and macOS**. (The optional executable build targets
  the OS you run it on.)

## Install

```sh
git clone https://github.com/Rasmus257/Tupo.git
cd Tupo
pip install -r requirements.txt
```

## Usage

```sh
python main.py path/to/your_script.py
```

The obfuscated file is written to `test-obf/<name>.py`. Run with no argument to
obfuscate the bundled `test/test_general.py` sample. Enable/disable transforms
and set options in [`config.py`](config.py).

## Building an executable (optional)

The executable build step (PyInstaller + UPX) is included but **not actively
tested**. To use it:

1. Download **UPX** from <https://upx.github.io/> and put the binary in
   `src/tools/` (it is intentionally not committed to the repo).
2. Uncomment `Tupo().main()` in [`main.py`](main.py).
3. It shells out to `pipenv`; a `Pipfile` is included for that path.

## Optional dependency

Enabling the **AntiDebug** protector injects code that uses
[`psutil`](https://pypi.org/project/psutil/) to check machine specs. Install it
in whatever environment runs the obfuscated program:

```sh
pip install psutil
```

## Known limitations

- Enabling **AST obfuscation together with every other transform** on a complex
  file can nest expressions deeper than CPython's compiler allows
  (`RecursionError ... during compilation`). Use AST obfuscation with fewer
  companion transforms, or on smaller files. Every individual transform and the
  default configuration work fine.
- A few optional minifier passes (e.g. `CombineImports`) are skipped silently
  when `python_minifier`'s internal requirements aren't met — they simply don't
  apply rather than breaking the output.
- The executable build path is unverified.

## Disclaimer

Tupo is provided for educational purposes and for legitimately protecting your
own source code. Do not use it to conceal malware or for any unlawful purpose.

## License

[PolyForm Noncommercial License 1.0.0](LICENSE) — free to use, modify and share
for **non-commercial** purposes. Commercial use, including selling, is not
permitted.
