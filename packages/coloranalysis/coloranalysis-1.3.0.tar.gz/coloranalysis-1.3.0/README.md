# **coloranalysis**
coloranalysis is a python package for calculating the percentage of area covered by one or more colors in an image.

### **Prerequisites**
numpy, opencv and matplotlib are required to execute coloranalysis, you can download them using the following commands:
```
pip install numpy
pip install opencv-python
pip install matplotlib
```

### **Installing**
You can either clone or download this repository, or use this command:
```
pip install coloranalysis
```

### **Usage**

See [this notebook](https://github.com/sravyadhulipala/coloranalysis/blob/master/example/colorAreasExample.ipynb) for an example program on how to use this package. However, reading this document entirely is recommended.

Let us consider this image of a rainbow. 

<img src=https://github.com/sravyadhulipala/coloranalysis/blob/master/example/IPTestRainbow.jpg width="400" height="200">

To know the area covered by red color, or the area covered by multiple colors in the image, we should get the HEX codes using a [colorpicker.](https://imagecolorpicker.com/)

In the above image, HEX codes of all colors are: ["#FE0000", "#FD6400", "#FFFF02", "#008101", "#0000FE", "#4B0081", "#BC31FD"]

Import colorArea, the class that calculates the area of the colors we want, as follows. 
```
from coloranalysis.colors import colorAreas
```
*colorAreas takes no arguments.*

**getArea** 

*returns* a list of the percentages of area covered by the given colors.

*arguments* 

- **hexColours**: A list of strings representing the HEX codes.
- **path**: A string specifying the path of the image.
- **diff**: An integer to determine the lower and upper boundaries of the given colors, in the HSV color space.

*hexColours - colour with a 'u'*

For a digital image as above, the recommended *diff* value is 10. While the recommended *diff* value for images of real-life objects is 30-50. 
For more information on HSV color space, see [this link.](https://www.linuxtopia.org/online_books/graphics_tools/gimp_advanced_guide/gimp_guide_node51.html)

**detectColor**

*returns* a tuple with 'mask' and 'result' representing the pixels that match a single color

*arguments*
- **colour**: Values of the color in HSV color space, in the range H[0-360], S[0-100], V[0-100]
- **img**: A numpy array returned by cv2.imread()
- **hsv_img**: A numpy array returned by cv2.cvtColor()
- **diff**: An integer to determine the lower and upper boundaries of the given colors, in the HSV color space.

*colour - colour with a 'u'*

'mask' and 'result' can be used to visualize the presence of the color in the given image

**convertHEXColours**

*returns* a tuple with two lists representing values of the colors in HSV colorspace and RGB colorspace respectively.

*arguments* 
- **hexColours**: A list of strings representing the HEX codes.
