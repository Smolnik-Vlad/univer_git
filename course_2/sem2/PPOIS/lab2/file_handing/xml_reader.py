import xml
from tkinter import filedialog
from xml.sax.handler import ContentHandler
import xml.etree.ElementTree as ET

from models.models import Student


class XMLReader(ContentHandler):

    @staticmethod
    def __reading_parser(filename):
        tree = ET.parse(filename)  # замените file.xml на имя вашего файла
        root = tree.getroot()

        students = []

        for student in root.findall('student'):
            student_data = {}
            for field in student:
                student_data[field.tag] = field.text
            students.append(student_data)
        return students

    @staticmethod
    def reader():
        file_path = filedialog.askopenfilename()
        students = XMLReader.__reading_parser(file_path)
        Student.set_students_from_file(students)
