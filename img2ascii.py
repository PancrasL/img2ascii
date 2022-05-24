import cv2
import os
import numpy as np
from colr import color as cl

class Config():
    def __init__(self):
        self.filepath = './images/pic.jpg'
        self.output = './'
        self.color_disable = True
        self.similarity = 5000
        self.width_limit = 150
        self.height_limit = None
        self.save_file = False
        self.symbols = ".o*<c~>|/\znw^@abcdefg"
    def __str__(self):
        return "filepath=%s,output=%s,color_disable=%s,similarity=%s,symbols=%s" % \
            (self.filepath, self.output, self.color_disable, self.similarity,str(self.symbols))

class AsciiImg(object):
    def __init__(self, config):
        self.config = config

    # 将转换后的ASCII图片显示在终端
    def show(self):
        print(self.convert())
        return

    # 将转换后的ASCII图片保存到文件
    def save(self):
        filename = os.path.basename(self.config.filepath)
        # front=文件名，ext=扩展名
        front, ext = os.path.splitext(filename)
        ascii_filepath = self.config.output+front+"_ascii.txt"
        open(ascii_filepath, 'w').write(self.convert())
        print('file saved in {}'.format(self.config.output))
        return

    # 将原始图片转换为ASCII图片
    def convert(self):
        #img = cv2.imread(self.config.filepath)
        img = cv2.imdecode(np.fromfile(self.config.filepath, dtype=np.uint8),-1)
        wstep, hstep = self._get_transformation_steps(
            img, self.config.width_limit, self.config.height_limit)

        img = img[0::hstep+1].transpose(1, 0, 2)[0::wstep+1].transpose(1, 0, 2)

        symbol_color_map = self._extract_valid_colors(
            img, self.config.similarity)

        result = self._draw_image(img, symbol_color_map,
                            color_disable=self.config.color_disable)
        return result

    def _get_transformation_steps(self, img, width_limit=None, height_limit=None):
        height,width,_ = img.shape
        if width_limit:
            height_limit = int(width_limit * height/(width+1000))
        elif height_limit:
            width_limit = int(height_limit * width/height)
        else:
            return [0, 0]
        wstep = int(width/width_limit)
        hstep = int(height/height_limit)
        return [wstep, hstep]


    def _extract_valid_colors(self, img, similarity):
        symbols = self.config.symbols
        symbol_color_map = {}
        height,width,_ = img.shape
        # convert image to linear array of color strings
        img = img.reshape(height*width, 3).tolist()
        img_string = np.array([','.join([str(x) for x in t]) for t in img])
        color_frequency = np.unique(img_string, return_counts=True)
        temp_color_frequency = []
        for t in np.argsort(color_frequency, 1)[1]:
            temp_color_frequency.append(color_frequency[0][t])

        color_frequency = [t for t in temp_color_frequency]
        color_frequency.reverse()

        symbol_color_map[color_frequency[0]] = symbols[0]

        last_used_color = color_frequency[0]
        current_symbol = 1
        updated = True

        while(updated and current_symbol < len(symbols)):
            marked = None
            updated = False
            for color in color_frequency:
                if symbol_color_map.get(color, '') == '':
                    if(self._dist(last_used_color, color) < similarity):
                        symbol_color_map[color] = symbol_color_map[last_used_color]
                    elif not marked:
                        symbol_color_map[color] = symbols[current_symbol]
                        current_symbol = current_symbol+1
                        marked = color
                        updated = True
            last_used_color = marked

        return symbol_color_map


    def _dist(self, s1, s2):
        s1 = s1.split(',')
        s2 = s2.split(',')
        return (int(s1[0])-int(s2[0]))**2+(int(s1[1])-int(s2[1]))**2+(int(s1[2])-int(s2[2]))**2

    def _draw_image(self, img, symbol_color_map, color_disable):
        result = ''
        for px_list in img:
            temp_result = ''
            for px in px_list:
                color = ','.join([str(t) for t in px])
                try:
                    pixels = px.tolist()
                    pixels.reverse()

                    if not color_disable:
                        pxvalue = cl(symbol_color_map[color], fore=pixels)
                    else:
                        pxvalue = symbol_color_map[color]

                    temp_result = temp_result+pxvalue
                except:
                    temp_result = temp_result+' '
            result = result + '\n' + temp_result

        return result


if __name__ == "__main__":
    global_config = Config()
    asciiImg = AsciiImg(global_config)
    if global_config.save_file:
        asciiImg.save()
        asciiImg.show()
    else:
        asciiImg.show()
