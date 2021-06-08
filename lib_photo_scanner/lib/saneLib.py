import sane
from .log import logger
import os 
import base64
from io import BytesIO

#======================================================================
#	Name:	    saneLib
#   Location:   https://github.com/soachishti/pyScanLib
#	License:    BSD 2-Clause License
#======================================================================

class saneLib(object):

    """The is main class of SANE API (Linux)
    """

    def __init__(self):
        self.dpi = 200
        self.layout = False
        self.scanner = None

    def getScanners(self):
        """
        Get available scanner from sane module
        """
        sane.init()
        devices = sane.get_devices()
        if len(devices) > 0:
            return devices
        else:
            return None

    def setScanner(self, scannerName):
        """
        Connected to Scanner using Scanner Name
        Arguments:
        scannerName -- Name of Scanner return by getScanners()
        """
        
        self.scanner = sane.open(scannerName)

    def setDPI(self, dpi):
        """
        Set DPI to selected scanner and dpi to self.dpi
        """

        if self.scanner == None:
            raise ScannerNotSet

        self.dpi = dpi
        self.scanner.resolution = self.dpi

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

        # http://www.sane-project.org/html/doc014.html#f5
        # (left, top, right, bottom)
        # top left x axis          left
        self.scanner.tl_x = float(inchTomm(left))
        # top left y axis           top
        self.scanner.tl_y = float(inchTomm(top))
        # bottom left x axis      width
        self.scanner.br_x = float(inchTomm(width))
        # bottom left y axis     height
        self.scanner.br_y = float(inchTomm(height))

    def getScannerSize(self):
        """
        Return Scanner Layout as Tuple (left, top, right, bottom) in Inches      
        """

        return (mmToInch(self.scanner.tl_x), mmToInch(self.scanner.tl_y), mmToInch(self.scanner.br_x), mmToInch(self.scanner.br_y))

    def setPixelType(self, pixelType):
        """
        Set pixelType to selected scanner
        Arguments:
        pixelType -- Pixel type - bw (Black & White), gray (Gray) and color(Colored)
        """

        if self.scanner == None:
            raise ScannerNotSet

        self.scanner.mode = pixelType.lower()

    def scan(self, scanner_name:str=None, return_type:str="image"):
        """
        Scan and return PIL object if success else return False
        return_type: image, path, based64
        """
        
        if self.scanner == None:
            raise ScannerNotSet

        # curr_folder = os.path.dirname(__name__)
        # image_path = os.path.join(curr_folder, "{0}.bmp".format(uuid.uuid4()))

        if scanner_name is None:
            scanner_name = self.scannerName

        # try:
        self.scanner.start()
        image = self.scanner.snap()

        if return_type == "image":
            return image
        elif return_type == "based64":
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
            return img_str
        # except:
        #     return False

    def closeScanner(self):
        """
        Destory 'self.scanner' class of sane module generated in setScanner function
        """
        if self.scanner:
            self.scanner.close()
            del self.scanner
        self.scanner = None

    def scanPreview(self):
        """
        Show preview of image while scanning in progress.
        """
        raise NotImplementedError

    def close(self):
        """
        Destory 'sane' class of sane module generated in getScanners function ie sane.init()
        Destory 'self.scanner' class of sane module generated in setScanner function
        """
        if self.scanner:
            self.scanner.close()
        sane.exit()