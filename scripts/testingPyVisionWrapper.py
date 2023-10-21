# import the wrapper library made by Dale to work with the vision API.
from pyvisionproductsearch import ProductSearch, ProductCategories
import os
# import the load_dotenv function to load in the environment variables
from dotenv import load_dotenv
from collections import Counter

load_dotenv()

ps = ProductSearch(os.getenv("PROJECTID"), os.getenv("CREDS"), os.getenv("BUCKET"))

try:
    productSet = ps.getProductSet(os.getenv("PRODUCT_SET"))
except:
    productSet = ps.createProductSet(os.getenv("PRODUCT_SET"))

try:
    blackCrop = ps.getProduct("black_crop_shirt") # productID doesn't have any slashes
except Exception as error:
    print(error);

def deleteWardrobe():
    # Delete entire wardrobe
    # loop through folder of folders and delete the products based on the folder names
    for folder in os.listdir(os.getenv("CLOSET_DIR")):
        # folder is just the name with no slashes in it. We want this because we set it up so that the folder name is the productID.
        currentItem = ps.getProduct(folder)
        print(f"Deleting {folder} Product from Google")
        try:
            currentItem.delete()
        except Exception as error:
            print(error);
    # TODO: Will need to also delete the images from Google Storage. But for now, I can do that by hand so its a future feature. I didn't have any gui for the Products though so I had to do it through code... Oh well, it helped me learn the inner workings better.

# Delete specific article of clothing
    # delete image from storage
    # delete product from product set

# print("deleting product set")
# productSet.delete()
# blackCrop.delete()
