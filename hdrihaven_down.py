import os, sys
from bs4 import BeautifulSoup
import requests
from urllib.request import URLopener
from fake_useragent import UserAgent

# settings
category = "all"  # choose category.
down_sizes = ["1k", "2k", "4k"]  # you can give multiple values 1,2,4,8,16.
down_thumbnail = False  # download thumbnail image.
down_preview = True  # download preview image.
down_spheres = True  # download spheres image.
owerwrite = False  # overwrite if the file exists, otherwise skip.
# down_folder = "C:\\Users\\agm\\Documents\\GitHub\\hdrihaven_down\\dw"

# urlopener
urlopener = URLopener()
urlopener.addheader("User-Agent", UserAgent().chrome)

# soup
url = "https://hdrihaven.com/hdris/?c=" + category
r = requests.get(url, headers={"User-Agent": UserAgent().chrome})
soup = BeautifulSoup(r.content, "lxml")
items = soup.find("div", id="item-grid").find_all("a")

# filelist
files = [
    f
    for f in os.listdir(".")
    if os.path.isfile(f) and f.endswith((".jpg", ".hdr", ".exr"))
]

# down operator
def downloader(url, ext, filename):
    for i in down_sizes:
        file = filename + "_" + i
        if file + ext in files:
            print("Already exist: " + file + ext)
        elif file + ext not in files and owerwrite == False:
            urlopener.retrieve(url + i + ext, file + ext)
            print("Download complete: " + file + ext)
        elif owerwrite == True:
            urlopener.retrieve(url + i + ext, file + ext)
            print("Already exist (overwrite): " + file + ext)


for i in items:
    item = i["href"].replace("/hdri/?h=", "")

    # preview image files
    hdr_file = "https://hdrihaven.com/files/hdris/" + item + "_"
    thumb_file = "https://hdrihaven.com/files/hdri_images/thumbnails/" + item + ".jpg"
    preview_file = (
        "https://hdrihaven.com/files/hdri_images/tonemapped/1500/" + item + ".jpg"
    )
    spheres_file = "https://hdrihaven.com/files/hdri_images/spheres/" + item + ".jpg"
    if down_thumbnail == True and item + "_thumbnail.jpg" not in files:
        urlopener.retrieve(thumb_file, item + "_thumbnail.jpg")
    if down_preview == True and item + "_preview.jpg" not in files:
        urlopener.retrieve(preview_file, item + "_preview.jpg")
    if down_spheres == True and item + "_spheres.jpg" not in files:
        urlopener.retrieve(spheres_file, item + "_spheres.jpg")

    # hdr file
    try:
        downloader(hdr_file, ".hdr", item)
    except:
        downloader(hdr_file, ".exr", item)
