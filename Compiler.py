import os
import sys
import shutil
import time

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


compiler = "g++"

def removeDir(path):
    try:
        shutil.rmtree(path)
    except:
        Log(FAIL, f"[INFO] Cannot delete {path} directory")

def copyDir(folderName):
    name = folderName.split("/")[-1]
    if CheckIfPathExist(f"bin\\build\\{name}"):
        removeDir(f"bin\\build\\{name}")
    shutil.copytree(f"{folderName}", f"bin\\build\\{name}")

def copyToDir(folderName):
    folderName = folderName.replace("/", "\\")
    files = os.listdir(folderName)
    for file in files:
        shutil.copy(f"{folderName}\\{file}", f"bin\\build\\{file}")


try:
    argument = sys.argv[1]
except IndexError:
    argument = ""

def VerifyPath(path):
    if CheckIfPathExist(path):
        removeDir(path)

def Log(level, message):
    print(f"{level} {message} {ENDC}")

def CreateDir(name):
    VerifyPath(name)
    os.system(f'cmd /c "mkdir {name}"')
def CreateFile(name):
    os.system(f'cmd /c "type nul > {name}"')
def CheckIfPathExist(path):
    return os.path.exists(path)

def VerifyBinFolder(DirPath):
    if CheckIfPathExist("bin") == False:
        os.system('cmd /c"mkdir bin"')
    if CheckIfPathExist("bin\\build") == False:
        os.system('cmd /c"mkdir bin\\build"')
    if CheckIfPathExist("bin\\obj") == False:
        os.system('cmd /c"mkdir bin\\obj"')
    if CheckIfPathExist(f"bin\\obj\\{DirPath}") == False:
        os.system(f'cmd /c"mkdir bin\\obj\\{DirPath}"')
    if CheckIfPathExist(f"bin\\obj\\{DirPath}\\BuildData.txt") == False:
        CreateFile(f"bin\\obj\\{DirPath}\\BuildData.txt")
        CreateBuildDataTemplate(f"bin\\obj\\{DirPath}\\BuildData.txt")

def CreateBuildDataTemplate(file):
    f = open(f"{file}", "w")
    f.write("__________OBJ BUILD FILES INFORMATION_______\n\n\n")

def CreateBuildTemplate(file, app_name):
    # Create Template for the build File
    f = open(f"{file}", "w")
    f.write("______________BUILD INFORMATION___________\n\n\n")
    f.write(f"App name                     :{app_name}\n")
    f.write("Extension Type               :exe\n")
    f.write("Ressource Folder             :\n")
    f.write("Necessary Files              :\n")
    f.write("Additionnal Includes Dir     :\n")
    f.write("Additionnal Lib Dir          :\n")
    f.write("Additionnal dependencies     :\n")
    f.write("Preprocessors                :\n")
    f.write("Build Type                   :Debug \n")
    f.write("Cpp version                  :20\n")

def InterpretBuildFile(path):
    f = open(path, "r")
    data = []
    for line in f:
        if ":" in line:
            line = line.split(":")[1]
            line = line.split("\n")[0]
            data.append(line)

    return data

def FindCppFiles(DirPath):
    cpp_files = []
    for root, dirs, files in os.walk(DirPath):
        for file in files:
            if ".cpp" in file:
                path = os.path.join(root, file)
                cpp_files.append([file, path])
    return cpp_files
def FindHFiles(DirPath):
    h_files = []
    for root, dirs, files in os.walk(DirPath):
        for file in files:
            if ".h" in file or ".hpp" in file:
                path = os.path.join(root, file)
                h_files.append([file, path])
    return h_files

def spaces_calculator(file_name_length, needed_length):
    spaces = ""
    requires_spaces = needed_length - file_name_length
    i = 0
    while i < requires_spaces:
        spaces += " "
        i += 1

    return spaces

def run_app():
    exe_file = ""
    for file in os.listdir("bin\\build"):
        if ".exe" in file:
            exe_file = file
            break

    if exe_file != "":
        os.system(f'cmd /c"cd bin\\build && start {exe_file}"')
    else:
        Log(WARNING, "No exe file found in bin/build")

def GetLastBuildTime(DirPath):
    f = open(f"bin\\obj\\{DirPath}\\BuildData.txt", "r")
    objects = []
    cpp_objects = []
    h_objects = []
    for line in f:
        if "->" in line:
            if ".cpp" in line.split("->")[0]:
                newObj = []
                newObj.append(line.split("->")[0])
                newObj.append(time.strptime(line.split("->")[1].replace("\n", ""), '%Y-%m-%d %H:%M:%S'))
                cpp_objects.append(newObj)
            elif ".h" in line.split("->")[0] or ".hpp" in line.split("->")[0]:
                newObj = []
                newObj.append(line.split("->")[0])
                newObj.append(time.strptime(line.split("->")[1].replace("\n", ""), '%Y-%m-%d %H:%M:%S'))
                h_objects.append(newObj)
    objects.append(cpp_objects)
    objects.append(h_objects)
    return objects

def checkIfShouldReBuild(file, times, h_files):
    lastModTime = os.path.getmtime(file[1])
    modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastModTime))
    found_File = False
    for cpp_time in times[0]:
        if cpp_time[0] == file[0]:
            found_File = True
            buildTime = time.strftime('%Y-%m-%d %H:%M:%S', cpp_time[1])
            if modificationTime > buildTime:
                return True
        
    if found_File == False:
        return True

    f = open(file[1], "r")
    includes = []
    for line in f:
        if "#include" in line and '"' in line:
            includes.append(line.split('"')[1])

    for include in includes:
        for h in h_files:
            if h[0] == include:
                lastModTime = os.path.getmtime(h[1])
                modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastModTime))

        for h_time in times[1]:
            if h_time[0] == include:
                buildTime = time.strftime('%Y-%m-%d %H:%M:%S', h_time[1])
                if modificationTime > buildTime:
                    return True
                else:
                    return False
    
def UpdateObjBuildFileData(new_data, path):
    f = open(path, "w")

    f.write("__________OBJ BUILD FILES INFORMATION_______\n\n\n")
    for new in new_data:
        f.write(f"{new[0]}->{new[1]}\n")


def build(DirPath):
    data = InterpretBuildFile(f"{DirPath}\\build.txt")
    cpp_files = FindCppFiles(DirPath)
    h_files = FindHFiles(DirPath)

    app_name        =     data[0]
    app_type        =     data[1]
    ressource_dir   =     data[2].split(";")[1:]
    nece_files      =     data[3].split(";")[1:]
    includes        =     data[4].replace(";", " -I")
    libs            =     data[5].replace(";", " -L")
    dependencies    =     data[6].replace(";", " -l")
    preprocessors   =     data[7].replace(";", " -D")
    build_type      =     data[8]
    cpp_version     =     data[9]

    Log(OKBLUE, f"[INFO] Compiling {DirPath} directory in {build_type} mode")
    Log(OKGREEN, "")


    build_parameter = ""
    if build_type == "Debug":
        build_parameter = ""
    elif build_type == "Release":
        build_parameter = "-03"

    VerifyBinFolder(DirPath)

    # compile cpp files
    files_count = len(cpp_files)
    curr_file = 1
    succeeded = False
    files_New_Build_time = []
    compiled = 0
    for cpp_file in cpp_files:
        objects_time = GetLastBuildTime(DirPath)
        spaces = spaces_calculator(len(cpp_file[0]), 25)
        if checkIfShouldReBuild(cpp_file, objects_time, h_files):
            Log(HEADER, f"[COMPILER] Compiling {cpp_file[0]}...{spaces}{curr_file}/{files_count}")
            result = os.system(f'cmd /c"{compiler} {build_parameter} -g --std=c++{cpp_version} {preprocessors} {includes} -c {cpp_file[1]} -o bin\\obj\\{DirPath}\\{cpp_file[0]}.o"')
            if result == 1:
                succeeded = False
                Log(FAIL, f"[COMPILER] Failed to compile {cpp_file[0]}")
                break
            else:
                succeeded = True
            curr_file += 1
            files_New_Build_time.append([cpp_file[0], time.strftime('%Y-%m-%d %H:%M:%S')])
            compiled += 1
        else:
            name = cpp_file[0] + "(SKIP)"
            Log(HEADER, f"[COMPILER] Compiling {name}...{spaces}{curr_file}/{files_count}")
            curr_file += 1
            files_New_Build_time.append([cpp_file[0], time.strftime('%Y-%m-%d %H:%M:%S')])
            succeeded = True
    for h_file in h_files:
        files_New_Build_time.append([h_file[0], time.strftime('%Y-%m-%d %H:%M:%S')])
    UpdateObjBuildFileData(files_New_Build_time, f"bin\\obj\\{DirPath}\\BuildData.txt")


    # link
    if succeeded:
        result = 0
        if compiled > 0:
            Log(WARNING, f"[LINKER] Linking ...")
            if app_type == "exe":
                result = os.system(f'cmd /c"{compiler} {build_parameter} -g --std=c++{cpp_version} bin\\obj\\{DirPath}\\*.o -o bin\\build\\{app_name} {libs} {dependencies}"')
            elif app_type == "dll":
                result = os.system(f'cmd /c "{compiler} {build_parameter} -g --std=c++{cpp_version} -shared -o bin\\build\\{app_name}.dll  bin\\obj\\{DirPath}\\*.o -Wl,--out-implib,bin\\build\\lib{app_name}.a {libs} {dependencies}')
            else:
                result = 1
                Log(FAIL, f"[LINKER]{app_type} does not exist or we do not support it")
            if result == 0:
                Log(OKGREEN, f"[LINKER] Successfully created {app_name}.{app_type}")
            else:
                Log(FAIL, f"[LINKER] Failed to create {app_name}.{app_type}")
        elif compiled == 0:
            Log(WARNING, f"[LINKER] Linking ... (SKIP)")
        Log(OKGREEN, "")
        Log(OKGREEN, "")
        for dir in ressource_dir:
            if CheckIfPathExist(f"{dir}"):
                copyDir(dir)
            else:
                Log(WARNING, f"{dir} was not found")
        for dir in nece_files:
            if CheckIfPathExist(f"{dir}"):
                copyToDir(dir)
            else:
                Log(WARNING, f"{dir} was not found")

    
def main():
    if "create_" in argument:
        dir_name = argument.split("create_")[1]
        CreateDir(dir_name)
        CreateFile(f"{dir_name}\\build.txt")
        CreateBuildTemplate(f"{dir_name}\\build.txt", dir_name)
    elif "recompile_" in argument:
        dir_name = argument.split("recompile_")[1]
        if CheckIfPathExist(dir_name):
            if CheckIfPathExist(f"bin\\obj\\{dir_name}"):
                removeDir(f"bin\\obj\\{dir_name}")
            build(dir_name)
        else:
            print(f"{dir_name} does not exist")
        run_app()
    elif "compile_" in argument:
        dir_name = argument.split("compile_")[1]
        if CheckIfPathExist(dir_name):
            build(dir_name)
        else:
            print(f"{dir_name} does not exist")
        run_app()
    else:
        if "recompileall" in argument:
            if CheckIfPathExist("bin"):
                removeDir("bin")



        # Find directories in project
        dirs = []
        for file in os.listdir("./"):
            if os.path.isdir(file):
                if os.path.exists(f"{file}\\build.txt"):
                    dirs.append(file)


        if len(dirs) == 0:
            print("no directory found. You may want to use : python Compiler.py create_foldername") 
        else:
            start = time.time();
            for dir in dirs:
                if CheckIfPathExist(f"{dir}\\build.txt"):
                    build(dir)
            end = time.time();
            run_app()
            Log(OKBLUE, f"Compilation took: {round(end - start, 4)} seconds")

        
    

if "__main__" == __name__:
    main()
