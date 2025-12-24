# импортируем необходимые модули
import sys
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt  # импорт matplotlib для графиков

# создаем класс для нашего приложения, наследуемся от qwidget
class SimpleSalaryCalc(QWidget):
    def __init__(self): 
        super().__init__() #наследование всех свойств и методов родительского класса QWidget
        self.initUI() #создание метода, раскрывающего детали приложения
        
    def initUI(self):
        self.setWindowTitle("Зарплата") #заголовок окна приложения
        self.setGeometry(100, 100, 400, 400) #параметры начальной точки (x,y) и размеров окна приложения
        
        layout = QVBoxLayout() #создания экземпляра класса вертикального макета
        self.setLayout(layout) #добавление макета в окно
        
        #данные для расчетов
        self.mrot = 15279 #мрот для расчета оклада
        self.last_salary = 32000 #зарплата за прошлый месяц для сравнения
        self.coeff = {"1": 1.00, "2": 1.05, "3": 1.10, "4": 1.15} #тарифные коэффициенты
        
        #создание элементов интерфейса
        layout.addWidget(QLabel("Рабочих дней:")) #метка для поля ввода
        self.days_input = QLineEdit() #поле ввода количества рабочих дней
        layout.addWidget(self.days_input)
        
        layout.addWidget(QLabel("Отработано дней:")) #метка для поля ввода
        self.worked_input = QLineEdit() #поле ввода количества отработанных дней
        layout.addWidget(self.worked_input)
        
        layout.addWidget(QLabel("Разряд:")) #метка для выбора разряда
        self.grade_combo = QComboBox() #выпадающий список для выбора разряда
        self.grade_combo.addItems(["1", "2", "3", "4"]) #добавление вариантов выбора
        layout.addWidget(self.grade_combo)
        
        #кнопки для выполнения расчетов
        self.btn_oklad = QPushButton("Оклад") #кнопка расчета оклада
        self.btn_oklad.clicked.connect(self.calc_oklad) #привязка к методу расчета
        layout.addWidget(self.btn_oklad)
        
        self.oklad_result = QLineEdit() #поле для вывода результата расчета оклада
        self.oklad_result.setReadOnly(True) #поле только для чтения
        layout.addWidget(self.oklad_result)
        
        self.btn_salary = QPushButton("Зарплата") #кнопка расчета зарплаты
        self.btn_salary.clicked.connect(self.calc_salary) #привязка к методу расчета
        layout.addWidget(self.btn_salary)
        
        self.salary_result = QLineEdit() #поле для вывода результата расчета зарплаты
        self.salary_result.setReadOnly(True) #поле только для чтения
        layout.addWidget(self.salary_result)
        
        self.btn_dinamika = QPushButton("Динамика") #кнопка показа динамики
        self.btn_dinamika.clicked.connect(self.show_dinamika) #привязка к методу
        layout.addWidget(self.btn_dinamika)
        
        self.dinamika_result = QLineEdit() #поле для вывода динамики
        self.dinamika_result.setReadOnly(True) #поле только для чтения
        layout.addWidget(self.dinamika_result)
    
    def calc_oklad(self): #метод расчета оклада
        try:
            grade = self.grade_combo.currentText() #получение выбранного разряда
            oklad = self.mrot * self.coeff[grade] #расчет оклада по формуле
            self.oklad_result.setText(f"{oklad:.0f} руб.") #вывод результата
        except:
            self.oklad_result.setText("Ошибка") #обработка ошибок
    
    def calc_salary(self): #метод расчета зарплаты
        try:
            days = float(self.days_input.text()) #получение рабочих дней
            worked = float(self.worked_input.text()) #получение отработанных дней
            grade = self.grade_combo.currentText() #получение разряда
            
            oklad = self.mrot * self.coeff[grade] #расчет оклада
            salary = oklad * worked / days #расчет зарплаты по формуле
            self.salary_result.setText(f"{salary:.0f} руб.") #вывод результата
        except:
            self.salary_result.setText("Ошибка") #обработка ошибок
    
    def show_dinamika(self): #метод показа динамики зарплаты с гистограммой
        try:
            days = float(self.days_input.text()) #рабочих дней
            worked = float(self.worked_input.text()) #отработанных дней
            sick_days = days - worked #расчет дней болезни
            
            grade = self.grade_combo.currentText() #разряд
            oklad = self.mrot * self.coeff[grade] #оклад
            salary = oklad * worked / days #текущая зарплата
            
            #создание гистограммы
            labels = ['Прошлый месяц', 'Текущий месяц'] #подписи столбцов
            values = [self.last_salary, salary] #значения зарплат
            colors = ['blue', 'green'] if salary > self.last_salary else ['blue', 'red'] #цвета столбцов
            
            #создание графика
            plt.figure(figsize=(8, 5)) #размер окна графика
            bars = plt.bar(labels, values, color=colors, width=0.6) #создание столбцов
            
            #добавление значений над столбцами
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, height + 100, 
                        f'{height:.0f} руб.', ha='center', va='bottom')
            
            #настройки графика
            plt.title(f'Динамика зарплаты\n(больничных дней: {sick_days:.0f})') #заголовок с днями болезни
            plt.ylabel('Зарплата (руб.)') #подпись оси Y
            plt.grid(axis='y', alpha=0.3) #горизонтальная сетка
            plt.ylim(0, max(values) * 1.2) #масштаб оси Y
            
            #отображение графика
            plt.tight_layout()
            plt.show()
            
            #текстовый вывод в поле
            if salary > self.last_salary: #сравнение с прошлым месяцем
                text = f"↑ На {salary-self.last_salary:.0f} руб." #рост
            else:
                text = f"↓ На {self.last_salary-salary:.0f} руб." #снижение
            
            self.dinamika_result.setText(f"Болезнь: {sick_days:.0f} дн. {text}") #вывод
            
        except ValueError:
            self.dinamika_result.setText("Ошибка: введите числа в поля дней")
        except Exception as e:
            self.dinamika_result.setText(f"Ошибка: {str(e)}")

#основная часть программы
app = QApplication(sys.argv) #создания экземпляра приложения QApplication
window = SimpleSalaryCalc() #создание окна приложения
window.show() #демонстрация окна приложения
sys.exit(app.exec_()) #запуск основного цикла приложения