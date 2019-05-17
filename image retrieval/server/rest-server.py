#!flask/bin/python
################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #
#-------------------------------------------------------------------------------------------------------------------------------
################################################################################################################################
from flask import Flask, jsonify, abort, request, make_response, url_for,redirect, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import re
import shutil
import numpy as np
from search import recommend
import tarfile
from datetime import datetime
from scipy import ndimage
from scipy.misc import imsave
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
from tensorflow.python.platform import gfile
app = Flask(__name__, static_url_path = "")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

#==============================================================================================================================
#
# Loading the extracted feature vectors for image retrieval
#
#==============================================================================================================================
extracted_features=np.zeros((10000, 2048), dtype=np.float32)
with open('saved_features_recom.txt') as f:
    for i, line in enumerate(f):
        extracted_features[i, :]=line.split()
print("loaded extracted_features")

# This function is used to do the image search/image retrieval
@app.route('/imgUpload', methods=['GET', 'POST'])  # /imgUpload matches the url in ajax
def upload_img():
    print("image upload")
    result = 'static/result'
    if not gfile.Exists(result):  # If there is no result folder, create it
        os.mkdir(result)
    shutil.rmtree(result)  # Empty the result folder

    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)

        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file:  # and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            recommend(inputloc, extracted_features)
            os.remove(inputloc)
            image_path = "/result"
            image_list = [os.path.join(image_path, file) for file in os.listdir(result)
                          if not file.startswith('.')]
            images = {
                'image0': image_list[0],
                'image1': image_list[1],
                'image2': image_list[2],
                'image3': image_list[3],
                'image4': image_list[4],
                'image5': image_list[5],
                'image6': image_list[6],
                'image7': image_list[7],
                'image8': image_list[8]
            }
            return jsonify(images)

# This function is tag
@app.route('/tag', methods=['GET', 'POST'])
def tag():
    print("tag")
    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
    # Create a file to read the stream object and read each tag file
    animalsfile_object = open('database/tags/animals.txt')
    babyfile_object = open('database/tags/baby.txt')
    birdfile_object = open('database/tags/bird.txt')
    carfile_object = open('database/tags/car.txt')
    dogfile_object = open('database/tags/dog.txt')
    femalefile_object = open('database/tags/female.txt')
    flowerfile_object = open('database/tags/flower.txt')
    foodfile_object = open('database/tags/food.txt')
    indoorfile_object = open('database/tags/indoor.txt')
    lakefile_object = open('database/tags/lake.txt')
    malefile_object = open('database/tags/male.txt')
    nightfile_object = open('database/tags/night.txt')
    peoplefile_object = open('database/tags/people.txt')
    plant_lifefile_object = open('database/tags/plant_life.txt')
    portraitfile_object = open('database/tags/portrait.txt')
    riverfile_object = open('database/tags/river.txt')
    seafile_object = open('database/tags/sea.txt')
    skyfile_object = open('database/tags/sky.txt')
    structuresfile_object = open('database/tags/structures.txt')
    sunsetfile_object = open('database/tags/sunset.txt')
    transportfile_object = open('database/tags/transport.txt')
    treefile_object = open('database/tags/tree.txt')
    waterfile_object = open('database/tags/water.txt')
    try:
        # Read the contents of each tag file and store it as a string
        animalsfile_context = animalsfile_object.read()
        babyfile_context = babyfile_object.read()
        birdfile_context = birdfile_object.read()
        carfile_context = carfile_object.read()
        dogfile_context = dogfile_object.read()
        femalefile_context = femalefile_object.read()
        flowerfile_context = flowerfile_object.read()
        foodfile_context = foodfile_object.read()
        indoorfile_context = indoorfile_object.read()
        lakefile_context = lakefile_object.read()
        malefile_context = malefile_object.read()
        nightfile_context = nightfile_object.read()
        peoplefile_context = peoplefile_object.read()
        plant_liftfile_context = plant_lifefile_object.read()
        portraitfile_context = portraitfile_object.read()
        riverfile_context = riverfile_object.read()
        seafile_context = seafile_object.read()
        skyfile_context = skyfile_object.read()
        structuresfile_context = structuresfile_object.read()
        sunsetfile_context = sunsetfile_object.read()
        transportfile_context = transportfile_object.read()
        treefile_context = treefile_object.read()
        waterfile_context = waterfile_object.read()
    finally:
        # Close file
        animalsfile_object.close()
        babyfile_object.close()
        birdfile_object.close()
        carfile_object.close()
        dogfile_object.close()
        femalefile_object.close()
        flowerfile_object.close()
        foodfile_object.close()
        indoorfile_object.close()
        lakefile_object.close()
        malefile_object.close()
        nightfile_object.close()
        peoplefile_object.close()
        plant_lifefile_object.close()
        portraitfile_object.close()
        riverfile_object.close()
        seafile_object.close()
        skyfile_object.close()
        structuresfile_object.close()
        sunsetfile_object.close()
        transportfile_object.close()
        treefile_object.close()
        waterfile_object.close()

    image_path = "/result"
    # Read each image file in the result folder
    image_list = [os.path.join(image_path, file) for file in os.listdir('static/result')
                  if not file.startswith('.')]
    for i in range(0, 9):
        image_list[i] = ('\n'+str(re.findall("\d+", image_list[i])[0])+'\n')  # image_list存储每个图片文件的序号

    # image_tag stores the tag of each image file
    image_tag =[]
    for i in range(0, 9):  # Determine which tag each image belongs to
        if image_list[i] in animalsfile_context:
            image_tag.append('animals')
        elif image_list[i] in babyfile_context:
            image_tag.append('baby')
        elif image_list[i] in birdfile_context:
            image_tag.append('bird')
        elif image_list[i] in carfile_context:
            image_tag.append('car')
        elif image_list[i] in dogfile_context:
            image_tag.append('dog')
        elif image_list[i] in femalefile_context:
            image_tag.append('female')
        elif image_list[i] in flowerfile_context:
            image_tag.append('flower')
        elif image_list[i] in foodfile_context:
            image_tag.append('food')
        elif image_list[i] in indoorfile_context:
            image_tag.append('indoor')
        elif image_list[i] in lakefile_context:
            image_tag.append('lake')
        elif image_list[i] in malefile_context:
            image_tag.append('male')
        elif image_list[i] in nightfile_context:
            image_tag.append('night')
        elif image_list[i] in peoplefile_context:
            image_tag.append('people')
        elif image_list[i] in plant_liftfile_context:
            image_tag.append('plant_life')
        elif image_list[i] in portraitfile_context:
            image_tag.append('portrait')
        elif image_list[i] in riverfile_context:
            image_tag.append('river')
        elif image_list[i] in seafile_context:
            image_tag.append('sea')
        elif image_list[i] in skyfile_context:
            image_tag.append('sky')
        elif image_list[i] in structuresfile_context:
            image_tag.append('structures')
        elif image_list[i] in sunsetfile_context:
            image_tag.append('sunset')
        elif image_list[i] in transportfile_context:
            image_tag.append('transport')
        elif image_list[i] in treefile_context:
            image_tag.append('tree')
        elif image_list[i] in waterfile_context:
            image_tag.append('water')

    images = {
        'image0': image_tag[0],
        'image1': image_tag[1],
        'image2': image_tag[2],
        'image3': image_tag[3],
        'image4': image_tag[4],
        'image5': image_tag[5],
        'image6': image_tag[6],
        'image7': image_tag[7],
        'image8': image_tag[8]
    }
    print(images)
    return jsonify(images)

# This function is addFavorite
@app.route('/addFavorite', methods=['GET', 'POST'])
def addFavorite():
    print("addFavorite")
    favorite = 'static/favorite'
    if not gfile.Exists(favorite):  # if favorite is not existing
        os.mkdir(favorite)  # Create a new folder

    if request.method == 'POST' or request.method == 'GET':
        print(request.method)

    # checkedData stores the received data, which is the file name of the selected pictures
    checkedData = request.get_json()
    print(checkedData)
    imgname = []  # imgname Save the path of the selected images
    for i in range(0, len(checkedData['checkedData'])):
        imgname.append('static/result/'+str(checkedData['checkedData'][i]))  # Get the path of the selected images
        print(imgname[i])
        shutil.copy(imgname[i], "static/favorite")  # Copy the picture under the path to the favorite folder
    return jsonify(checkedData)

# This function is displaying favorites
@app.route('/favorite', methods=['GET', 'POST'])
def favorite():
    print('favorite')
    image_list = []  # image_list store all image names under the favorite folder
    for filename in os.listdir(r"static/favorite"):  # listdir's parameter is the path of the folder
        image_list.append(filename)
        print(filename)  # The filename is the name of the files in the favorite folder.

    images = {}
    for i in range(0, len(image_list)):
        images['image'+str(i)] = image_list[i]
    return jsonify(image_list)

# This function is deleting favorites
@app.route('/deleteFavorite', methods=['GET', 'POST'])
def deleteFavorite():
    print("deleteFavorite")
    favorite = 'static/favorite'
    if not gfile.Exists(favorite):  # if favorite is not existing
        os.mkdir(favorite)  # Create a new folder

    if request.method == 'POST' or request.method == 'GET':
        print(request.method)

    # checkedData stores the received data, which is the file name of the selected pictures
    checkedData = request.get_json()
    print(checkedData)
    imgname = []  # imgname saves the path of the selected images
    for i in range(0, len(checkedData['checkedData'])):
        imgname.append('static/favorite/'+str(checkedData['checkedData'][i]))  # Get the path of the selected images
        print(imgname[i]+'has been deleted')
        os.remove(imgname[i])  # Remove the picture from the path from the favorite folder
    return jsonify(checkedData)

# Main function
@app.route("/")
def main():
    return render_template("main.html")

if __name__ == '__main__':
    app.run(debug = True, host= '0.0.0.0')
