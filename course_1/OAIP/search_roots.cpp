#include <iostream>
#include <math.h>

using namespace std;

double Function(double x)
{
	return pow(x, 2) - 10 * pow(sin(x), 2) + 2;
}

double dF(double x)
{
	return 2 * x -10*sin(2*x);
}

double Method_Newton(double x0, double e)
{
	double x1;
	x1 = x0 - Function(x0) / dF(x0);
	do
	{
		x0 = x1;
		x1 = x1 - Function(x1) / dF(x1);
	} while (fabs(x1 - x0) > e);
	return x0;
}

int main()
{
	double a, b, h, e, x, q = 0;
	cout << "Input a, b, h, e: ";
	cin >> a >> b >> h;
	cin >> e;
	for (x = a; x <= b; x += h)  //Проходим по всему интервалу с маленьким шагом 
	{
		if (Function(x) * (Function(x + h)) < 0)  //условие простоого корня
		{
			q++;
			cout << "x" << q << " = " << Method_Newton(x, e) << endl; //Возвращает корень 
			cout << "Y(x) = " << Function(Method_Newton(x, e)) << endl;
		}
	}
}