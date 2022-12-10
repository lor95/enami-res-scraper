import fitz
from .helpers import prepare_download_folders
import os

class PDFLoader:
    
    def __init__(self, pdf_path, download_path):
        doc = fitz.open(pdf_path)
        page_count = doc.page_count
        xreflist = []
        imglist = []
        for pno in range(page_count):
            il = doc.get_page_images(pno)
            imglist.extend([x[0] for x in il])
            for img in il:
                xref = img[0]
                if xref in xreflist:
                    continue
                image = self.recoverpix(doc, img)
                n = image["colorspace"]
                imgdata = image["image"]
                
                imgfile = os.path.join(prepare_download_folders(download_path,os.path.basename(pdf_path),"PDF"), "img%05i.%s" % (xref, image["ext"]))
                fout = open(imgfile, "wb")
                fout.write(imgdata)
                fout.close()
                xreflist.append(xref)

    def recoverpix(self, doc, item):
        xref = item[0]
        smask = item[1]

        if smask > 0:
            pix0 = fitz.Pixmap(doc.extract_image(xref)["image"])
            if pix0.alpha:
                pix0 = fitz.Pixmap(pix0, 0)
            mask = fitz.Pixmap(doc.extract_image(smask)["image"])

            try:
                pix = fitz.Pixmap(pix0, mask)
            except:
                pix = fitz.Pixmap(doc.extract_image(xref)["image"])

            if pix0.n > 3:
                ext = "pam"
            else:
                ext = "png"

            return {
                "ext": ext,
                "colorspace": pix.colorspace.n,
                "image": pix.tobytes(ext),
            }

        if "/ColorSpace" in doc.xref_object(xref, compressed=True):
            pix = fitz.Pixmap(doc, xref)
            pix = fitz.Pixmap(fitz.csRGB, pix)
            return {
                "ext": "png",
                "colorspace": 3,
                "image": pix.tobytes("png"),
            }
        return doc.extract_image(xref)