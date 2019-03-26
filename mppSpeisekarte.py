#!/bin/bash python

'''
    mppSpeisekarte
    --------------
    Package to extract the menu of the day for the MPP menu.

    Author: Hendrik Windel
    Mail: hwindel@mpp.mpg.de
    Date : 2019/03/26
    License: GNU General Public License v3.0
'''


from pdf2image import convert_from_path
import pytesseract

# These values are unique values for the box sizes which define the day and meals
# for the Speisekarte of the MPI for Physics.
# If you want to change, convert the pdf to a picture and open it with GIMP.
# The coordinates are the same the python uses.
box_lx = 0.800 # 1870 px
box_ly = 0.516 # 854 px

box_x = 0.1283 # 300px
box_y = 0.2305 # 380 px
box_w = 0.1666 # 390px
box_h = 0.0963 # 158 px

def crop(image, box, save=False, **kwgs):
    '''
        Crops an image with size and position of you defined box.

        Parameters
        ----------
        image : PIL.Image.Image
            Python image variable of your menu.

        box : Tuple
            Tuple  with the size and position of the box you want
            as the new image in percentage (no pixels) of the original image.
            E.g. box=(x, y, width, height)=(0.12, 0.23, 0.16, 0.9). x and y
            are the top left corner of your box.

        save : Bool
            If save is true, the image is saved as 'crop.png' in the working directory.

        Returns
        -------
        PIL.Image.Image
            Returns a image of size and position given by box.
    '''
    w, h = image.size
    x = int(box[0]*w)
    y = int(box[1]*h)
    cropped_w = int(box[2]*w)
    cropped_h = int(box[3]*h)
    cropped = image.crop((x,y,x+cropped_w, y+cropped_h))
    if save:
        cropped.save("crop.png", "png")

    return cropped



def getMeals(pathToPDF, day, **kwgs):
    '''
        Returns the meal of the given day for the MPP Menu.

        Parameters
        ----------
        pathToPDF : string
            Path to your menu as a PDF file.

        day : string
            The day you want the menu for.
            Day needs to be given in German:
            Montag, Dienstag, Mittwoch, Donnerstag, Freitag

        Returns
        -------
        dict
            Returns a dict with the meals of the day:
            Brotzeit, MenuI, MenuII


    '''
    image = convert_from_path(pathToPDF)[0]

    try:
        day = day.lower()
    except AttributeError as err:
        print('Error: The day must be a string!')
        return -1

    days = {'montag' : 0, 'dienstag' : 1, 'mittwoch' : 2, 'donnerstag' : 3, 'freitag' : 4}
    meals = {   'Datum' : '',
                'Brotzeit' : '',
                'MenuI' : '',
                'MenuII' : ''}
    for i,meal in zip(range(0,4),meals):
        essen = crop(image,(box_x+days[day]*box_w, box_y+i*box_h, box_w, box_h))
        meals[meal] = pytesseract.image_to_string(essen, lang="deu")

    return meals


if __name__ == '__main__':
    pass
