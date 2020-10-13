import numpy as np
from PIL import Image

from srp_rw import pysrp

srp = pysrp.Srp()
srp.open('H:/transSrp/SZSQ_originaldata/Tongji_7th/positive/tj19071287.srp')

# srp.say_hello()

attrs = srp.getAttrs()
print(attrs)

img = srp.ReadRegionRGB(0, 30000, 30000,  1024, 1024)
if img is not None:
    nimg = np.ctypeslib.as_array(img)
    nimg.dtype = np.uint8
    nimg = nimg.reshape((1024, 1024, 3))
    im = Image.fromarray(np.uint8(nimg))
    im.save("aa.jpg", "JPEG")
    print(np.shape(im))
else:
    print('read img is None')


#srp.CleanAnno()

#srp.WriteAnno(3000, 3000, 0.9876)
#srp.WriteScore(0.65)

# srp.WriteManualAnnoRect("123451", 1000, 1000, 2000, 2000)
#srp.CleanManualAnno()

# annos = srp.ReadManualAnno()
# print(annos)


srp.close()