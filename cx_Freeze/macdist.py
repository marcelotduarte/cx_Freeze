from distutils.core import Command
import distutils.errors
import distutils.util
import os
import stat
import subprocess

__all__ = [ "bdist_dmg", "bdist_mac" ]

PLIST_TEMPLATE = \
"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleIconFile</key>
	<string>%(bundle_iconfile)s</string>
	<key>CFBundleDevelopmentRegion</key>
	<string>English</string>
	<key>CFBundleExecutable</key>
	<string>%(bundle_executable)s</string>
</dict>
</plist>
"""

class bdist_dmg(Command):
    description = "create a Mac DMG disk image containing the Mac application bundle"
    user_options = [
        ('volume-label=', None, 'Volume label of the DMG disk image'),
    ]

    def initialize_options(self):
        self.volume_label = self.distribution.get_fullname()

    def finalize_options(self):
        pass

    def buildDMG(self):
        # Remove DMG if it already exists
        if os.path.exists(self.dmgName):
            os.unlink(self.dmgName)

        # Create the dmg
        if os.spawnlp(os.P_WAIT,'hdiutil','hdiutil','create','-fs','HFSX',
            '-format','UDZO',self.dmgName, '-imagekey', 'zlib-level=9',
            '-srcfolder',self.bundleDir,'-volname',self.volume_label)!=0:
            raise OSError('creation of the dmg failed')

    def run(self):
        # Create the application bundle
        self.run_command('bdist_mac')

        # Find the location of the application bundle and the build dir
        self.bundleDir = self.get_finalized_command('bdist_mac').bundleDir
        self.buildDir = self.get_finalized_command('build').build_base

        # Set the file name of the DMG to be built
        self.dmgName = os.path.join(self.buildDir, self.distribution.get_fullname() + '.dmg')

        self.execute(self.buildDMG,())


class bdist_mac(Command):
    description = "create a Mac application bundle"

    user_options = [
        ('bundle-iconfile=', None, 'Name of the application bundle icon file as stored in the '
                'Info.plist file'),
        ('qt-app=', None, 'Make specific changes for a Qt application.'),
    ]

    def initialize_options(self):
        self.bundle_iconfile = 'icon.icns'
        self.qt_app = False

    def finalize_options(self):
        pass

    def create_plist(self):
        """Create the Contents/Info.plist file"""
        plist = open(os.path.join(self.contentsDir, 'Info.plist'),'w')
        plist.write(PLIST_TEMPLATE % self.__dict__)
        plist.close()

    def setRelativeReferencePaths(self):
        """ For all files in Contents/MacOS, check if they are binaries
            with references to other files in that dir. If so, make those references
            relative. The appropriate commands are applied to all files; they will
            just fail for files on which they do not apply."""
        files = os.listdir(self.binDir)
        for file in files:
            filepath = os.path.join(self.binDir, file)

            #Ensure write permissions
            mode = os.stat(filepath).st_mode
            if not (mode & stat.S_IWUSR):
                os.chmod(filepath, mode | stat.S_IWUSR)

            #Let the file itself know its place
            subprocess.call(('install_name_tool','-id','@executable_path/'+file,filepath))

            #Find the references: call otool -L on the file and read lines [1:]
            otool = subprocess.Popen(('otool','-L', filepath),stdout=subprocess.PIPE)
            references = otool.stdout.readlines()[1:]

            for reference in references:
                # Find the actual referenced file name
                referencedFile = reference.decode().strip().split()[0]

                if referencedFile.startswith('@'):
                    #The referencedFile is already a relative path
                    continue

                path, name = os.path.split(referencedFile)

                # See if we provide the referenced file, if so, change the reference
                if name in files:
                    newReference='@executable_path/'+name
                    subprocess.call(('install_name_tool', '-change', referencedFile, newReference,
                            filepath))

    def qt_tweaks(self):
        self.copy_tree('/opt/local/lib/Resources/qt_menu.nib',\
                       os.path.join(self.resourcesDir, 'qt_menu.nib'))
        # This needs to exist, but needn't have any content
        f = open(os.path.join(self.resourcesDir, 'qt.conf'), "w")
        f.close()

    def run(self):
        self.run_command('build')
        build = self.get_finalized_command('build')

        # Define the paths within the application bundle
        self.bundleDir = os.path.join(build.build_base, self.distribution.get_fullname()+".app")
        self.contentsDir = os.path.join(self.bundleDir, 'Contents')
        self.resourcesDir = os.path.join(self.contentsDir, 'Resources')
        self.binDir = os.path.join(self.contentsDir, 'MacOS')

        #Find the executable name
        executable = self.distribution.executables[0].targetName
        _, self.bundle_executable=os.path.split(executable)

        # Build the app directory structure
        self.mkpath(self.resourcesDir)
        self.mkpath(self.binDir)

        self.copy_tree(build.build_exe, self.binDir)

        # Create the Info.plist file
        self.execute(self.create_plist,())

        # Make all references to libraries relative
        self.execute(self.setRelativeReferencePaths,())
        
        # For a Qt application, run some tweaks
        if self.qt_app:
            self.execute(self.qt_tweaks, ())

