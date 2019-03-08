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
        """
        - check calculation of ratio between original image size and inputed
        - no image files will not be tested because of Django ImageField
        :return:
        """
        ratio = ut.get_ratio(self.big_img, '800x600')
        print('test_001_get_ratio', ratio)
        self.assertGreater(ratio, 0)

    def test_002_save_img(self):
        """
        - check if big files are resized correctly
        - check if small files are not resized
        :return:
        """
        # resize big image
        ratio = ut.get_ratio(self.big_img, '800x600')
        ut.save_img(self.big_img, self.big_img_save_url, ratio)
        self.big_img.close()
        new_size = Image.open(self.big_img_save_url).size
        print('test_002_resizing 800x600', new_size)
        self.assertTrue(new_size[0] == 800 or new_size[1] == 600)

        # do not resize image
        ratio = ut.get_ratio(self.small_img, '800x600')
        ut.save_img(self.small_img, self.small_img_save_url, ratio)
        self.small_img.close()
        new_size = Image.open(self.small_img_save_url).size
        print('test_002_resizing 800x600', new_size)
        self.assertTrue(new_size[0] < 800 and new_size[1] < 600)

    def test_003_gd_upload(self):
        """
        - compare file size before and after GD upload
        :return:
        """
        drive = ut.gd_connect()
        ut.gd_upload(drive, self.small_img_url)
        detl = ut.get_gd_file_details(drive, self.small_img_url)
        stat = os.stat(self.small_img_url)
        print('test_003_gd_upload', detl['fileSize'], stat.st_size)
        self.assertEqual(int(detl['fileSize']), stat.st_size)
        # delete GD file
        ut.gd_delete(drive, detl['id'])

    @classmethod
    def tearDownClass(self):

        # remove copies files
        os.remove(self.small_img_save_url)
        os.remove(self.big_img_save_url)


if __name__ == '__main__':
    unittest.main()




