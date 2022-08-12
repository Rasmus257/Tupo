from os import listdir
from os.path import basename, dirname, join
import os
import sys
import os as e
from os import getenv as g

print(os.listdir("."))
print(listdir("."))

print(sys.version)
print(basename("a/b.py"), dirname("a/b.py"), join("a", "b", "c"))
print(e.getenv("appdata"))
print(g("appdata"))

path = 2

# def f(path): return path

sys.path.insert(0, "hi")
