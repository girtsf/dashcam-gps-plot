#!/usr/local/bin/python3
#
# Plots dots on a geo-referenced image file.

from PIL import Image, ImageFont, ImageDraw

FONT = '/Library/Fonts/Arial Black.ttf'
FONT_SIZE = 48


class GeoLocated:
    """Geolocates points on a Mercator projected image."""

    def __init__(self, p1_pix, p1_coord, p2_pix, p2_coord):
        self.coeffs = [(p2_pix[i] - p1_pix[i]) / (p2_coord[i] - p1_coord[i]) for i in [0, 1]]
        self.pix = p1_pix
        self.coord = p1_coord

    def GetPixel(self, coords):
        out = []
        for i in [0, 1]:
            out.append(int(self.pix[i] + (coords[i] - self.coord[i]) * self.coeffs[i]))
        return out


class Plotter:
    """Plots stuff on top of an existing bitmap."""

    def __init__(self, fn):
        self.image = Image.open(fn)
        self.pixels = self.image.load()
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype(FONT, FONT_SIZE)

    def Cross(self, pix):
        for delta in range(-5, 6):
            self.pixels[pix[1] + delta, pix[0]] = (255, 0, 0)
            self.pixels[pix[1], pix[0] + delta] = (255, 0, 0)

    def Square(self, pix, size):
        for r in range((-size // 2) + 1, (size // 2) + 1):
            for c in range((-size // 2) + 1, (size // 2) + 1):
                self.pixels[pix[1] + r, pix[0] + c] = (255, 0, 0)

    def Text(self, pix, text):
        self.draw.text(pix, text, font=self.font, fill=(255, 0, 0, 200))

    def Save(self, fn):
        self.image.save(fn)


if __name__ == '__main__':
    pixel1 = [134, 104]  # y, x
    coords1 = [41.998466, -124.212002]
    pixel2 = [314, 1304]  # y, x
    coords2 = [43.255725, -79.068634]
    gl = GeoLocated(pixel1, coords1, pixel2, coords2)
    print(gl.GetPixel((42, -122)))
    print(gl.GetPixel((41, -122)))
    print(gl.GetPixel((40, -122)))
    # print(gl.GetPixel((37, -122)))
    im = Plotter('usa_nw.png')
    im.Cross((100, 10))
    im.Square((200, 10), 5)
    im.Text((50, 50), 'foo')
    im.Save('test.png')
