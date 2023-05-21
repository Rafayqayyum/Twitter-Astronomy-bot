# import requests and oAuth2
import requests
import datetime
import random
import os
from PIL import Image
NASA_API_KEY = os.environ.get('NASA_API_KEY')


# function to generate a random date between 2010-01-01 and current date
def get_random_date():
    # get current date
    current_date = datetime.datetime.now()
    # get a random date between 2010-01-01 and current date dynamically
    random_date = datetime.datetime(random.randint(2010, current_date.year), random.randint(1, 12), random.randint(1, 28))
    # return the random date
    return random_date

# function to get a random picture of the day of random dates
def get_picture_of_the_day(date):
    response = requests.get('https://api.nasa.gov/planetary/apod?api_key=' + NASA_API_KEY + '&date=' + date.strftime('%Y-%m-%d')).json()
    # return the picture of the day
    return response.get('title'),response.get('explanation'),response.get('url'),response.get('hdurl'),response.get('media_type')

# function to compare the hdimage against twitter image size and resolution limit
# and resize the image if it exceeds the limit
def compare_and_reshape(filename_hd, filename):
    # get the image size and resolution
    image_size = os.path.getsize(filename_hd)
    image_resolution = Image.open(filename_hd).size
    # compare the resolution and size against the limit if exceeds use filename instead of filename_hd
    if image_resolution[0] > 4096 or image_resolution[1] > 4096 or image_size>5242880:
        return filename
    else:
        return filename_hd


# function to get a random picture of the day of random dates
def get_random_picture_of_the_day():
    # get a random date
    random_date = get_random_date()
    # get the picture of the day for the random date
    title, explanation,url,hdurl,media = get_picture_of_the_day(random_date)
    while media!='image' or url==None or url=='':
        random_date = get_random_date()
        title, explanation,url,hdurl,media = get_picture_of_the_day(random_date)
    # download the picture of the day
    # get image
    response = requests.get(url)
    # save the picture of the day
    filename='picture_of_the_day.jpg'
    with open(filename, 'wb') as f:
        f.write(response.content)
    # get hd image
    response = requests.get(hdurl)
    # save the picture of the day
    filename_hd='picture_of_the_day_hd.jpg'
    with open(filename_hd, 'wb') as f:
        f.write(response.content)
        
    # compare and reshape the image
    filename=compare_and_reshape(filename_hd,filename)
    # return the picture of the day
    return title, explanation, filename,hdurl,random_date

if __name__ == '__main__':
    # get a random picture of the day
    title, explanation, filename,hdurl,random_date = get_random_picture_of_the_day()
    # print the picture of the day
    print(title)
    print(explanation)
    print(filename)
    print(hdurl)
    print(random_date)