import os
import unittest
from PIL import Image
import ImgUploader.utils as ut
import pdb


class ImgUploaderUnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.small_img_url = r"static/small_img.png"
        self.small_img_save_url = r"media/small_img.png"
        self.small_img = Image.open(self.small_img_url)
        self.big_img_url = r"static/big_img.jpg"
        self.big_img_save_url = r"media/big_img.png"
        self.big_img = Image.open(self.big_img_url)

    def test_001_get_ratio(self):

        ratio = ut.get_ratio(self.big_img, '800x600')
        print('test_001_get_ratio', ratio)
        self.assertGreater(ratio, 0)

    def test_002_save_img(self):

        # resize big image
        ratio = ut.get_ratio(self.big_img, '800x600')
        new_size = ut.save_img(self.big_img, self.big_img_save_url, ratio)
        print('test_002_resizing 800x600', new_size)
        self.assertTrue(new_size[0] == 800 or new_size[1] == 600)

        # do not resize image
        ratio = ut.get_ratio(self.small_img, '800x600')
        new_size = ut.save_img(self.small_img, self.small_img_save_url, ratio)
        print('test_002_resizing 800x600', new_size)
        self.assertTrue(new_size[0] < 800 and new_size[1] < 600)

    @classmethod
    def tearDownClass(self):

        # remove copies files
        os.remove(self.small_img_save_url)
        os.remove(self.big_img_save_url)
        pass


if __name__ == '__main__':
    unittest.main()




