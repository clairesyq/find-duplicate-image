import os
import json
import socket
import logging
import shutil
import urllib.request
from pathlib import Path
from urllib.error import HTTPError
from imagededup.methods import PHash

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Chrome/23.0.1271.64'}
phasher = PHash()


def getUrl(str, lst):
    idx = str[:str.index('.')]
    url = lst[int(idx)]
    return url


# returns a 2-D array of duplicated images
def detect(picStr):
    final_result_dict = []
    if picStr is None:
        return final_result_dict

    web_dict = json.loads(picStr)
    image_folder = web_dict['_id']

    try:
        dirpath = Path(image_folder)
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        os.makedirs(image_folder)

        image_urls = web_dict['_source']['pictures']
        for i in range(len(image_urls)):
            this_url = image_urls[i]
            req = urllib.request.Request(url=this_url)

            resource = urllib.request.urlopen(req, timeout=5)
            output = open(image_folder + '/' + str(i) + '.jpg', 'wb')
            output.write(resource.read())
            output.close()

        encodings = phasher.encode_images(image_dir=image_folder)
        duplicates = phasher.find_duplicates(encoding_map=encodings)
        print(duplicates)

        # add duplicates to result_dict
        result_dict = {'dupPics': []}
        for key in duplicates:
            if key not in result_dict['dupPics']:
                values = duplicates[key]
                result_dict['dupPics'].extend(values)
        for key in duplicates:
            if key not in result_dict['dupPics'] and duplicates[key]:
                result_dict[key] = duplicates[key]
        result_dict.pop('dupPics')

        # retrieve original url of image and convert return type to a 2-D array
        row = 0
        for key, value in result_dict.items():
            list = []
            new_key = getUrl(key, image_urls)
            print(row)
            list.append(new_key)
            for elt in value:
                new_elt = getUrl(elt, image_urls)
                list.append(new_elt)
            final_result_dict.append(list)
            row += 1

    # catch errors
    except socket.timeout:
        logging.error(' image download timeout error')
    except HTTPError:
        logging.error(' HTTPError 403: Forbidden')
    except ValueError:
        logging.error(' WARNING: Invalid image file')
    except:
        logging.error(' Other Exceptions')

    # delete the image folder
    shutil.rmtree(image_folder)

    return final_result_dict
