from PIL import Image


def get_ratio(img, resolution):

    new_size = resolution.split('x')
    size = img.size

    (x, y) = (float(new_size[0]) / float(size[0]),
              float(new_size[1]) / float(size[1]))
    ratio = min(x, y)
    return ratio


def save_img(img, img_save_url, ratio):

    size = img.size
    # pdb.set_trace()
    if ratio < 1:
        img = img.resize((int(ratio * size[0]), int(ratio * size[1])),
                         Image.ANTIALIAS)
        img.save(img_save_url)
    else:
        img.save(img_save_url)
    new_size = Image.open(img_save_url).size
    img.close()
    return new_size
