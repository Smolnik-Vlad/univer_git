#include <iostream>
#include <ctime>
using namespace std;

template<typename T>
class List
{
private:

	template <typename T>
	struct Node		//структура, храняшая данные и указатель на следующий узедл
	{
	public:
		Node *pNext;
		T data;

		Node(T data = NULL, Node* pNext = nullptr)
		{
			this->data = data;
			this->pNext = pNext;
		}
	}; 

	int Size;
	Node<T> *head;


public:
	List()
	{
		Size = 0;
		head = nullptr; //Так как нету ни одного элемента, head тоже нету, но мы его объявляем при создании самой структуры
	};

	void push_back(T data)			//Функция добавления нового узла
	{
		if (head == nullptr)		//Если это самый первый узел
		{
			head = new Node<T>(data); //Создаем самый первый узел, head - указатель на него
			/*last = head; //кусок второго варианта*/ 
		}
		else
		{
			Node<T>* current = this->head;  //временный указатель, который будет меняться, пока не будет укзывать на последний узел, изначально указывает на самый первый элемент
			while(current->pNext!=nullptr) //поскольку последний узел не имеет указатель на слежующий узел, то current будет брать pNext со следующего узла, пока тот не станет последним 
			{
				current = current->pNext; //current принимает указатель на следующий узел
			}
			current->pNext = new Node<T>(data); //создаем новый узел и запихиваем его адрес в указатель pNext предыдущего узла


			/*last = (last->pNext = new Node<T>(data)); //Вторрой вариант добавления нового узла, заключается в том, что он сразу хранит указатель на последний узел*/
		
		}
		Size++;
		
		
	};

	int size() { return Size; }; //функция вывода размера списка

	T& operator[](const int index) //функция для вывода любого элемента 
	{
		Node<T>* current = this->head;  //создаем временный указатель, указывающий на самый первый узел
		for (int i = 0; i < index; i++)
		{
			current = current->pNext; //временный указатель принимает адрес следующего узла
		}
		return current->data;
	}

	void all_inf()
	{
		for (Node<T>* current = this->head; current != nullptr; current = current->pNext)
		{
			cout << current->data << ' ';
		}
	}

	void reset(const int index)
	{
		Node <T>* current = this->head;
		Node<T>* del;
		if (index == 0)
		{
			del = head;
			head = current->pNext;
			delete[] del;
		}
		else
		{
			for (int i = 0; i < index - 1; i++)
			{
				current = current->pNext;
			}
			del = current->pNext;
			current->pNext = current->pNext->pNext;
			delete[] del;
		}
		Size--;
		
	}

	void reset_even()
	{
		Node <T>* current = this->head;
		Node<T>* del;
		while (current->pNext!=nullptr)
		{
			if (current->data % 2 == 0)
			{
				del = current;
				current = current->pNext;
				delete[] del;
				Size--;
			}
			else
			{
				current = current->pNext;
			}
		}
		if (current->data % 2 == 0)
		{
			current = nullptr;
			Size--;
		}
	}

	void sort_value()
	{
		Node <T>* current_1 = this->head;
		for (current_1; current_1->pNext->pNext != nullptr; current_1 = current_1->pNext)
		{
			for (Node <T>* current_2 = current_1; current_2->pNext != nullptr; current_2 = current_2->pNext)
			{
				if (current_1->data > current_2->data)
				{
					swap(current_1->data, current_2->data);
				}
			}
		}
	}

	void sort()
	{
		Node <T>* current_1 = this->head;
		for (current_1; current_1->pNext->pNext != nullptr; current_1 = current_1->pNext)
		{
			for (Node <T>* current_2 = current_1->pNext; current_2->pNext!= nullptr; current_2 = current_2->pNext)
			{
				if (current_1->data > current_2->data)
				{
					Node <T>* change_1 = current_1->pNext;
					current_1->pNext = current_2->pNext;
					current_2->pNext = change_1;
					Node<T>* change_2 = current_1;
					current_1 = current_2;
					current_2 = change_2;
				}
			}
		}
	}
};

void push_back_f(List<int> &lst)
{
	lst.push_back(-1000+rand() % 2001);
}

void size_f(List<int>& lst)
{
	cout << "Размер списка: "<<lst.size()<<endl;
}

void get_inf_f(List<int>& lst)
{
	int choose;
	cout << "Введите номер узла, значение которого хотите узнать: ";
	cin >> choose;
	cout <<"Значение узла: "<< lst[choose]<<endl;
}

void reset_f(List<int>& lst)
{
	cout << "Введите номер узла, которого вы хотите удалить: ";
	int choose;
	cin >> choose;
	lst.reset(choose);
}

void reset_even_f(List<int>& lst)
{
	lst.reset_even();
}

void sorts_f(List<int> lst)
{
	int choose;
	cout << "Как вы хотите сортировать список? 1. Значения списка. 2. Узлы списка";
	cin >> choose;
	switch (choose)
	{
	case 1:
		lst.sort_value();
		break;
	case 2:
		lst.sort();
		break;
	}
	
};

void all_inf_f(List<int> lst)
{
	lst.all_inf();
	cout << endl;
}


int main()
{
	setlocale(LC_ALL, "rus");
	srand(time(NULL));
	List<int> lst;
	int choose;
	bool check=1;
	
	while (check)
	{
		cout << "1. Добавить узел списка.  2. Узнать размер списка.  3. Узнать n-ый элемент списка.  4. Удалить n-ый узел списка.  5. Удалить узел списка с четными значениями.  6 Сортировки.  7. Выйти из программы. 8. Вывести все элементы списка: ";

		cin >> choose;
		switch (choose)
		{
		case 1:
			push_back_f(lst);
			break;
		case 2:
			size_f(lst);
			break;
		case 3:
			get_inf_f(lst);
			break;
		case 4:
			reset_f(lst);
			break;
		case 5:
			reset_even_f(lst);
			break;
		case 6:
			sorts_f(lst);
			break;
		case 7:
			check = !check;
			break;
		case 8:
			all_inf_f(lst);
			break;
		}
		
	}
	
}

