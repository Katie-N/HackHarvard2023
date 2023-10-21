#  * Copyright 2020 Google LLC
#  *
#  * Licensed under the Apache License, Version 2.0 (the "License");
#  * you may not use this file except in compliance with the License.
#  * You may obtain a copy of the License at
#  *
#  *      http://www.apache.org/licenses/LICENSE-2.0
#  *
#  * Unless required by applicable law or agreed to in writing, software
#  * distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.

# import the wrapper library made by Dale to work with the vision API.
from pyvisionproductsearch import ProductSearch, ProductCategories
import os
# import the load_dotenv function to load in the environment variables
from dotenv import load_dotenv
from collections import Counter

# Imports the variables from env.txt
# This is how these variables get defined:
# PROJECTID
# BUCKET
# CREDS
# CLOSET_DIR
# PRODUCT_SET
load_dotenv()

ps = ProductSearch(os.getenv("PROJECTID"), os.getenv("CREDS"), os.getenv("BUCKET"))

def getLabel(fileName):
    # The label is just the last word in the filename
    return fileName.split("_")[-1].lower()
# define the productSet (which is the collection of the user's clothing items)
try:
    productSet = ps.getProductSet(os.getenv("PRODUCT_SET"))
except:
    productSet = ps.createProductSet(os.getenv("PRODUCT_SET"))

labels = []
# Loop through each subfolder (each article of clothing) in the user's closet
# This is what Dale calls "indexing" the closet
for folder in os.listdir(os.getenv("CLOSET_DIR")):

    # label is the last word in the folder name
    label = getLabel(folder)
    labels.append(label)

    print(f"Creating product {folder}")

    product = ps.createProduct(folder, "apparel", labels={"type": label})

    imgFolder = os.path.join(os.getenv("CLOSET_DIR"), folder)

    for img in os.listdir(imgFolder):
        try:
            product.addReferenceImage(os.path.join(imgFolder, img))
        except:
            print(f"Couldn't add reference image {imgFolder}/{img}")

    productSet.addProduct(product)
    print(f"Added product {product.displayName} to set")

numAdded = len(productSet.listProducts())
print(f"Added {numAdded} products to set")
print(Counter(labels))
