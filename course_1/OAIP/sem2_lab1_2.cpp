#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <Windows.h>
#include <fstream>

using namespace std;

vector<string> get_surnames(string sur)
{
	vector<string> surnames;
	string surname="";
	sur += ' ';
	bool a=true;
	for (int i = 0; i < sur.length(); i++)
	{
		if (sur[i] != ' ')
		{
			surname += sur[i];
			a = 0;
		}

		else if(sur[i]==' ' && a==0)
		{
			surnames.push_back(surname);
			surname = "";
			a=1;
		}
	}
	return surnames;
}

void aver(int physics, int math, int inf, int chem, double& average)
{

	average = (physics + math + inf + chem) / 4.;
}


class Student
{
protected:
	string name, father_name;
	int year, numb_of_groop, physics, math, inf, chem;
	double  average;

public:
	string surname;

	void enter_info(string surname)
	{
		this->surname = surname;
		cout << "Введите инфу по студенту " << surname<<endl;
		cout << "Введите имя: ";
		cin >> name;
		cout << "\nВведите отчество: ";
		cin >> father_name;
		cout << "\nВведите год рождения: ";
		cin >> year;
		cout << "\nВведите номер группы: ";
		cin >> numb_of_groop;
		cout << "\nВведите оценки за семестр: " << endl << "По физике: ";
		cin >> physics;
		cout << "\nПо математике: ";
		cin >> math;
		cout << "\nПо информатике: ";
		cin >> inf;
		cout << "\nПо химии: ";
		cin >> chem;

		aver(physics, math, inf, chem, average);

	}

	void enter_info(string surname_file, string name_file, string father_name_file, int year_file, int numb_of_groop_file, int physics_file, int math_file, int inf_file, int chem_file)
	{
		surname = surname_file;
		name = name_file;
		father_name = father_name_file;
		year = year_file;
		numb_of_groop = numb_of_groop_file;
		physics = physics_file;
		math = math_file;
		inf = inf_file;
		chem = chem_file;
		aver(physics, math, inf, chem, average);
	}

	void get_info()
	{
		cout <<endl<< surname << " "<<name <<" "<< father_name << endl;
		cout << "Год: " << year<<endl;
		cout << "Группа: " << numb_of_groop<<endl;
		cout << "Отметка по" << endl;
		cout << "Математике: " << math<<endl;
		cout << "Физике: " << physics << endl;
		cout << "Информатике: " << inf << endl;
		cout << "Химии: " << chem<<endl;
		cout << "Средняя отметка: " << average<<endl;

	}

	void changing(vector<string>& surnames, int numb)
	{
		string new_name;
		int choose;
		cout << "Что вы хотите изменить? 1. Фамилию 2. Имя 3. Отчество 4. Год рождения 5. Номер группы 6. Отметку по физике 7. Отметку по математике 8. Отметку по информатике 9. Отметку по химии: ";
		cin >> choose;

		switch (choose)
		{

		 case 1:
			cout << "\nНовая фамилия: ";
			
			cin >> new_name;
			surnames[numb] = new_name;
			surname = new_name;
			break;

		 case 2:
			 cout << "\nНовое имя: ";
			 cin >> name;
			 break;
		 case 3:
			 cout << "\n Новое отчество: ";
			 father_name = father_name;
			 break;
		 case 4:
			 cout << "\n Год рождения: ";
			 cin >> year;
			 break;
		 case 5:
			 cout << "\nНомер группы: ";
			 cin >> numb_of_groop;
			 break;
		 case 6:
			 cout << "\nОтметка по физике: ";
			 cin >> physics;
			 break;
		 case 7:
			 cout << "\nОтметка по математике: ";
			 cin >> math;
			 break;
		 case 8:
			 cout << "\nОтметка по информатике: ";
			 cin >> inf;
			 break;
		 case 9:
			 cout << "\nОтметка по химии: ";
		     cin >> chem;
			 break;
		}
		aver(physics, math, inf, chem, average);
	}

	void honors()
	{
		if (math >= 9 && inf >= 9 && chem >= 9 && physics >= 9)
		{
			ofstream file("honors.txt", ios::app);
			if (file.is_open()) cout << "ok";
			file << surname << " " << name << ' ' << father_name << endl;
			file << "Год рождения: " << year<<endl;
			file << "Номер группы: " << numb_of_groop << endl;
			file << "Физика: " << physics << endl;
			file << "Математика: " << math << endl;
			file << "Информатика: " << inf << endl;
			file << "Химия: " << chem << endl;
			file.close();
		}
	}

	void save_in_file()
	{
		ofstream file("save_info.txt", ios::app);
		file << surname << " " << name << " " << father_name << " " << year << " " << numb_of_groop << " " << physics << " " << math << " " << inf << " " << chem << endl;

		file.close();
	}

};

int choose_student(vector<Student> student)
{
	int choose;
	cout << "Выберите студента: ";
	for (int i = 0; i < student.size(); i++)
	{
		cout << i + 1 << " " << student[i].surname << " ";
	}
	cout << ":";
	cin >> choose;
	return choose;
}


void info(vector<Student> student)
{
	int choose;
	cout << "О каком студенте хотите получить инфу: ";
	for (int i = 0; i < student.size(); i++)
	{
		cout << i+1 << ". " << student[i].surname << " ";
	}
	cin >> choose;
	student[choose - 1].get_info();
}

void enter_from_file(vector<Student>& student, vector<string>& surnames)
{
	vector<string> file_surname, name, father_name;
	vector <int> year, numb_of_groop, physics, math, inf, chem;
	ifstream file_enter;
	file_enter.open("D:\\уник\\уник проги\\labs_cons\\sem2\\sem2_lab1_2\\enter_info.txt");
	while (!file_enter.eof())
	{
		int a;
		string str;
		file_enter >> str;
		file_surname.push_back(str);
		surnames.push_back(str);
		file_enter >> str;
		name.push_back(str);
		file_enter >> str;
		father_name.push_back(str);
		file_enter >> a;
		year.push_back(a);
		file_enter >> a;
		numb_of_groop.push_back(a);
		file_enter >> a;
		physics.push_back(a);
		file_enter >> a;
		math.push_back(a);
		file_enter >> a;
		inf.push_back(a);
		file_enter >> a;
		chem.push_back(a);
	}

	if (file_surname.size() != 0 /* && file_surname.size() == name.size() == father_name.size() == year.size() == numb_of_groop.size() == physics.size() == math.size() == inf.size() == chem.size()*/)
	{
		int b = 0;
		int elem_beg = student.size();
		student.resize(student.size() + file_surname.size());
		for (int i = elem_beg; i < student.size(); i++)
		{
			student[i].enter_info(file_surname[b], name[b], father_name[b], year[b], numb_of_groop[b], physics[b], math[b], inf[b], chem[b]); //решить вопрос с индексами
			b++;
		}
	}
	else cout << "В файле не записан ни один студент или хвататет данных";
	
	file_enter.close();
	
}

void saving_file(vector<Student> student)
{
	ofstream file("save_info.txt");
	file.close();
	for (int i = 0; i < student.size(); i++)
	{
		student[i].save_in_file();
	}
}

void changing(vector<Student>& student, vector<string>& surnames)
{
	int choose;
	string new_stud;

	cout << "\nЧто вы хотите сделать? 1. Удалить студента 2. Добавить студента 3. Добавить студента с файла 4. Изменить информацию о студенте 5. Отмена действия: ";
	cin >> choose;

	switch (choose)
	{
	 case 1:
		
		choose = choose_student(student);
		student.erase(student.begin() + choose - 1);
		break;

	 case 2:
		 cout << "Фамилия нового студента: ";
		 cin >> new_stud;
		 student.resize(student.size()+1);
		 surnames.push_back(new_stud);
		 student[student.size() - 1].enter_info(surnames[surnames.size() - 1]);
		 break;
	 case 3:
		 enter_from_file(student, surnames);
		 break;

	 case 4:
		 choose = choose_student(student);
		 student[choose - 1].changing(surnames, choose-1);
		 break;

	 case 5:
		 break;
	}

}

void students_letter(vector<Student> students)
{
	char letter;
	cout << "Введите букву, с которой будут начинаться начинаться имена отличников: ";
	cin >> letter;
	ofstream file("honors.txt");
	file.close();

	for (int i = 0; i < students.size(); i++)
	{
		if (students[i].surname[0] == letter)
		{
			students[i].honors();
		}
	}

}

int main()
{
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);

	cout << "Введите фамилии студентов в строку: ";
	int choose;
	bool a = true;;
	string sur;
	vector <string> surnames;
	getline(cin, sur);

	surnames = get_surnames(sur);

	vector<Student> student(surnames.size());

	for (int i = 0; i < student.size(); i++)
	{
		student[i].enter_info(surnames[i]);
	}

	while (a)
	{
		cout << "\n1. Просмотреть инфу по студенту 2. Изменить инфу о студенте; 3.Вывести отличников, фамилии которых начинаются с заданной буквы 4. Записать всю инфу в файл 5. Выйти из программы: ";

		cin >> choose;

		switch (choose)
		{
		case 1:
			info(student);
			break;
		case 2:
			changing(student, surnames);
			break;
		case 3:
			students_letter(student);
			break;
		case 4:
			saving_file(student);
			break;
		case 5:
			a = false;
			break;
		}


		
	}
}