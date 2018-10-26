# Godot Python Test

Godot Python Test Projects  
Tested on Mac 10.14

## Dependencies

- Godot 3.0.6
- GodotPyton 0.11.3

## Build Environments

### Installing Godot

In Mac
```
brew cask install godot
```

In Windows

```
scoop bucket add extras
scoop install godot
```

### Installing Godot Python

1. Import Project
2. Search Python in AssetLib
3. Install PythonScript for your environment
4. Reboot Editor

### Fix Python Dependencies(mac only)

```
brew install gnu-sed
```

Chmod 755
```
cd pythonscript/osx-64-cpython/
chmod 755 ./bin/*
chmod 755 ./lib/libpython3.6m.dylib
```

Change Python shebang
```
cd pythonscript/osx-64-cpython/
find ./bin/ -type f -not -name 'python3' -not -name 'python3.6' -not -name 'python3.6m' | xargs gsed -i '1c #!./bin/python3.6'
```

Add LC_RPATH and fix LC_LOAD_DYLIB for python
```
cd pythonscript/osx-64-cpython/

install_name_tool -add_rpath @loader_path/../lib/ ./bin/python3
install_name_tool -add_rpath @loader_path/../lib/ ./bin/python3.6
install_name_tool -add_rpath @loader_path/../lib/ ./bin/python3.6m

otool -L ./bin/python3 | grep -e libpython3.6m | cut -d ' ' -f 1 | xargs -I{} sh -c 'install_name_tool -change {} @rpath/libpython3.6m.dylib ./bin/python3'
otool -L ./bin/python3.6 | grep -e libpython3.6m | cut -d ' ' -f 1 | xargs -I{} sh -c 'install_name_tool -change {} @rpath/libpython3.6m.dylib ./bin/python3.6'
otool -L ./bin/python3.6m | grep -e libpython3.6m | cut -d ' ' -f 1 | xargs -I{} sh -c 'install_name_tool -change {} @rpath/libpython3.6m.dylib ./bin/python3.6m'

install_name_tool -id @rpath/libpython3.6m.dylib ./lib/libpython3.6m.dylib
install_name_tool -add_rpath @loader_path/ ./lib/libpython3.6m.dylib
```

Now you can use pip!

Add LC_RPATH and fix LC_LOAD_DYLIB for libpythonscript
```
cd pythonscript/osx-64-cpython/

install_name_tool -id @rpath/libpythonscript.dylib ./libpythonscript.dylib

install_name_tool -add_rpath @loader_path/ ./libpythonscript.dylib

otool -L ./libpythonscript.dylib | grep -e libpython3.6m | cut -d ' ' -f 1 | xargs -I{} sh -c 'install_name_tool -change {} @rpath/libpython3.6m.dylib ./libpythonscript.dylib'
```

## Using pip

### Easy Access
```
cd pythonscript/osx-64-cpython/
./bin/pip3 --version
```

### freeze and install
```
cd pythonscript/osx-64-cpython/
./bin/pip3 freeze > ../../../requirements.txt
./bin/pip3 install -r ../../../requirements.txt
```

## Known Issues

- Plugin load problem on Mac after packaging (TODO: Need to fix Godot or Godot Python)
- Python directory problem on Mac after packaging (TODO: Need to fix Godot or Godot Python)
