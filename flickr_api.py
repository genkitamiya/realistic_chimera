# FlickrAPI
import os

import time
import traceback

import flickrapi
from urllib.request import urlretrieve

import sys
from retry import retry

flickr_api_key = "97fc5aab09f8b76262f320930acec14c"
secret_key = "86352b2178654a5e"

keyword = sys.argv[1]


@retry()
def get_photos(url, filepath):
    urlretrieve(url, filepath)
    time.sleep(1)


if __name__ == '__main__':

    flicker = flickrapi.FlickrAPI(flickr_api_key, secret_key, format='parsed-json')
    response = flicker.photos.search(
        text=keyword,
        per_page=300,
        media='photos',
        sort='relevance',
        safe_search=1,
        extras='url_q,license'
    )
    photos = response['photos']

    try:
        if not os.path.exists('./flickr_images/' + keyword):
            os.mkdir('./flickr_images/' + keyword)

        for photo in photos['photo']:
            url = photo['url_q']
            filepath = './flickr_images/' + keyword + '/' + photo['id'] + '.jpg'
            get_photos(url, filepath)

    except Exception as e:
        traceback.print_exc()
