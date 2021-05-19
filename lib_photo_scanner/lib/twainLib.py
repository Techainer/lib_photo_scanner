import twain
from PIL import Image
from io import StringIO
import uuid 
import base64
import os 
from .log import logger

#======================================================================
#	Name:	    twainLib
#   Location:   https://github.com/soachishti/pyScanLib
#	License:    BSD 2-Clause License
#======================================================================

class twainLib(object):

    """
    The is main class of Twain API (Win32)
    """

    def __init__(self):
        self.scanner = None
        self.dpi = 200  # Define for use in pixeltoInch function
        self.scannerName = None 
        self.sourceManager = None
        self.scanner = None

    def getScanners(self):
        """
        Get available scanner from twain module
        """
        if self.sourceManager is None:
            self.sourceManager = twain.SourceManager(0)
        scanners = [x for x in self.sourceManager.GetSourceList() if x != "SaneTwain"]
        if scanners:
            return scanners
        else:
            return None

    def setScanner(self, scannerName):
        """
        Connected to Scanner using Scanner Name

        Arguments:
        scannerName -- Name of Scanner return by getScanners()
        """
        self.scannerName = scannerName
        self.scanner = self.sourceManager.OpenSource(scannerName)

    def setDPI(self, dpi):
        """
        Set DPI to selected scanner and dpi to self.dpi
        """
    
        if self.scanner == None:
            raise ScannerNotSet
        
        self.dpi = dpi

        self.scanner.SetCapability(
            twain.ICAP_XRESOLUTION, twain.TWTY_FIX32, float(self.dpi))
        self.scanner.SetCapability(
            twain.ICAP_YRESOLUTION, twain.TWTY_FIX32, float(self.dpi))

    def setScanArea(self, left=0.0, top=0.0, width=8.267, height=11.693):
        """
        Set Custom scanner layout to selected scanner in Inches

        Arguments:
        left -- Left position of scanned Image in scanner 
        top -- Top position of scanned Image in scanner
        width(right) -- Width of scanned Image
        bottom(height) -- Height of scanned Image
        """

        if self.scanner == None:
            raise ScannerNotSet

        #((left, top, width, height) document_number, page_number, frame_number)
        width = float(width)
        height = float(height)
        left = float(left)
        top = float(top)
        self.scanner.SetImageLayout((left, top, width, height), 1, 1, 1)

    # size in inches
    def getScannerSize(self):
        """
        Return Scanner Layout as Tuple (left, top, right, bottom) in Inches       
        """
    
        if self.scanner == None:
            raise ScannerNotSet

        return self.scanner.GetImageLayout()

    def setPixelType(self, pixelType):
        """
        Set pixelType to selected scanner

        Arguments:
        pixelType -- Pixel type - bw (Black & White), gray (Gray) and color(Colored)
        """
        
        if self.scanner == None:
            raise ScannerNotSet

        self.pixelType = pixelType

        pixelTypeMap = {'bw': twain.TWPT_BW,
                        'gray': twain.TWPT_GRAY,
                        'color': twain.TWPT_RGB}
        try:
            pixelType = pixelTypeMap[pixelType]
        except:
            pixelType = twain.TWPT_RGB
        self.scanner.SetCapability(
            twain.ICAP_PIXELTYPE, twain.TWTY_UINT16, pixelType)

    def scan(self, scanner_name:str=None, return_type:str="image"):
        """
        Scan and return PIL object if success else return False
        return_type: image, path, based64
        """
        curr_folder = os.path.dirname(__name__)
        image_path = os.path.join(curr_folder, "{0}.bmp".format(uuid.uuid4()))

        if scanner_name is None:
            scanner_name = self.scannerName
        twain.acquire(image_path, ds_name=scanner_name, dpi=self.dpi, pixel_type=self.pixelType)

        if return_type == "path":
            return image_path
        elif return_type == "image":
            image = Image.open(image_path)

            os.remove(image_path) if os.path.exists(image_path) else None
            return image
        elif return_type == "based64":
            with open(image_path, "rb") as image_file:
                image = base64.b64encode(image_file.read()).decode('ascii')
            os.remove(image_path) if os.path.exists(image_path) else None
            return image

        return False

    def closeScanner(self):
        """
        Destory 'self.scanner' class of twain module generated in setScanner function
        """
        if self.scanner:
            self.scanner.destroy()
        self.scanner = None

    def scanPreview(self):
        """
        Show preview of image while scanning in progress.
        """
        raise NotImplementedError

    def close(self):
        """
        Destory 'self.sourceManager' class of twain module generated in getScanners function
        Destory 'self.scanner' class of twain module generated in setScanner function
        """
        if self.scanner:
            self.scanner.destroy()
        if self.sourceManager:
            self.sourceManager.destroy()
        (self.scanner, self.sourceManager) = (None, None)