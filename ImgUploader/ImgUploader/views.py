import os
from django.shortcuts import render
from PIL import Image
from .forms import ImageForm
from . import utils as ut
from .settings import BASE_DIR


def main(request):
    """
    Main and only django webpage view containing upload form
    :param request:
    :return:
    """
    msg = {'1': 'hello'}
    if request.method == 'POST':
        imageform = ImageForm(request.POST, request.FILES)
        if imageform.is_valid():
            # save image to DB
            instance = imageform.save(commit=False)
            instance.name = instance.picture.name
            instance.url = instance.picture.url
            instance.save()
            url = ut.clean_path(instance.picture.url)

            resize = imageform.cleaned_data['size']
            # open saved image
            with Image.open(url) as img:
                ratio = ut.get_ratio(img, resize)
                # resize and save image
                res = ut.save_reduced_img(img, url, ratio)
            if res:
                new_size = Image.open(url).size
                msg['1'] = 'Image was reduced to %s pixels.' % str(new_size)
            else:
                del msg['1']

            # get upload type
            upload_type = imageform.cleaned_data['location']

            if upload_type == 'local':
                msg['2'] = 'Image was successfully saved to local drive. ' \
                           'DB id: %s ; location: ' % instance.pk
                # location as hyperlink. msg[3] has different style.
                msg['3'] = 'file:///%s%s' % (BASE_DIR, instance.url)
            elif upload_type == 'Google Drive':
                # connect to GD, upload, get details
                drive = ut.gd_connect()
                ut.gd_upload(drive, url)
                detl = ut.get_gd_file_details(drive, url)
                if detl:
                    # delete local file copy
                    os.remove(url)
                    # update url in DB
                    instance.url = detl['embedLink']
                    instance.save()
                    msg['2'] = \
                        'Image was successfully saved to Google Drive ' \
                        'storage. DB id: %s ; link: ' % instance.pk
                    msg['3'] = '%s' % instance.url
                else:
                    msg['2'] = 'Google Drive upload failed.'
            else:
                msg['2'] = 'Option not supported.'
    else:
        imageform = ImageForm()
    return render(request, 'main.html', {'imageform': imageform, 'msg': msg})
