from pyvisionproductsearch import ProductSearch, ProductCategories
from google.cloud import storage, vision
from google.cloud.vision import types

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import pandas as pd
from utils import detectLabels, detectObjects
import io
from tqdm import tqdm # Not using jupyter notebook so I removed the .notebook (and it was causing an error)

import os
from dotenv import load_dotenv

load_dotenv()

ps = ProductSearch(os.getenv("PROJECTID"), os.getenv("CREDS"), os.getenv("BUCKET"))
productSet = ps.getProductSet(os.getenv("PRODUCT_SET"))

# For each fashion inspiration pic, check to make sure that it's
# a "fashion" picture. Ignore all other pics
storage_client = storage.Client()
blobs = list(storage_client.list_blobs(os.getenv("INSPO_BUCKET"), prefix=os.getenv("INSPO_SUBFOLDER")))
uris = ["gs://" + blobs[0].bucket.name + "/" + x.name
        for x in blobs if ('.jpg' in x.name or '.png' in x.name)]

# This format of "[... for ... in ... if ...]" is called a Python list comprehension. It is the same thing as saying:
# for (x in blobs):
#     if ('.jpg' in x.name or '.png' in x.name):
#         uri.append("gs://" + blobs[0].bucket.name + "/" + x.name)
urls = [x.public_url for x in blobs if ('.jpg' in x.name or '.png' in x.name)]

fashionPics = []
fashionWords = ["Fashion", "Shoe", "High Heel", "Boot", "Outerwear", "T-shirt", "Footwear", "Jeans", "Pants", "Shorts", "Clothing", "Clothes", "Dress", "Jewelry", "Earrings", "Earring", "Rings", "Ring", "Necklace", "Necklaces", "Style", "Outfit"]
for uri, url in tqdm(list(zip(uris, urls))):
    # Such a simple way to pull labels from an image with Google Vision!
    labels = detectLabels(image_uri=uri)
    # We don't want any bad data. If the AI can't even tell that the inspiration pic is fashion then we don't want to include it in the set
    if any([x.description in fashionWords for x in labels]):
        fashionPics.append((uri, url))
# Select a cell using: fashion_pics['column label'].iloc[row index]
fashion_pics = pd.DataFrame(fashionPics, columns=["uri", "url"])

# We want to recommend items that are similar and of the same type as in the inspiration picture.
# For example, the Product Search API might return a dress as a match for a shirt.
# getBestMatch sorts through the results returned by the API and makes sure that
    # 1. the match with the highest confidence is returned.
    # 2. the item types match (the match in our closet and the match in the inspiration should have the same type)

# The API sometimes uses different names for similar items, so this
# function tells you whether two labels are roughly equivalent
def isTypeMatch(label1, label2):
    # everything in a single match group are more or less synonymous
    matchGroups = [
        ("skirt", "miniskirt"),
        ("jeans", "pants"),
        ("shorts"),
        ("jacket", "vest", "outerwear", "coat", "suit"),
        ("top", "shirt"),
        ("dress"),
        ("swimwear", "underpants"),
        ("footwear", "sandal", "boot", "high heels"),
        ("handbag", "suitcase", "satchel", "backpack", "briefcase"),
        ("sunglasses", "glasses"),
        ("bracelet"),
        ("scarf", "bowtie", "tie"),
        ("earrings"),
        ("necklace"),
        ("sock"),
        ("hat", "cowboy hat", "straw hat", "fedora", "sun hat", "sombrero")]
    for group in matchGroups:
        if label1.lower() in group and label2.lower() in group:
            return True
    return False

# This returns a set of matches for each item identified in the inspiration photo (selected with .iloc[0]).
# For each item, a bounding box is returned that indicates where the item is in the picture.
    # RETURN: For each matched item in your closet, a Product object is returned along with its image id and a confidence score.
    # INPUT: Takes in one match of the response (not the response itself, just one of matches at a time)
def getBestMatch(searchResponse):
    label = searchResponse['label']
    matches = searchResponse['matches']
    viableMatches = [match for match in matches if any([isTypeMatch(label, match['product'].labels['type'])])]
    # If there are any viable matches return them. Otherwise return None
    return max(viableMatches, key= lambda x: x['score']) if len(viableMatches) else None

# Test the functions by seeing fetching the first matched outfit
# fashion_pics['uri'].iloc[0] selects the cell in row 0 in the column 'uri' from the fashion_pics dataframe.
response = productSet.search("apparel", image_uri = fashion_pics['uri'].iloc[0])
# print(fashion_pics) # Prints the dataframe as a table so you can see what inspo pics made it through the purge

def canAddItem(existingArray, newType):
    bottoms = {"pants", "skirt", "shorts", "dress"}
    newType = newType.lower()
    # Don't add the same item type twice
    if newType in existingArray:
        return False
    if newType == "shoe":
        return True
    # Only add one type of bottom (pants, skirt, etc)
    # I want to modify this so leggings can be their own category and worn with skirts/dresses.
    if newType in bottoms and len(bottoms.intersection(existingArray)):
        return False
    # You can't wear both a top and a dress
    if newType == "top" and "dress" in existingArray:
        return False
    return True

# A couple of options for deciding which of the matches give the best outfit

# Option 1: sum up the confidence scores for each closet item matched to the inspo photo
def scoreOutfit1(matches):
    if not matches:
        return 0
    return sum([match['score'] for match in matches]) / len(matches)

# Option 2: Sum up the confidence scores only of items that matched with the inspo photo
# with confidence > 0.3. Also, because shoes will match most images _twice_
# (because people have two feet), only count the shoe confidence score once
# I can't get the second algorithm to work because x["label"] does not exist. It should be going to x["product"]["label"] however that is not possible because x["product"] isn't an interactive object :(
# Deal with this in the future
# OH I wonder if you have to import Product from pyvisionproductsearch. Definitely come back to try that, it would be good to know if that's the issue
# def scoreOutfit2(matches):
#     if not len(matches):
#         return 0
#     for x in matches:
#         print("See if label is here: ", x["product"])
#     noShoeSum = sum([x['score'] for x in matches if (x['score'] > 0.3 and not isTypeMatch("shoe", x["product"]["label"]))])
#     shoeScore = 0
#     try:
#         shoeScore = max([x['score'] for x in matches if isTypeMatch("shoe", x["product"]["label"])])
#     except:
#         pass
#     return noShoeSum + shoeScore * 0.5 # half the weight for shoes

# Final function to put all the helpers together. This is the main one we will interface with.
def getOutfit(imgUri, verbose=False):
    # 1. Search for matching items
    response = productSet.search("apparel", image_uri=imgUri)
    if verbose:
        print("Found matching " + ", ".join([x['label'] for x in response]) + " in closet.")

    clothes = []
    # 2. For each item in the inspo pic, find the best match in our closet and add it to the outfit array
    for item in response:
        bestMatch = getBestMatch(item)
        if not bestMatch:
            if verbose:
                print(f"No good match found for {item['label']}")
            continue
        if verbose:
            print(f"Best match for {item['label']} was {bestMatch['product'].displayName}")
        clothes.append(bestMatch)

    # 3. Sort the items by highest confidence score first
    clothes.sort(key=lambda x: x['score'], reverse=True)

    # 4. Add as many items as possible to the outfit while still
    # maintaining a logical outfit
    outfit = []
    addedTypes = []
    for item in clothes:
        itemType = item['product'].labels['type'] # i.e. shorts, top, etc
        if canAddItem(addedTypes, itemType):
            addedTypes.append(itemType)
            outfit.append(item)
            if verbose:
                print(f"Added a {itemType} to the outfit")

    # 5. Now that we have a whole outfit, compute its score!
    score = scoreOutfit1(outfit)
    if verbose:
        print("Algorithm score: %0.3f" % score)
    return (outfit, score)

# print(getOutfit(fashion_pics.iloc[0]['uri'], verbose=True))


app = firebase_admin.initialize_app(credentials.Certificate(os.getenv("CREDS")))
db = firestore.client()
userid = os.getenv("userid")
thisUser = db.collection('users').document(userid)

outfits = thisUser.collection('outfitsDEMO')
# outfits = outfitsRef.get()

# if (outfits.exists):
#     print("OutfitsDEMO Exists")

# Go through all of the inspo pics and compute matches.
for row in fashion_pics.iterrows():
    srcUrl = row[1]['url']
    srcUri = row[1]['uri']
    (outfit, score1) = getOutfit(srcUri, verbose=False)

    # Construct a name for the source image--a key we can use to store it in the database
    srcId = srcUri[len("gs://"):].replace("/","-")

    # Firestore writes json to the database, so let's construct an object and fill it with data
    fsMatch = {
        "srcUrl": srcUrl,
        "srcUri": srcUri,
        "score1": score1,
    }
    # Go through all of the outfit matches and put them into json that can be
    # written to firestore
    theseMatches = []
    for match in outfit:
        image = match['image']
        imgName = match['image'].split('/')[-1]
        name = match['image'].split('/')[-3]
        # The storage api makes these images publicly accessible through url
        imageUrl = f"https://storage.googleapis.com/{os.getenv('BUCKET')}/" + imgName
        label = match['product'].labels['type']
        score = match['score']

        theseMatches.append({
            "score": score,
            "image": image,
            "imageUrl": imageUrl,
            "label": label
        })
    fsMatch["matches"] = theseMatches
    # Add the outfit to firestore!
    outfits.document(srcId).set(fsMatch)
