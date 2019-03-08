# ImgUploader
Image upload API 
## Installation
Please clone this GIT repository
```buildoutcfg
git clone https://gitlab.com/miloszsobiczewski/imguploader.git/
```
Then just run
```buildoutcfg
sudo docker-compose up
```
After docker image installation is complete you can find the application 
running in you browser under following url:
```buildoutcfg
0.0.0.0:8000
```
## How to use

### Options

Interface of the application allows to select few options from drop-downs:
* Location - for upload storage type: Google Drive or local HD
* Size - for image compression. For more details see "Picture Compression"
* Picture - select picture you want to upload

### Database

Standard Django SQLite database was used.
All saved image data can be find here:
```buildoutcfg
http://0.0.0.0:8000/admin/ImgUploader/image/
```
login: `new`

password: `New_12345`

### Google Drive storage

Free Google Drive storage account was used for purpouse of this application 
with
Google Drive API enabled.

## Details

### Picture compression
Uploading picture is compressed by resizing it to one of the available  
formats: 800x600 or 480x640. Each picture is checked for its pixel dimension
and reduced to match overall proportions. Smaller images are not changed.

Example:
* picture_1 of size 800x1000 in case of 800x600 "Size" selection is reduced by 
60% to 480x600 pixels.
* picture_2 of size 200x200 will not be changed no mather what "Size"
option will be selected.

