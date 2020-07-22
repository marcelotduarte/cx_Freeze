import sys, os, site

from typing import List, Tuple

def getQtPluginIncludes(pluginList: List[str]) -> List[Tuple[str,str]]:
    includes = []
    for ppath in pluginList:
        includes.append(_getInclude(ppath))
        pass
    return includes

def _getInclude(pluginPath: str) -> Tuple[str,str]:
    foundPath = None

    if sys.platform == "darwin":
        packagesDirs = [c for c in sys.path if c.find("site-packages")!=-1]
    else:
        packagesDirs = site.getsitepackages()  # search site packages locations to see if we can find required .dll
        pass
    for pdir in packagesDirs:
        testPath = os.path.join(pdir, os.path.join("PyQt5", "Qt", "plugins", pluginPath ))
        bname = os.path.basename(pluginPath)

        # print("Checking for {} at {}".format(bname, testPath))
        if os.path.exists(testPath):
            foundPath = testPath
            # print("DLL Found")
            break
        pass
    if foundPath is None:
        print("Error, could not find: {}".format(pluginPath))
        sys.exit(1)

    return (foundPath, pluginPath)
