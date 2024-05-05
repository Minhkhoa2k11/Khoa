import json
from PyQt6.QtWidgets import QLineEdit,QFileDialog, QApplication, QMainWindow, QStackedWidget, QPushButton, QListWidget, QListWidgetItem, QLabel, QVBoxLayout, QWidget, QScrollArea, QDialog, QComboBox, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from PyQt6.QtCore import Qt
import re
class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui\login.ui", self)

    # Bắt sự kiện click chuột vào nút login
        self.pushButton.clicked.connect(self.check_login)
    #Bắt sự kiện click chuột vào nút sign up
        self.pushButton_2.clicked.connect(self.showRegister)

    def check_login(self):
        # Lấy thông tin email và mật khẩu từ người dùng
        email = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        
        # Kiểm tra email và mật khẩu có được nhập hay không
        if not email: 
            msg_box.setText("Please enter your email or phone number!")
            msg_box.exec()
            return
        if not password:
            msg_box.setText("Please enter a password!")
            msg_box.exec()
            return
    
    # Kiểm tra email và mật khẩu có khớp với tài khoản admin hay không
        if email == "admin@example.com" and password == "admin":
            # Nếu đăng nhập thành công, chuyển sang giao diện chính (Main)
            self.close()
            mainwindowPage.show()  
        else:
            # Nếu đăng nhập không thành công, hiển thị thông báo lỗi
            msg_box.setText("Incorrect email or password!")
            msg_box.exec()

    def showRegister(self):
        registerPage.show()
        self.close()

# Lớp chứa giao diện đăng ký
class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/register.ui", self)
        self.title= ""
        
        # Bắt sự kiện click chuột vào nút đăng ký
        self.pushButton.clicked.connect(self.Register)

        #Bắt sự kiện "đã có tài khoản" và chuyển sag trang đăng nhập
        self.pushButton_3.clicked.connect(self.showLoginPage)
    
    def Register(self):
        # Lấy thông tin email, usertitlevà mật khẩu từ người dùng
        self.title= self.lineEdit.text()
        email = self.lineEdit_3.text()
        password = self.lineEdit_4.text()

        # Kiểm tra các trường thông tin có được nhập hay không
        if not self.title:
            msg_box.setText("Please enter your title!")
            msg_box.exec()
            return
        if not email: 
            msg_box.setText("Please enter your email or phone number!")
            msg_box.exec()
            return
        if not password:
            msg_box.setText("Please enter a password!")
            msg_box.exec()
            return
        if not self.checkBox.isChecked():
            msg_box.setText("Please read and agree to the terms and conditions of The Fashion shop!")
            msg_box.exec()
            return
        
        if not self.validate_password(password):
            msg_box.setText("Password must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters.")
            msg_box.exec()
            return
        if not self.validate_email(email):
            msg_box.setText("Invalid email format!")
            msg_box.exec()
            return

        # Đóng giao diện đăng ký và chuyển sang giao diện chính
        mainPage = mainwindowPage.stackedWidget.currentWidget()
        mainPage.label_8.setText(self.title)
        mainwindowPage.show()        
        self.close()
    

    def validate_password(self, password):
        if len(password) < 8:
            return False
        if not re.search('[a-z]', password):
            return False
        if not re.search('[A-Z]', password):
            return False
        if not re.search('[0-9]', password):
            return False
        if not re.search('[^a-zA-Z0-9]', password):
            return False
        return True

    def validate_email(self, email):
        if '@' not in email:
            return False
        return True


    def showLoginPage(self):
        loginPage.show()
        self.close()

class ItemLoader:
    def __init__(self, json_file):
        with open(json_file, 'r', encoding='utf8') as file:
            self.data = json.load(file)

    def get_items(self):
        items = []
        for item in self.data:
            id = item['id']
            title = item['title']
            content = item['content']
            date = item['date']
            place = item['place']
            rating = item['rating']
            labels = item['labels']
            image = item['image']
            items.append((id, title, content, date, place, rating, labels, image))
        return items
    def update_items(self, items):
        updated_data = []
        existing_items = self.get_items()  # Lấy danh sách item hiện tại từ self.data

        for existing_item in existing_items:
            item_id = existing_item[0]
            matching_items = [item for item in items if item[0] == item_id]  # Tìm các item trong danh sách cần cập nhật có cùng ID

            if matching_items:
                updated_item = matching_items[0]  # Chỉ lấy một item duy nhất nếu có nhiều
            else:
                updated_item = existing_item  # Nếu không tìm thấy item trong danh sách cần cập nhật, giữ nguyên item hiện tại

            updated_data.append({
                'id': updated_item[0],
                'title': updated_item[1],
                'content': updated_item[2],
                'date': updated_item[3],
                'place': updated_item[4],
                'rating': updated_item[5],
                'labels': updated_item[6],
                'image': updated_item[7]
            })
        with open('json_file', 'w', encoding='utf8') as file:
            json.dump(updated_data, file, indent=4)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        self.loadUiFiles()
        self.displays()
        self.resize(800, 600)

    def loadUiFiles(self):
        ui_files = ['ui/Main.ui', 'ui/list.ui', 'ui/search.ui', 'ui/contact.ui']

        for ui_file in ui_files:
            widget = uic.loadUi(ui_file)
            self.stackedWidget.addWidget(widget)

        self.showMainPage()
        self.showItems()

    def displays(self):
        main_widget = self.stackedWidget.widget(0)
        main_widget.pushButton_3.clicked.connect(self.showListPage)
        main_widget.pushButton_2.clicked.connect(self.showSearchPage)
        main_widget.pushButton.clicked.connect(self.showContactPage)

        list_widget = self.stackedWidget.widget(1)
        list_widget.pushButton_4.clicked.connect(self.showMainPage)
        list_widget.pushButton_2.clicked.connect(self.showSearchPage)
        list_widget.pushButton.clicked.connect(self.showContactPage)

        search_widget = self.stackedWidget.widget(2)
        search_widget.pushButton_4.clicked.connect(self.showMainPage)
        search_widget.pushButton_3.clicked.connect(self.showListPage)
        search_widget.pushButton.clicked.connect(self.showContactPage)

        contact_widget = self.stackedWidget.widget(3)
        contact_widget.pushButton_4.clicked.connect(self.showMainPage)
        contact_widget.pushButton_2.clicked.connect(self.showSearchPage)
        contact_widget.pushButton_3.clicked.connect(self.showListPage)

        # # Kết nối comboBox với phương thức sortItems
        list_widget.comboBox.currentTextChanged.connect(self.sortItems)
        # Kết nói nút tìm kiếm với phương thức searchtimes
        search_widget = self.stackedWidget.widget(2)
        search_widget.pushButton_2.clicked.connect(self.searchItems)


    def showMainPage(self):
        self.stackedWidget.setCurrentIndex(0)

    def showListPage(self):
        self.stackedWidget.setCurrentIndex(1)

    def showSearchPage(self):
        self.stackedWidget.setCurrentIndex(2)

    def showContactPage(self):
        self.stackedWidget.setCurrentIndex(3)

    def showItems(self):
        list_widget = self.stackedWidget.widget(1)
        scroll_area = list_widget.scrollArea
        scroll_content_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_content_widget)

        self.item_loader = ItemLoader('data.json')
        items = self.item_loader.get_items()

        for item in items:
            detail_widget = DetailWidget(item, self.item_loader)
            scroll_layout.addWidget(detail_widget)

        scroll_area.setWidget(scroll_content_widget)

    #Phương thức sắp xếp
    def sortItems(self, sort_place):
        list_widget = self.stackedWidget.widget(1)
        scroll_area = list_widget.scrollArea
        scroll_content_widget = scroll_area.widget()
        scroll_layout = scroll_content_widget.layout()

        # Xóa các mục hiện có trong scroll_area
        while scroll_layout.count():
            child = scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        

        # Sắp xếp danh sách các mục
        items = self.item_loader.get_items()
        if sort_place == 'Giảm dần theo rating':
            items.sort(key=lambda x: x[5], reverse=True)  # Sắp xếp theo rating từ cao xuống thấp
        elif sort_place == 'Giảm dần theo rating':
            items.sort(key=lambda x: x[5])  # Sắp xếp theo rating từ thấp lên cao
        

        # Hiển thị danh sách đã sắp xếp
        for item in items:
            detail_widget = DetailWidget(item, self.item_loader)  # Truyền thêm đối số item_loader
            scroll_layout.addWidget(detail_widget)

        scroll_area.setWidget(scroll_content_widget)
        #Phương thức tìm kiếm
    def searchItems(self):
        search_widget = self.stackedWidget.widget(2)
        line_edit = search_widget.lineEdit
        search_text = line_edit.text()

        found_items = []
        items = self.item_loader.get_items()

        for item in items:
            if search_text.lower() in item[1].lower():  # Tìm kiếm theo tên (không phân biệt chữ hoa, chữ thường)
                found_items.append(item)

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Search Results")

    # Hiển thị kết quả tìm kiếm
        if found_items:
            search_widget = self.stackedWidget.widget(2)
            scroll_area = search_widget.scrollArea
            scroll_content_widget = QWidget()
            scroll_layout = QVBoxLayout(scroll_content_widget)

            for item in found_items:
                detail_widget = DetailWidget(item, self.item_loader)  # Truyền thêm đối số item_loader
                scroll_layout.addWidget(detail_widget)

            scroll_area.setWidget(scroll_content_widget)
            self.stackedWidget.setCurrentIndex(2)  # Chuyển sang trang kết quả tìm kiếm
        else:
            # Hiển thị thông báo khi không tìm thấy kết quả
            msg_box.setText("No items found.")
            msg_box.exec()

class DetailWidget(QWidget):
    def __init__(self, item, item_loader):
        super().__init__()
        self.item = item
        self.item_loader = item_loader
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label_id = QLabel(f"ID: {item[0]}")
        self.label_title = QLabel(f"Title: {item[1]}")
        self.label_rating = QLabel(f"Rating: {item[5]}")
        pixmap = QPixmap(item[7])
        self.label_image = QLabel()
        self.label_image.setPixmap(pixmap)

        self.label_id.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_rating.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.label_image)
        layout.addWidget(self.label_id)
        layout.addWidget(self.label_title)
        layout.addWidget(self.label_rating)

        self.button_show_detail = QPushButton("Show Detail")
        layout.addWidget(self.button_show_detail)

        self.button_show_detail.clicked.connect(self.showDetail)
#Them nút chinh sửa cho mỗi đối tượng và keests nối tới phương thức chỉnh sửa
        self.button_edit = QPushButton("Edit")
        self.button_edit.clicked.connect(self.editItem)
        layout.addWidget(self.button_edit)
#Thêm nút xóa cho mỗi đối tượng và kết nối tới phương thức xóa
        self.button_delete = QPushButton("Delete")
        layout.addWidget(self.button_delete)
        self.button_delete.clicked.connect(self.deleteItem)

    def showDetail(self):
        list_widget = QListWidget()
        list_widget.addItem(f"ID: {self.item[0]}")
        list_widget.addItem(f"Title: {self.item[1]}")
        list_widget.addItem(f"Content: {self.item[2]}")
        list_widget.addItem(f"Date: {self.item[3]}")
        list_widget.addItem(f"Place: {self.item[4]}")
        list_widget.addItem(f"Rating: {self.item[5]}")
        list_widget.addItem(f"Labels: {self.item[6]}")

        detail_dialog = QDialog(self)
        detail_dialog.setWindowTitle("Item Detail")
        detail_dialog.setFixedSize(300, 200)

        layout = QVBoxLayout(detail_dialog)
        layout.addWidget(list_widget)

        detail_dialog.exec()

    def editItem(self):
        edit_dialog = QDialog(self)
        edit_dialog.setWindowTitle("Edit Item")
        edit_dialog.setFixedSize(400, 400)

        layout = QVBoxLayout(edit_dialog)

        label_id = QLabel(f"ID: {self.item[0]}")
        layout.addWidget(label_id)

        label_title = QLabel("Title:")
        layout.addWidget(label_title)

        line_edit_title = QLineEdit(str(self.item[1]))
        layout.addWidget(line_edit_title)

        label_content = QLabel("Content:")
        layout.addWidget(label_content)

        line_edit_content = QLineEdit(str(self.item[2]))
        layout.addWidget(line_edit_content)

        label_date = QLabel("Date:")
        layout.addWidget(label_date)

        line_edit_date = QLineEdit(str(self.item[3]))
        layout.addWidget(line_edit_date)

        label_place = QLabel("Place:")
        layout.addWidget(label_place)

        line_edit_place = QLineEdit(str(self.item[4]))
        layout.addWidget(line_edit_place)

        label_rating = QLabel("Rating:")
        layout.addWidget(label_rating)

        line_edit_rating = QLineEdit(str(self.item[5]))
        layout.addWidget(line_edit_rating)

        label_labels = QLabel("Labels:")
        layout.addWidget(label_labels)

        line_edit_labels = QLineEdit(str(self.item[6]))
        layout.addWidget(line_edit_labels)

        button_upload_image = QPushButton("Upload Image")
        layout.addWidget(button_upload_image)

        button_upload_image.clicked.connect(lambda: self.uploadImage(line_edit_image))

        line_edit_image = QLineEdit()
        layout.addWidget(line_edit_image)

        button_save = QPushButton("Save")
        layout.addWidget(button_save)

        button_save.clicked.connect(lambda: self.saveItem(line_edit_title.text(),
                                                          line_edit_content.text(),
                                                          line_edit_date.text(),
                                                          line_edit_place.text(),
                                                          line_edit_rating.text(),
                                                          line_edit_labels.text(),
                                                          line_edit_image.text(), edit_dialog))

        edit_dialog.exec()

    def uploadImage(self, line_edit_image):
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix('.png')
        file_dialog.setWindowTitle("Upload Image")
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp *.gif)")

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            line_edit_image.setText(selected_files[0])

    def saveItem(self, title, content, date, place, rating, labels, image, edit_dialog):
        self.item = (
            self.item[0],
            str(title),
            str(content),
            str(date),
            str(place),
            float(rating),
            str(labels),
            image
        )
        self.item_loader.update_items([self.item])
        self.label_id.setText(f"ID: {self.item[0]}")
        self.label_title.setText(f"Title: {self.item[1]}")
        self.label_rating.setText(f"Rating: {self.item[5]}")
        pixmap = QPixmap(self.item[7])
        self.label_image.setPixmap(pixmap)

        edit_dialog.close()

        edit_dialog.close()
    def deleteItem(self):
        confirm_dialog = QDialog(self)
        confirm_dialog.setWindowTitle("Confirm Delete")
        confirm_dialog.setFixedSize(300, 100)

        layout = QVBoxLayout(confirm_dialog)

        label_message = QLabel("Are you sure you want to delete this item?")
        layout.addWidget(label_message)

        button_confirm = QPushButton("Confirm")
        layout.addWidget(button_confirm)

        button_confirm.clicked.connect(lambda: self.confirmDelete(confirm_dialog))

        confirm_dialog.exec()

    def confirmDelete(self, confirm_dialog):
        items = self.item_loader.get_items()
        if self.item in items:
            items.remove(self.item)
            self.item_loader.update_items(items)
            self.setParent(None)
            self.deleteLater()

        confirm_dialog.close()

if __name__ == '__main__':
    app = QApplication([])
    #Tạo các đối tượng tương ứng với các trang giao diện
    loginPage = Login()
    loginPage.show()
    registerPage = Register()
    mainwindowPage = MainWindow()
    # Thiết lập hộp thoại thông báo lỗi
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Error")
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setStyleSheet("background-color: #F8F2EC; color: #356a9c")
    
    app.exec()