# CPP-Compiler2.0
compiler made in python that uses g++ to compile your projects

If you modify a header file, The cpp files that includes it will be recompiled, but this only applies for files that are in the same project direcotry. If you have multiple project directory they will be compiled separatly.

You first need to make a folder and inside that folder you can create your projects. It basically has the same structure as visual studio community. 
Folder->project->code
      ->project2->code

Create new project
``` python
python Compiler.py create_projectname
```

You Can Create multiple projects if you want

Use this to compile. You have to call in side the folder that contains the projects.
```python 
python Compiler.py
```

Or This to Compile Specific Projects
```python
python Compiler.py compile_projectname
```


Use this to recompile the whole project completely
```python
python Compiler.py recompileall
```

Or this to recompile specifi project
```python 
python Compiler.py recompile_projectname
```


# Important
In each project created there is a build.txt file
In there you can specify some additional paramterers such as includes, libs and dependencies. You can also change the app type(exe or dll). You can Choose between Debug or release and add preprocessors.
If you are using the executable instead of the python file, call with just Compiler parameters.

if you have multiple arguments to pass in includes, libs, dependencies or preprocessors, Add a ; before each argument. BEFORE and NOT AFTER

Exemple: (libs :;src/folder/dsd;src2/folder/asa)



