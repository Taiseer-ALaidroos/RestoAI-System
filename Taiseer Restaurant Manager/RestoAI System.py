from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QMessageBox, QInputDialog,QListWidgetItem
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import speech_recognition as sr
import re
import sqlite3

class Main(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("log_in.ui", self)
        self.logIn_puttun.clicked.connect(self.verify_log_in)
        

    def verify_log_in(self):
        UserName=self.UserNameInput.text()
        password=self.Password_Input.text()

        if password=="1234":
            self.open_Manager_window()
        elif password=="1212":
            self.open_casheir_window()

        else:
            QMessageBox.warning(self,"خطا","عذرا ,, ليس لديك حساب مستخدم")    

   
    def open_casheir_window(self):
        self.Casheir =CasheirWindow()
        self.Casheir.show()

    def open_Manager_window(self):
        self.manager=Manager()
        self.manager.show()    

class CasheirWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("meals.ui", self)

        # قائمة الوجبات مع الأسعار والصور
        self.meal_data = {
            "شاورما": {"price": 500, "image": "photo/shawrma1.webp"},
            "بروست": {"price": 2500, "image": "photo/broast.webp"},
            "فلافل": {"price": 250, "image": "photo/falafel_sandwish.webp"},
            "بيتزا": {"price": 800, "image": "photo/pizza.jpg"},
            "بطاطس": {"price": 800, "image": "photo/botato.webp"},
            "برجر": {"price": 800, "image": "photo/Burger.jpg"},
        }

        # قائمة المشروبات مع الأسعار والصور
        self.juice_data = {
            "قهوة اسبريسو": {"price": 1500, "image": "photo/spareso_coffee.webp"},
            "قهوة كابتشينو": {"price": 1200, "image": "photo/cappuccino.jpg"},
            "شاي": {"price": 50, "image": "photo/tea.jpg"},
            "ميلك شيك": {"price": 1000, "image": "photo/milk_sheak.jpg"},
            "كوكا كولا": {"price": 600, "image": "photo/coca_cola.jpg"},
            "بيبسي": {"price": 600, "image": "photo/Pepsi.jpg"},
            "سبرايت": {"price": 600, "image": "photo/sprite.jpg"},
            "قهوة مثلجة": {"price": 1800, "image": "photo/Ice_coffee.jpg"}
        }

        self.list_meals.itemClicked.connect(self.display_image)
        self.list_juice.itemClicked.connect(self.display_image)
        self.list_meals.itemClicked.connect(self.handle_meal_selection)
        self.list_juice.itemClicked.connect(self.handle_juice_selection)
        self.pushButton_voice.clicked.connect(self.start_voice_input)
        self.pushButton_calculate.clicked.connect(self.calculate_total)
        self.pushButton_pay.clicked.connect(self.process_payment)

        self.table_orders.setColumnCount(3)  # تم تعديل عدد الأعمدة ليكون 3 (الصنف, الكمية, السعر الإجمالي)
        self.table_orders.setHorizontalHeaderLabels(["الصنف", "الكمية", "السعر الإجمالي"])

    def handle_meal_selection(self, item):
        """ إضافة الطلب عند اختيار وجبة بالنقر """
        meal_name = item.text()
        self.display_image(meal_name)  # عرض الصورة
        self.add_order(meal_name)      # إضافة الطلب للجدول

    def handle_juice_selection(self, item):
        """ إضافة الطلب عند اختيار مشروب بالنقر """
        juice_name = item.text()
        self.display_image(juice_name)  # عرض الصورة
        self.add_order(juice_name)      # إضافة الطلب للجدول


    def display_image(self, item):
        """ عرض صورة الوجبة أو المشروب في نفس QLabel """
        if isinstance(item, QListWidgetItem):  # التأكد أن العنصر من القائمة
            item_name = item.text()  # استخراج النص الصحيح من العنصر
        else:
            item_name = item  # إذا كان النص مُمررًا مباشرة، استخدمه كما هو

        if not item_name:
            QMessageBox.warning(self, "خطأ", "لم يتم تحديد عنصر لعرض صورته!")
            return

        # البحث عن الصورة في قوائم المشروبات والوجبات
        meal_info = self.meal_data.get(item_name)
        juice_info = self.juice_data.get(item_name)

        image_path = None
        if meal_info:
            image_path = meal_info.get("image")
        elif juice_info:
            image_path = juice_info.get("image")

        if image_path:
            pixmap = QPixmap(image_path)
            self.label_photo.setPixmap(pixmap.scaled(self.label_photo.size()))
        else:
            QMessageBox.warning(self, "خطأ", f"لم يتم العثور على صورة لـ {item_name}")

    def start_voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language='ar-SA')
            self.process_voice_command(text)
        except sr.UnknownValueError:
            QMessageBox.warning(self, "خطأ", "لم يتم التعرف على الصوت")
        except sr.RequestError:
            QMessageBox.warning(self, "خطأ", "تعذر الاتصال بخدمة التعرف على الصوت")

    def process_voice_command(self, command):
        """ معالجة الأمر الصوتي وإضافة الطلب تلقائيًا """
        for meal in self.meal_data:
            if meal in command:
                self.display_image(meal)  # عرض صورة الوجبة
                self.add_order(meal)       # إضافة الطلب إلى الجدول
                return

        for juice in self.juice_data:
            if juice in command:
                self.display_image(juice)  # عرض صورة المشروب
                self.add_order(juice)      # إضافة الطلب إلى الجدول
                return

        QMessageBox.warning(self, "خطأ", "لم يتم العثور على الطلب")

    def select_meal(self, meal_name):
        items = self.list_meals.findItems(meal_name, Qt.MatchFlag.MatchExactly)
        if items:
            self.list_meals.setCurrentItem(items[0])
            self.display_image(self.list_meals.currentItem())
            self.add_order(meal_name)  # إضافة الطلب بعد عرض الصورة
        else:
            QMessageBox.warning(self, "خطأ", f"لم يتم العثور على الوجبة: {meal_name}")

    def select_juice(self, juice_name):
        items = self.list_juice.findItems(juice_name, Qt.MatchFlag.MatchExactly)
        if items:
            self.list_juice.setCurrentItem(items[0])
            self.display_image(self.list_juice.currentItem())
            self.add_order(juice_name)  # إضافة الطلب بعد عرض الصورة
        else:
            QMessageBox.warning(self, "خطأ", f"لم يتم العثور على المشروب: {juice_name}")

    def add_order(self, meal_name=None):
        """ إضافة الطلبات إلى الجدول مع إدخال الكمية عبر مربع حوار """
        if not meal_name:
            QMessageBox.warning(self, "خطأ", "يرجى اختيار وجبة أو مشروب!")
            return

        # البحث عن السعر في قوائم المشروبات والوجبات
        price = self.meal_data.get(meal_name, {}).get("price", self.juice_data.get(meal_name, {}).get("price", 0))

        # التأكد من أن الصنف موجود بالفعل في البيانات
        if price == 0:
            QMessageBox.warning(self, "خطأ", f"لم يتم العثور على {meal_name} في القائمة!")
            return

        # طلب إدخال الكمية يدويًا عبر مربع حوار
        quantity, ok = QInputDialog.getInt(self, "إدخال الكمية", f"كم عدد {meal_name} الذي تريده؟", 1, 1, 100)

        if not ok:  # في حال تم إلغاء الإدخال
            return

        total_price = price * quantity

        # إضافة الطلب إلى الجدول
        row_position = self.table_orders.rowCount()
        self.table_orders.insertRow(row_position)
        self.table_orders.setItem(row_position, 0, QTableWidgetItem(meal_name))
        self.table_orders.setItem(row_position, 1, QTableWidgetItem(str(quantity)))
        self.table_orders.setItem(row_position, 2, QTableWidgetItem(str(total_price)))

    def get_quantity_from_voice(self, meal_name):
        """ إظهار حوار إدخال للكمية بدلاً من التعرف عليها صوتياً """
        quantity, ok = QInputDialog.getInt(self, "إدخال الكمية", f"كم عدد {meal_name} الذي تريده؟", 1, 1, 100)
        
        if ok:
            return quantity
        return None  # إذا ألغى المستخدم الإدخال


    def extract_number_from_text(self, text):
        """ محاولة استخراج الرقم من النص المدخل """
        numbers = re.findall(r'\d+', text)
        if numbers:
            return int(numbers[0])  # إذا تم العثور على الرقم، أعده
        return None  # إذا لم يتم العثور على رقم

    def calculate_total(self):
        """ حساب الإجمالي بناءً على الطلبات في الجدول """
        total_price = 0
        for row in range(self.table_orders.rowCount()):
            total_price += int(self.table_orders.item(row, 2).text())

        # عرض المجموع
        self.label_total.setText(f"{total_price} ريال")

    def process_payment(self):
        """ معالجة الدفع والتأكد من أن المبلغ كافٍ """
        total_price = 0
        for row in range(self.table_orders.rowCount()):
            total_price += int(self.table_orders.item(row, 2).text())

        if total_price == 0:
            QMessageBox.warning(self, "خطأ", "لم يتم اختيار أي طلب بعد!")
            return

        # طلب إدخال المبلغ المدفوع من المستخدم
        amount_paid, ok = QInputDialog.getDouble(self, "إدخال المبلغ", "الرجاء إدخال المبلغ المدفوع:", 0, 0, 100000, 2)

        if not ok:
            return  # المستخدم ألغى الإدخال

        if amount_paid < total_price:
            QMessageBox.critical(self, "خطأ", "المبلغ المدفوع غير كافٍ! يرجى دفع المبلغ المطلوب.")
        else:
            # حساب المبلغ المسترد
            change = amount_paid - total_price
            QMessageBox.information(self, "نجاح", f"أهلاً وسهلاً بك، يرجى الانتظار حتى يتم تجهيز طلبك! \nالمبلغ المسترد: {change} ريال")
            self.reset_order()

    def reset_order(self):
        """ إعادة تعيين الطلبات بعد الدفع """
        self.table_orders.setRowCount(0)  # مسح الجدول
        self.label_total.setText(" 0 ريال")  # إعادة ضبط السعر الإجمالي
    
class Manager(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("Manager.ui",self)

        self.pushButton_select_Employee.clicked.connect(self.selectEmployee)
        self.pushButton_add_Emplyee.clicked.connect(self.addEmployeeFunc)
        self.pushButton_Edit_Emplyee.clicked.connect(self.edit_employee)
        self.pushButton_Delete_Emplyee.clicked.connect(self.deleteEmployee)
        self.pushButton_back.clicked.connect(self.close)

    def addEmployeeFunc(self):
        self.addEmployee=add_employee()
        self.addEmployee.show()

    def selectEmployee(self):
        self.selectEmployee=Get_employee()
        self.selectEmployee.show()

    def edit_employee(self):
        self.editEmployee=edit_employee()
        self.editEmployee.show()

    def deleteEmployee(self):
        self.deleteEmployees=DeleteEmployee()
        self.deleteEmployees.show()

class add_employee(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("AddEmployee.ui",self)
        self.pushButton_send_data.clicked.connect(self.add_employee_func)
        self.pushButton_back.clicked.connect(self.close)
        
    def add_employee_func(self):
        name=self.Input_name_Employee.text()
        id=self.Input_id_Employee.text()
        position=self.Input_position_Employee.text()
        salary=self.Input_salary_Employee.text()

        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO employees (name, position, salary,id) VALUES (?, ?, ?, ?)", 
                    (name, position, salary,id))
        
        conn.commit()
        conn.close()
        QMessageBox.information(self, "نجاح","تمت اضافة الموظف بنجاح")
        print('//////////////////////////////////')

class edit_employee(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("EditEmployee.ui",self)

        self.pushButton_send_data.clicked.connect(self.Edit_employee_func)
        self.pushButton_back.clicked.connect(self.close)
        
    def Edit_employee_func(self):
        name=self.Input_name_Employee.text()
        id=self.Input_id_Employee.text()
        position=self.Input_position_Employee.text()
        salary=self.Input_salary_Employee.text()

        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()

        cursor.execute("UPDATE employees SET name= ?, position = ?, salary = ? WHERE id = ?", 
                   (name, position, salary,id))
        

        
        conn.commit()
        conn.close()
        QMessageBox.information(self, "نجاح","تمت التعديل على بيانات الموظف بنجاح")
        print('//////////////////////////////////')

class Get_employee(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("getEmployees.ui",self)

        self.pushButton_back.clicked.connect(self.close)
        
        self.load_employees()  # تحميل الموظفين عند فتح النافذة
    
    def load_employees(self):
        """تحميل بيانات الموظفين من قاعدة البيانات وعرضها في الجدول"""
        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, position, salary FROM employees")
        employees = cursor.fetchall()  # جلب جميع الموظفين
        
        self.tableWidgetEmployees.setRowCount(len(employees))  # ضبط عدد الصفوف
        
        for row_idx, emp in enumerate(employees):
            for col_idx, data in enumerate(emp):
                self.tableWidgetEmployees.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        
        conn.close()

class DeleteEmployee(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("DeleteEmployee.ui",self)

        self.pushButton_delete.clicked.connect(self.delete_employee_func)
        self.pushButton_back.clicked.connect(self.close)
        
    def delete_employee_func(self):
       
        id=self.Input_id_Employee.text()
       
        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()
    
        cursor.execute("DELETE FROM employees WHERE id = ?", (id,))
        
        conn.commit()
        conn.close()
        QMessageBox.information(self, "نجاح","تمت حذف الموظف بنجاح")
        print('//////////////////////////////////')

app = QApplication([])
main = Main()
main.show()
app.exec()