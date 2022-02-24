from PIL import Image, ImageDraw, ImageOps
import random
import numpy as np
import math
import itertools

## Parameters

size = 2400
centers = 400
color_lst = ['#cd5c5c', '#6a5acd', '#bc8f8f', '#708090', '#2f4f4f', '#b0c4de', '#a9a9a9', '#f5f5dc']
background = color_lst[-1]

image = Image.new(mode = "RGB", size= (size, size), color= background)
draw = ImageDraw.Draw(image)

n = int(math.sqrt(centers))
d = size // n 

def get_centers(size, centers):
    """ Returns the coordinates (as tuple) of the center of each square, given the size of the image
    and the number of squares desired"""
    n = int(math.sqrt(centers))
    d = size // n 
    c = [i * d + d/2 for i in range(n)] 
    y = [[(x,y) for x in c] for y in c]
    flat_list = list(itertools.chain(*y))
    return flat_list

def get_cordiates(points):
    """ Returns each point of the individual square, given its center and the length of 
    the sides"""
    p4 = (points[0] - (d // 2) , points[1] + (d // 2))
    p3 = (points[0] + (d // 2) , points[1] + (d // 2))
    p2 = (points[0] + (d // 2) , points[1] - (d // 2))
    p1 = (points[0] - (d // 2) , points[1] - (d // 2))
    return p1, p2, p3, p4

def get_random_polynomial(p1, p2, p3, p4):
    """ Create a random polygon with each point in a different quadrant in the 
    hyothetical cartesian plane"""
    x_mid = (p1[0] + p2[0]) // 2
    y_mid = (p1[1] + p4[1]) // 2
    updated_p1 = (random.randint(p1[0] , x_mid) , random.randint(p1[1] , y_mid))
    updated_p2 = (random.randint(x_mid , p2[0]) , random.randint(p2[1] , y_mid))
    updated_p3 = (random.randint(x_mid , p3[0]) , random.randint(y_mid , p3[1]))
    updated_p4 = (random.randint(p4[0] , x_mid) , random.randint(y_mid , p4[1]))
    return updated_p1, updated_p2, updated_p3, updated_p4

def get_split_lst(lst):
    """ Split list into 20 equal parts"""
    chunked_lst = []
    for i in range(0, len(lst), math.ceil((len(lst) / 20))):
        chunked_lst.append(lst[i : i + math.ceil((len(lst) / 20))])
    return chunked_lst

def get_color_prob(x):
    """ Return a color based off the given probability distribution"""
    diction = {
        1: .05, 2: .1, 3: .15, 4: .2, 5: .25, 6: .3, 7: .35, 8: .4, 9: .45, 10: .5,
        11: .55, 12: .6, 13: .65, 14: .7, 15: .75, 16: .8, 17: .85, 18: .9, 19: .95, 20: 1 
        }
    number = diction[x]
    other = (1 - number) / 7
    p_1_10 = np.random.choice(color_lst, 1, p = [other, other, other, other, other, other, other, number])
    color = p_1_10[0]
    return color

def get_antialias():
    """ Antialias the image"""
    new_img = ImageOps.expand(image, border=(int(size * .07), int(size * .07), int(size * .07), int(size * .07)), fill='#f5f5dc')
    im = new_img.resize((1920 // 2, 1920 // 2), resample=Image.ANTIALIAS)
    return im

def create_image():
    """ Creates the image"""
    lst = get_centers(size, centers)
    output = get_split_lst(lst)
    num_loop = 1
    for x in output:
        for i in x:
            color = get_color_prob(num_loop)
            p1, p2, p3, p4 = get_cordiates(i)
            width = random.randint(1, 3)
            for _ in range(10):
                p1_n, p2_n, p3_n, p4_n = get_random_polynomial(p1, p2, p3, p4)
                draw.line([p1_n, p2_n, p3_n, p4_n, p1_n], width = width, fill = color)
        num_loop += 1

def main():
    create_image()
    picture = get_antialias()
    picture.show()

if __name__ == "__main__":
    main()

