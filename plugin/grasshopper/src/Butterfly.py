# Butterfly: A Plugin for CFD Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Butterfly.
#
# You should have received a copy of the GNU General Public License
# along with Ladybug; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
This component downloads butterfly library from github to:
C:\Users\%USERNAME%\AppData\Roaming\McNeel\Rhinoceros\5.0\scripts\butterfly

-

    Args:
        butterflyFolder_: Optional path to load butterfly libraries instead of the
            installed version
        update_: Optional boolean to update butterfly even if you have it already installed.
    Returns:
        swooooosh: !!!
"""

ghenv.Component.Name = "Butterfly"
ghenv.Component.NickName = "BF::BF"
ghenv.Component.Message = 'VER 0.0.01\nJUL_14_2016'
ghenv.Component.Category = "Butterfly"
ghenv.Component.SubCategory = "00::Create"
ghenv.Component.AdditionalHelpFromDocStrings = "1"

import os
import System
import sys
import zipfile
import shutil


def installButterfly(update):
    
    """
    This code will download butterfly library from github to:
        C:\Users\%USERNAME%\AppData\Roaming\McNeel\Rhinoceros\5.0\scripts\butterfly
    """
    url = "https://github.com/mostaphaRoudsari/butterfly/archive/master.zip"
    targetDirectory = [p for p in sys.path if p.find('scripts')!= -1][0]
    libFolder = os.path.join(targetDirectory, r"butterfly")
    
    if not update and os.path.isdir(libFolder):
        return
    elif update and os.path.isdir(libFolder):
        shutil.rmtree(libFolder)
    
    # download the zip file
    print "Downloading the source code..."
    zipFile = os.path.join(targetDirectory, os.path.basename(url))

    try:
        client = System.Net.WebClient()
        client.DownloadFile(url, zipFile)
    except Exception, e:
        msg = `e` + "\nDownload failed! Try to download and unzip the file manually form:\n" + url
        raise Exception(msg)
        
    #unzip the file
    with zipfile.ZipFile(zipFile) as zf:
        for f in zf.namelist():
            if f.endswith('/'):
                try: os.makedirs(f)
                except: pass
            else:
                zf.extract(f, targetDirectory)
    zf.close()
    
    bfFolder = os.path.join(targetDirectory, r"butterfly-master\butterfly")
    shutil.copytree(bfFolder, libFolder)
    
    # try to clean up
    try:
        shutil.rmtree(os.path.join(targetDirectory, 'butterfly-master'))
        os.remove(zipFile)
    except:
        pass


if not butterflyFolder_:
    installButterfly(update_)
elif update_ and not os.path.isdir(butterflyFolder_):
   installButterfly(update_)
elif os.path.isdir(butterflyFolder_) and butterflyFolder_ not in sys.path:
        sys.path.insert(0, butterflyFolder_)


try:
    import butterfly
    print "Imported butterfly from {}\nswoosh swoosh...".format(butterfly.__file__)
    reload(butterfly)
except ImportError as e:
    raise Exception("Failed to import butterfly:\n{}".format(e))