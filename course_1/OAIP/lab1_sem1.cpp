#include <iostream>
#include <Windows.h>
#include <string>
#include <vector>
#include <sstream>
using namespace std;

vector<int> get_marks(string sub) //Для ввода отметок
{
    string m, mark;
    vector <string> sub_mark_str;
    vector<int> sub_mark_int;
    cout << "Оценки по предмету " << sub<<": ";
    getline(cin, m);
    m += ' ';

    for (int i = 0; i < m.length(); i++)
    {
        if (m[i] != ' ')
        {
            mark += m[i];
        }
        else
        {
            if (mark != "")
            {
                sub_mark_str.push_back(mark);
            }
            mark = "";

        }
    }
    for (int i = 0; i < sub_mark_str.size(); i++)
    {
        sub_mark_int.push_back(stoi(sub_mark_str[i]));
    }
    return sub_mark_int;

}


vector<string> get_name(string name_get) //функция для запихивания имен в вектор
{
    string name;
    vector<string> names_of_students;

    name_get += ' ';

    for (int i = 0; i < name_get.length(); i++)
    {
        if (name_get[i] != ' ')
        {
            name += name_get[i];
        }
        else
        {
            if (name != "")
            {
                names_of_students.push_back(name);
            }
            name = "";

        }
    }
    return names_of_students;
}

class Subjects 
{
public:
    vector<int> physics;
    vector<int> math;
    vector<int> inf;
    vector<int> chemistry;
    
};

class Student : public Subjects
{
public:
    string name;
    int date_of_birthday;
    int numb_of_group;


    void creating(string name_get, int date_of_birthday_get, int numb_of_group_get, vector<int> physics_get, vector<int> math_get, vector<int> inf_get, vector<int> chemistry_get) //получение инфы
    {
        name = name_get; 
        date_of_birthday = date_of_birthday_get;
        numb_of_group = numb_of_group_get;
        physics = physics_get;
        math = math_get;
        inf = inf_get;
        chemistry = chemistry_get;
    }

    void check_marks(vector<int> subject) //для вывода оценок(используется только в функци check)
    {
        for (int i = 0; i < subject.size(); i++)
        {
            cout << subject[i] << " ";
        }
        cout << endl;
    }
    void check()      //Функция для вывода инфы о студенте
    {
        cout << name << endl;
        cout << date_of_birthday<<endl;
        cout << numb_of_group<<endl;
        cout << "Physics: ";
        check_marks(physics);
        cout << "math: ";
        check_marks(math);
        cout << "programming: ";
        check_marks(inf);
        cout << "chemistry: ";
        check_marks(chemistry);
    }

    void correction(int choose)
    {

    }
};




int main()
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    string name_get, name;
    vector <string> names_of_students;
    cout << "Вводите имя учеников в строку"<<endl;
    getline(cin, name_get);

    names_of_students = get_name(name_get); //вызываем функцию для запихивания имен в вектор
    
    vector <Student> students(names_of_students.size());
    
    for (int i = 0; i < names_of_students.size(); i++)
    {
        int year_of_birthday, groop_number;
        cout << "Введите информацию о студенте " << names_of_students[i] << ": " << endl << "Год рождения: ";
        cin >> year_of_birthday;
        cout << "\nНомер группы: ";
        cin >> groop_number;
        vector<int> math = get_marks("математика");
        vector<int> physics = get_marks("физика");
        vector<int> prog = get_marks("Информатика");
        vector<int> chemistry = get_marks("Химия");

        students[i].creating(names_of_students[i], year_of_birthday, groop_number, math, physics, prog, chemistry);
    }
    
    
    
    /*Student vas;
    vector<int> math{ 1, 2, 3 };
    vector<int> physics{ 1, 2, 3 };
    vector<int> prog{ 1, 2, 3 };
    vector<int> chem{ 1, 2, 3 };
    vas.creating("Ivanjv A.O", 2004, 3, math, physics, prog, chem);
    vas.check();*/
}