# Import of the app
import sys
import pyrebase
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox


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
    return firebase


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
    my_db = config_firebase().database()
    data = my_db.child("productsDb").get()
    return data.val()


# function to insert a new element on the array on the API
# ============================================================================
def insert_new_product(newItem):
    # create the instance of the Firebase to insert the new item
    my_db = config_firebase().database()

    # this function get the list from the server insert de new item
    # and save the complete list en the server.
    product_list = get_list_of_product()
    if product_list is not None:
        product_list.append(newItem)
    else:
        product_list = list()
        product_list.append(newItem)

    my_db.child("productsDb").set(product_list)
    return True


# function to get the file of the product
# ============================================================================
def get_file_image():
    return QFileDialog.getOpenFileName()[0]


# function to get the file of the product
# ============================================================================
def get_code_category(category):
    match category:
        case "Fruit":
            return 1
        case "Vegetables":
            return 2
        case "Fresh Herbs":
            return 3
        case "Dried Fruit & Nuts":
            return 4
        case "Others":
            return 5


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

        # event to set the image of the product
        self.button_load_image.clicked.connect(lambda: self.editText_image_location.setText(get_file_image()))

        # set the default options
        self.available_option_true.setChecked(True)
        self.disable_option_false.setChecked(True)
        self.season_option_false.setChecked(True)
        self.editText_image_location.setEnabled(False)

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

        if image != "":
            image_url = self.load_image()
            if image_url == "":
                self.show_dialog("error...", "There was an error loading the image     ")
            else:
                # check field information
                if product_name != "" and \
                        product_origen != "" and \
                        price != "" and \
                        discount != "" and \
                        moq != "" and \
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
                        categoryProduct=get_code_category(category),
                        salesUnit=sales_unit,
                        isAvailable=available,
                        isDisable=disable,
                        inSeason=season_product,
                        imageProduct=image_url
                    )
                    if insert_new_product(new_product):
                        self.clean_form()
                        self.show_dialog("Completed      ", "The operation successful!!      ")
                    else:
                        self.show_dialog("Error has occurred      ", "The operation failed..      ")
                else:
                    self.show_dialog("Information is missing      ", "Some fields are empty      ")
        else:
            self.show_dialog("image is missing      ", "Product image not selected      ")

    def load_image(self):
        store = config_firebase().storage()
        title_file = self.split_name(self.editText_image_location.text())
        result = store.child('imagenProduct/' + title_file).put(self.editText_image_location.text())

        return store.child('imagenProduct/' + title_file).get_url(result['downloadTokens'])

    def split_name(self, url):
        x = url.split("/")
        return x[len(x) - 1]

    def clean_form(self):
        self.editText_product_name.setText("")
        self.editText_product_origen.setText("")
        self.editText_price.setText("")
        self.editText_discount.setText("")
        self.editText_moq.setText("")
        self.editText_description.setText("")
        self.editText_image_location.setText("")

    def show_dialog(self, title, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(message)
        dlg.exec()


# function main
# ============================================================================
if __name__ == '__main__':
    screen = QApplication(sys.argv)
    GUI = InterfaceGui()
    GUI.show()
    sys.exit(screen.exec())
