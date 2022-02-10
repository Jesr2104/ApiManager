# Import of the app
import sys
import pyrebase
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


# function to configurate our service of database
# ============================================================================
def config_firebase():
    firebase_config = {
        "apiKey": "AIzaSyD38MhGW8-0NM4oRseY1xIrkI0Xj2-H464",
        "authDomain": "grocerystore-justjump.firebaseapp.com",
        "databaseURL": "https://grocerystore-justjump-default-rtdb.europe-west1.firebasedatabase.app",
        "projectId": "grocerystore-justjump",
        "storageBucket": "grocerystore-justjump.appspot.com",
        "messagingSenderId": "496229318920",
        "appId": "1:496229318920:web:98f64838f81f9744a32cbd"
    }
    firebase = pyrebase.initialize_app(firebase_config)
    return firebase.database()


# function to configurate our service of database
# ============================================================================
def create_new_product(moq, categoryProduct, discount, imageProduct,
                       inSeason, isAvailable, isDisable, nameProduct,
                       price, productDetails, productOrigin, salesUnit):
    database = {
        "MOQ": moq,
        "categoryProduct": categoryProduct,
        "discount": discount,
        "imageProduct": imageProduct,
        "inSeason": inSeason,
        "isAvailable": isAvailable,
        "isDisable": isDisable,
        "nameProduct": nameProduct,
        "price": price,
        "productDetails": productDetails,
        "productOrigin": productOrigin,
        "salesUnit": salesUnit
    }
    return database


# function to get the list of the product on the API
# ============================================================================
def get_list_of_product():
    my_db = config_firebase()
    data = my_db.child("productsDb").get()
    return data.val()


# function to insert a new element on the array on the API
# ============================================================================
def insert_new_product(newItem):
    my_db = config_firebase()
    product_list = get_list_of_product()
    product_list.append(newItem)

    my_db.child("productsDb").set(product_list)


class exampleGui(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ApiTools.ui", self)

        self.insert_btn.clicked.connect(
            lambda:
            print(get_list_of_product())
        )


# function main
# ============================================================================
if __name__ == '__main__':
    screen = QApplication(sys.argv)
    GUI = exampleGui()
    GUI.show()
    sys.exit(screen.exec())

    # Data information
    # newProduct = create_new_product(
    #     6, 1, 25,
    #     "gs://grocerystore-justjump.appspot.com/imagenProduct/fruit_red_apple.jpg",
    #     False, True, False, "Washington Apples - new 9", 3.50, "", "UK / France", "Unit",
    # )
    #
    # insert_new_product(newProduct)
