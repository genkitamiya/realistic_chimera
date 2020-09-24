import argparse
import cv2
import numpy as np
import os
import glob


def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged


def resize_to_square(im, size):
    desired_size = size
    old_size = im.shape[:2]  # old_size is in (height, width) format

    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])

    # new_size should be in (width, height) format

    im = cv2.resize(im, (new_size[1], new_size[0]))

    delta_w = desired_size - new_size[1]
    delta_h = desired_size - new_size[0]
    top, bottom = delta_h//2, delta_h-(delta_h//2)
    left, right = delta_w//2, delta_w-(delta_w//2)

    color = [255, 255, 255]
    new_im = cv2.copyMakeBorder(
        im, top, bottom, left, right, cv2.BORDER_REPLICATE, value=color)

    return new_im


def combine_A_B(src, dest, size):
    ls = [0]
    for f in os.listdir(dest):
        for w in f.split('.'):
            try:
                ls.append(int(w))
            except:
                pass

    count = max(ls)+1

    X = []
    y = []

    for f in os.listdir(src):
        if '.jpg' in f:
            img = cv2.imread(os.path.join(src, f))
            img = resize_to_square(img, size)
            X.append(img)
            # make edges image
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            edges = auto_canny(blurred)  # auto
    #             edges = cv2.Canny(blurred, 10, 200) #wide
    #             edges = cv2.Canny(blurred, 225, 250) #tight
    #             edges = cv2.Canny(blurred, 100, 250) #custom
            edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

            y.append(edges)

    X = np.array(X)
    y = np.array(y)

    dataset = np.concatenate((X, y), axis=2)

    for i, f in enumerate(dataset):
        cv2.imwrite(os.path.join(dest, '{}.jpg'.format(count+i)), f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    """
    コマンドライン引数
    """
    parser.add_argument(
        '-i', '--input',
        help='source directory'
    )

    parser.add_argument(
        '-o', '--output',
        help='output directory'
    )

    parser.add_argument(
        '-s', '--size', type=int, default=256,
        help='output image size (default=256)'
    )

    FLAGS = parser.parse_args()

    combine_A_B(FLAGS.input, FLAGS.output, FLAGS.size)
