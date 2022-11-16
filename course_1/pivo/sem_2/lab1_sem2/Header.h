#pragma once
#include<string>;
using namespace std;

class ArrSuf
{
private:
	string str;
	int* arrSuf_int;
	string* arrSuf_str;
	int arr_size;
public:
	ArrSuf(string str);
	int* ArrSuf_get();
	string Pref( int a, int b);
	string Shift();
};

