#include <iostream>
using namespace std;

class Queue
{
private:
	struct Node
	{
		int value;
		Node* next;
		Node* previous;

		Node(int value, Node* next, Node* previous)
		{
			this->value = value;
			this->next = next;
			this->previous = previous;
		}
	};
	Node* first=nullptr;
	Node* last=nullptr;

public:
	Queue()
	{
		cout << "Введите первый элемент очереди: ";
		int val;
		cin >> val;
		first = last =new Node(val, nullptr, nullptr);
	}

	bool first_last()
	{
		if (first == nullptr && last == nullptr) return 0;
		else return 1;
	}

	void add_left()
	{
		cout << "Введите значение нового правого узла: ";
		int val;
		cin >> val;
		if (first_last())
		{
			first = new Node(val, first, nullptr);
			first->next->previous = first;
		}
		else
		{
			first = last = new Node(val, nullptr, nullptr);
		}
	}

	void add_right()
	{
		cout << "Введите значение нового левого узла: ";
		int val;
		cin >> val;
		if (first_last())
		{
			last = new Node(val, nullptr, last);
			last->previous->next = last;
		}
		else
		{
			first = last = new Node(val, nullptr, nullptr);
		}
	}

	

	void view_left()
	{
		if (first_last())
		{
			Node* current = first;
			while (current != nullptr)
			{
				cout << current->value << ' ';
				current = current->next;
			}
			cout << endl;
		}
		else cout << "В списке нет ни одного элемента. " << endl;
	}

	void view_right()
	{
		if (first_last())
		{
			Node* current = last;
			while (current != nullptr)
			{
				cout << current->value << ' ';
				current = current->previous;
			}
			cout << endl;
		}
		else cout << "В списке нет ни одного элемента. " << endl;
	}

	void del_even()
	{
		first = new Node(1, first, nullptr);
		first->next->previous = first;
		Node* current = first;
		while (current->next != last)
		{
			if (current->next->value % 2 == 0)
			{
				Node* del = current->next;
				current->next = current->next->next;;
				current->next->previous = current;
				delete del;
			}
			else current = current->next;
		}

		if (last->value % 2 == 0)
		{
			Node* del = last;
			last->previous->next = nullptr;
			last = last->previous;
			delete del;
		}

		if (first != last)
		{
			Node* del = first;
			first = first->next;
			first->previous = nullptr;
			delete del;
		}

		else
		{
			Node* del = first;
			first = nullptr;
			last = nullptr;
			delete del;
		}
		

		
	}
	
};

void add(Queue& qe)
{
	cout << "Добвить элемент: 1. Спереди  2. Cзади: ";
	int choose;
	cin >> choose;
	switch (choose)
	{
	case 1:
		qe.add_left();
		break;
	case 2:
		qe.add_right();
		break;
	}
}

void view(Queue qe)
{
	cout << "1. Просмотреть с начала 2. Просмотреть с конца";
	int choose;
	cin >> choose;
	switch (choose)
	{
	case 1:
		qe.view_left();
		break;

	case 2:
		qe.view_right();
		break;
	}
}

int main()
{
	setlocale(LC_ALL, "rus");
	Queue qu;
	while (true)
	{
		cout << "1. Добавить узел 2. Просмотреть узел 3. Удалить узлы с четными значениями 4. Выйти из программы: ";
		int choose;
		cin >> choose;
		switch (choose)
		{
		case 1:
			add(qu);
			break;
		case 2:
			view(qu);
			break;
		case 3:
			qu.del_even();
			break;

		case 4:
			return 0;
			break;
		}
	}
	
}
