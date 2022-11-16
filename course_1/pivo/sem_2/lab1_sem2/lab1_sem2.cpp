#include <iostream>
#include "Header.h";
#include <string>;
using namespace std;

void get_suf(int size, ArrSuf a)
{
	int* suf_int = new int[size];
	suf_int = a.ArrSuf_get();

	for (int i = 0; i < size; i++)
	{
		cout << suf_int[i];
	}
	cout << endl;
	
}

void get_shift(ArrSuf a)
{
	string str;
	str = a.Shift();
	cout << str<<endl;
}

void get_MaxPref(ArrSuf a)
{
	int pos1, pos2;
	string pref;
	cout << "Введите номера элементов строки, с которых попробуем найти наибольший общий префикс: ";
	cin >> pos1>>pos2;
	pref = a.Pref(pos1, pos2);
	cout << pref<<endl;

}

int main()
{
	setlocale(LC_ALL, "rus");
	bool check = true;
	while (check)
	{
		cout << "Введите строку: ";
		string str;
		cin >> str;
		ArrSuf a(str);
		cout << "Выберите действие: 1. Найти суффиксный массив строки 2. Найти минимальный циклиеский сдвиг 3. Найти наибольший общий префикс двух подстрок 4. Выйти из программы: ";
		int choose;
		cin >> choose;

		switch (choose)
		{
		 case 1:
			 get_suf(str.length(), a);
			 break;
		 case 2:
			 get_shift(a);
			 break;
		 case 3:
			 get_MaxPref(a);
			 break;
		 case 4:
			 check = !check;
			 break;

		}
	}
	

	
	
}