from PIL import Image
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


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


def gd_connect(config="mycreds.txt"):
    """
    Google Drive connector
    :param config:
    :return:
    """
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile(config)
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(config)

    drive = GoogleDrive(gauth)
    return drive


def gd_upload(drive, img_url):
    """
    Google Drive API function for file upload
    :return:
    """
    # remove /
    if img_url[0] == '/':
        img_url = img_url[1:]
    try:
        with drive.CreateFile({'title': img_url.split('/')[-1],
                                 "parents": [{
                                     "kind": "drive#fileLink",
                                     "id": '1w7hKYp3uwDGqprNsoic_Yo0_XRCDiu4v'
                                 }]}) as file:
            file.SetContentFile(img_url)
            file.Upload()
            return True
    except:
        return False


def get_gd_file_details(drive, img_url):
    """
    Retrieve file details from Google Drive (id, name, shared link,
    image metadata, file size)
    :param pic_url:
    :return: uploaded file details
    """
    # get exact file name
    img_name = img_url.split('/')[-1]
    # search for file details
    file = drive.ListFile({'q': "trashed=false and title='%s'" % img_name}
                               ).GetList()[0]
    detl = {
        'id': file['id'],
        'title': file['title'],
        'embedLink': file['embedLink'],
        'imageMediaMetadata': file['imageMediaMetadata'],
        'fileSize': file['fileSize']
    }
    return detl
