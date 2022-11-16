#include <iostream>
#include <string.h>
#include <sstream>

using namespace std;

int main() {
    setlocale(LC_ALL, "rus");
    char str[100];
    cin.getline(str, 100);
    int size = 0;

    while (true)
    {
        if (str[size] != '\0')
        {
            size++;
        }
        else break;
        
    }
    str[size]=' ';
    size++;

    int biggestLineSize = 0;
    string biggestLine = "";

    int currentLineSize = 0;
    string currentLine = "";

    for (int i = 0; i < size; i++)
    {
        if (str[i] != ' ')
        {
            biggestLineSize++;
        }
        else break;
        
    }
    
   

    for (int i = 0; i < size; i++) {
        if (str[i] != ' ') {
            currentLine += str[i];
            currentLineSize++;
        }
        else
        {
            if (currentLineSize <= biggestLineSize) {
                biggestLine = currentLine;
                biggestLineSize = currentLineSize;
            }
            currentLine = "";
            currentLineSize = 0;
        }
    }


    cout << "Наименьшая строка: " << biggestLine;
}

