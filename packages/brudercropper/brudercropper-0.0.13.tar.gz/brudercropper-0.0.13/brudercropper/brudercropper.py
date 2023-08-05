import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from abc import ABC, abstractmethod

import barcode
import cv2
import pytesseract
from PIL import Image
from barcode.writer import ImageWriter


class Barcode:
    @staticmethod
    def decode(im):
        image = im
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        filename = os.path.join(tempfile.mkdtemp(), next(tempfile._get_candidate_names())+".png")
        cv2.imwrite(filename, gray)

        text = pytesseract.image_to_string(Image.open(filename))
        os.remove(filename)
        print("{fn} = ".format(fn=filename) + text)
        return text

    @staticmethod
    def createbarcode(text):
        proper = text.replace(".", "").replace(" ", "")
        itf = barcode.get_barcode_class('itf')
        bc = itf(proper, writer=ImageWriter())

        outf = os.path.join(tempfile.mkdtemp(), next(tempfile._get_candidate_names())+".png")

        with open(outf, "wb") as f:
            bc.write(f, text=text, options={
                "module_width": 0.22,
                "module_height": 24.0,
                "font_size": 20
            })

        return (Image.open(outf), outf)

GSPATH = None
for i in os.getenv("PATH").split(";"):
    cp = os.path.join(i, "gswin32c.exe")
    if os.path.exists(cp):
        GSPATH = cp
        break

    cp = os.path.join(i, "gs")
    if os.path.exists(cp):
        GSPATH = cp
        break

if GSPATH is None:
    print("gs / gswin32c not in path")
    sys.exit(1)


class Section:
    xoff = 0.0
    yoff = 0.0

    xwidth = 0.0
    yheight = 0.0

    xbox = 0.0
    ybox = 0.0

    data = None

    def __init__(self, xoff, yoff, xwidth=None, yheight=None, xbox=None, ybox=None, margin=0):
        self.xoff = xoff
        self.yoff = yoff
        self.xwidth = xwidth
        self.yheight = yheight
        self.margin = margin

        if xbox:
            self.xbox = xbox
        else:
            self.xbox = self.xoff + self.xwidth

        if ybox:
            self.ybox = ybox
        else:
            self.ybox = self.yoff + self.yheight


class Crop(ABC):
    infile = ""
    sections = []
    srcimg = None
    logofile = None

    def __init__(self, infile, logofile):
        self.infile = self.pdf2tif(infile)
        self.logofile = logofile

        self.srcimg = Image.open(self.infile)
        self.dpi = self.srcimg.info['dpi']

    @staticmethod
    def mmtopixels(mm, resolution):
        return round(mm/254*resolution)

    @staticmethod
    def pixelstomm(pixels, resolution):
        return round(pixels/resolution*254)

    def addsection(self, xoff, yoff, xwidth, yheight):
        s = Section(xoff, yoff, xwidth, yheight)
        self.sections.append(s)

    def cut(self):
        for c in self.sections:
            c.data = "Fuck"

            cropped = self.srcimg.crop((c.xoff, c.yoff, c.xbox, c.ybox))
            cropped.load()
            c.data = cropped

    def pdf2tif(self, fp):
        outf = os.path.join(tempfile.mkdtemp(), next(tempfile._get_candidate_names()))
        inf = os.path.join(tempfile.mkdtemp(), next(tempfile._get_candidate_names()))

        shutil.copy(fp, inf)

        tpl = "{gs} -q -dNOPAUSE -sDEVICE=tiffg4 -sOutputFile={out} {inf} -c quit".format(gs=GSPATH, out=outf, inf=inf)
        proc = subprocess.run(tpl, shell=False)

        if proc.returncode != 0:
            print("Error converting {inf} to TIFF. Error:\n\n{stdout}\n{stderr}".format(inf=self.infile,
                                                                                        stdout=proc.stdout,
                                                                                        stderr=proc.stderr))
            sys.exit(1)

        os.remove(inf)

        #todo
        shutil.copy(outf, "../outf.tif")

        return outf

    @abstractmethod
    def save(self):
        pass


class DHL(Crop):
    def __init__(self, infile, logo):
        super(DHL, self).__init__(infile, logo)

        # edit here
        data = [
            # Section(xoff=Crop.mmtopixels(1777, 204),
            #         yoff=Crop.mmtopixels(12342, 196),
            #         xwidth=Crop.mmtopixels(1880, 204),
            #         yheight=-Crop.mmtopixels(7129, 196)),
            # 0
            Section(xoff=53,
                    yoff=655,
                    xbox=133+5,
                    ybox=956,
                    margin=0),
            # 1
            Section(xoff=48,
                    yoff=199,
                    xbox=128,
                    ybox=417,
                    margin=0),
            # 2
            Section(xoff=993,
                    yoff=186,
                    xwidth=26,
                    yheight=774,
                    margin=10),
            # 3
            Section(xoff=140+5,
                    yoff=405,
                    xwidth=140,
                    yheight=551,
                    margin=10),
            # 4
            Section(xoff=288,
                    yoff=405-5,
                    xwidth=309-1,
                    yheight=551+9),
            # 5
            Section(xoff=604,
                    yoff=183,
                    xbox=1013,
                    ybox=953,
                    margin=20),
            # 6
            Section(xoff=1044,
                    yoff=350-30,
                    xbox=1291-26,
                    ybox=778+14+20),
            # 7
            Section(xoff=1292-5,
                    yoff=188,
                    xbox=1308+2,
                    ybox=955,
                    margin=10),
            # 8
            Section(xoff=1333,
                    yoff=363,
                    xbox=1585,
                    ybox=768),
            # 9
            Section(xoff=1260,
                    yoff=473,
                    xwidth=34,
                    yheight=203),
            # 10
            Section(xoff=1555,
                    yoff=484,
                    xwidth=30,
                    yheight=181)

        ]
        for elem in data:
            self.sections.append(elem)

    def save(self):
        ofs = 0
        timg = Image.new("RGB", (Crop.mmtopixels(62*10, 300), Crop.mmtopixels(170*10, 300)), (255,255,255))

        tpaketlabel = self.sections[0]
        paketlabel = tpaketlabel.data.rotate(270, expand=True)
        timg.paste(paketlabel, (0, ofs))
        ofs += paketlabel.height + tpaketlabel.margin

        tdhllabel = self.sections[1]
        dhllabel = tdhllabel.data.rotate(270, expand=True)
        timg.paste(dhllabel, (550-50, 0))
        #ofs += dhllabel.height + t.margin

        tstrich = self.sections[2]
        strich = tstrich.data.rotate(270, expand=True)
        timg.paste(strich, (0, ofs))
        ofs += strich.height + tstrich.margin

        tstrich = self.sections[3]
        absender = tstrich.data.rotate(270, expand=True)
        # absender = absender.resize((137, 34), Image.LANCZOS)
        timg.paste(absender, (0, ofs))
        ofs += absender.height + tstrich.margin

        trec = self.sections[4]
        receiver = trec.data.rotate(270, expand=True)
        receiver.save("receiver.tif")
        receiver = receiver.resize((round(183*3.5), round(103*3.5)), Image.LANCZOS)
        timg.paste(receiver, (0, ofs))
        ofs += receiver.height + trec.margin

        timg.paste(strich, (0, ofs))
        ofs += strich.height + tstrich.margin

        tgg = self.sections[5]
        gg = tgg.data.rotate(270, expand=True)
        gg = gg.resize((round(gg.width * 0.95), round(gg.height * 0.95)), Image.LANCZOS)
        timg.paste(gg, (10, ofs))
        ofs += gg.height + tgg.margin
        gg.save("tgg.jpg")

        # tlc = self.sections[6]
        # lc = tlc.data.rotate(270, expand=True)
        # lc = lc.resize((round(lc.width * 1.2), round(lc.height * 1.2)), Image.LANCZOS)
        # timg.paste(lc, (round(timg.width/8), ofs))
        # ofs += lc.height + tlc.margin
        tlcn = self.sections[9]
        lcn = tlcn.data.rotate(270, expand=True)
        tlcnfn = os.path.join(tempfile.mkdtemp(), next(tempfile._get_candidate_names()) + ".png")
        lcn.save(tlcnfn)
        bcv = Barcode.decode(cv2.imread(tlcnfn))
        bcn, fn = Barcode.createbarcode(bcv)
        bcn = bcn.resize((round(bcn.width * 1), round(bcn.height * 1)))
        timg.paste(bcn, (-30, ofs))
        ofs += bcn.height + tlcn.margin

        tfetterstrich = self.sections[7]
        fetterstrich = tfetterstrich.data.rotate(270, expand=True)
        timg.paste(fetterstrich, (0, ofs))
        ofs += fetterstrich.height + tfetterstrich.margin

        # tic = self.sections[8]
        # ic = tic.data.rotate(270, expand=True)
        # ic = ic.resize((round(ic.width * 1.2), round(ic.height * 1.2)), Image.LANCZOS)
        # timg.paste(ic, (round(timg.width/8), ofs))
        # ofs += ic.height + tic.margin

        tic = self.sections[10]
        ic = tic.data.rotate(270, expand=True)
        ticfn = os.path.join(tempfile.mkdtemp(), next(tempfile._get_candidate_names()) + ".png")
        ic.save(ticfn)
        bcv = Barcode.decode(cv2.imread(ticfn))
        bcn, fn = Barcode.createbarcode(bcv)
        bcn = bcn.resize((round(bcn.width * 1.1), round(bcn.height * 1.1)))
        timg.paste(bcn, (-25, ofs))
        ofs += bcn.height + tic.margin

        timg.paste(fetterstrich, (0, ofs))
        ofs += fetterstrich.height + tfetterstrich.margin

        if self.logofile:
            logo = Image.open(self.logofile)

            basewidth = 300
            baseheight = 200
            wpercent = (baseheight / float(logo.size[1]))
            wsize = int((float(logo.size[0]) * float(wpercent)))
            logo = logo.resize((wsize, baseheight), Image.LANCZOS)
            logo = logo.convert('L')

            # logo = logo.resize((round(bcn.width * 1.1), round(bcn.height * 1.1)), Image.LANCZOS)
            timg.paste(logo, (208+50-50,840))

        # timg.show()

        timg.save("result.png", dpi=(200, 200))
        print("Saved to result.png")
        # sys.exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dhl", help="Cropped ein DHL A4 Etikett auf 62mm", action='store_true', required=False)
    parser.add_argument("-i", "--input", help="Inputfile", required=True)
    parser.add_argument("-l", "--logo", help="Dateipfad zu einem optionalen Logo", required=False)
    args = parser.parse_args()

    if args.dhl:
        d = DHL(args.input, args.logo)
        d.cut()
        d.save()


if __name__ == "__main__":
    main()