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
    # create the instance of the Firebase to insert the new item
    my_db = config_firebase()

    # this function get the list from the server insert de new item
    # and save the complete list en the server.
    product_list = get_list_of_product()
    product_list.append(newItem)

    my_db.child("productsDb").set(product_list)
    return True


# class to show the graphic windows and interface
# ============================================================================
class InterfaceGui(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("apiTools.ui", self)

        self.setWindowTitle("Api Products Manager")

        # events to navigation on the different form (insert, edit, delete)
        self.insert_btn.clicked.connect(lambda: self.pages_options.setCurrentIndex(0))
        self.edit_btn.clicked.connect(lambda: self.pages_options.setCurrentIndex(1))
        self.delete_btn.clicked.connect(lambda: self.pages_options.setCurrentIndex(2))

        # event to the creation of the new product
        self.button_create_product.clicked.connect(self.form_insert_product)

        # set the default options
        self.available_option_true.setChecked(True)
        self.disable_option_false.setChecked(True)
        self.season_option_false.setChecked(True)

    def form_insert_product(self):
        # Text Field
        product_name = self.editText_product_name.text()
        product_origen = self.editText_product_origen.text()
        price = self.editText_price.text()
        discount = self.editText_discount.text()
        moq = self.editText_moq.text()
        description = self.editText_description.text()

        # Combo Box
        category = self.comboBox_category.currentText()
        sales_unit = self.comboBox_sales_unit.currentText()

        # Group Box
        available = self.available_option_true.isChecked()
        disable = self.disable_option_true.isChecked()
        season_product = self.season_option_true.isChecked()

        # Image
        image = self.editText_image_location.text()

        # check field information
        if product_name != "" and \
                product_origen != "" and \
                price != "" and \
                discount != "" and \
                moq != "" and \
                image != "" and \
                not (category == "Select category") and \
                not (sales_unit == "Select option"):

            # if all fields are full we insert the new product
            new_product = create_new_product(
                nameProduct=product_name,
                productOrigin=product_origen,
                price=price,
                discount=discount,
                moq=moq,
                productDetails=description,
                categoryProduct=category,
                salesUnit=sales_unit,
                isAvailable=available,
                isDisable=disable,
                inSeason=season_product,
                imageProduct=image
            )
            if insert_new_product(new_product):
                print("The operation successful!!")
                self.clean_form()
            else:
                print("The operation failed..")
        else:
            print("some fields are empty")

    def clean_form(self):
        self.editText_product_name.setText("")
        self.editText_product_origen.setText("")
        self.editText_price.setText("")
        self.editText_discount.setText("")
        self.editText_moq.setText("")
        self.editText_description.setText("")
        self.editText_image_location.setText("")


# function main
# ============================================================================
if __name__ == '__main__':
    screen = QApplication(sys.argv)
    GUI = InterfaceGui()
    GUI.show()
    sys.exit(screen.exec())
