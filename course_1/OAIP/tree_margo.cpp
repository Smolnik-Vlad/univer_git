#include <iostream>
#include <algorithm>
#include <string>
using namespace std;

struct Node
{

	string inf;
	int key;
	Node* left;
	Node* right;
};

struct Tree
{
private:
	Node* root;
	int size;
	void get_arr(Node** arr, int a)
	{
		for (int i = 0; i < a; i++)
		{
			int key;
			string value;
			
			while (true)
			{
				bool check = true;
				cout << "Введите ключ элемента: ";
				cin >> key;
				for (int j = 0; j < i; j++)
				{
					if (key == arr[j]->key)
					{
						cout << "Такой ключ уже есть. ";
						check = false;
						break;
					}
				}
				if (check) break;
			}
			
			cout << "Введите значение: ";
			cin >> value;
			arr[i]->key = key;
			arr[i]->inf = value;
			arr[i]->left = NULL;
			arr[i]->right = NULL;
		}
	}
	void get_ballance_arr(Node** arr, Node* current, int& a)
	{
		if (current->left != nullptr)
		{
			get_ballance_arr(arr, current->left, a);
		}
		if (current->right != nullptr)
		{
			get_ballance_arr(arr, current->right, a);
		}

		arr[a] = current;
		a++;
	}
	void sort_arr(Node** arr)
	{
		for (int i = 0; i < size-1; i++)
		{
			for (int j = i + 1; j < size; j++)
			{
				if (arr[i]->key > arr[j]->key)
				{
					Node* change = arr[i];
					arr[i] = arr[j];
					arr[j] = change;
				}
			}
		}
	}
	bool check_el(Node** arr, int key)
	{
		for (int i = 0; i < size; i++)
		{
			if (arr[i]->key == key)
				return true;
		}
		return false;
	}

	void pre_order(Node* current)
	{
		if (current)
		{
			cout << "Ключ: " << current->key << " Значение: " << current->inf << endl;
			pre_order(current->left);
			pre_order(current->right);
		}
	}
	void post_order(Node* current)
	{
		if (current)
		{
			post_order(current->left);
			post_order(current->right);
			cout << "Ключ: " << current->key << " Значение: " << current->inf << endl;
		}
	}
	void in_order(Node* current)
	{
		if (current)
		{
			in_order(current->left);
			cout << "Ключ: " << current->key << " Значение: " << current->inf << endl;
			in_order(current->right);
		}
	}

	void balance_tree_1(Node** arr, Node* &current, int n, int k)
	{

		if (n == k)
		{
			current = nullptr;
			return;
		}
		else
		{
			int m = (n + k) / 2;
			current = arr[m];
			balance_tree_1(arr, current->left, n, m);
			balance_tree_1(arr, current->right, m + 1, k);
		}
	}

	void find_element_private(int key, Node* current)
	{
		if (current == nullptr)
		{
			cout << "Значения с таким ключом нету." << endl;
			return;
		}
		if (key == current->key)
		{
			cout << "Информация по заданному ключу: " << current->inf << endl;
			return;
		}
		if (key > current->key)
		{
			find_element_private(key, current->right);
			return;
		}
		if (key < current->key)
		{
			find_element_private(key, current->left);
			return;
		}
	}

	void new_element_private(Node* new_element, Node*& current)
	{
		if (current == nullptr)
		{
			current = new_element;
			return;
		}

		if (new_element->key > current->key)   //Проход правее ьекущего ключа
		{
			new_element_private(new_element, current->right);
			return;
		}

		if (new_element->key < current->key) //Проход левее текущего ключа
		{
			new_element_private(new_element, current->left);
			return;
		}
	}

	void del_element_private(Node*& root, int key)
	{
		Node* current = root;
		Node* prev = nullptr;
		int l_r;

		while (current->key != key)
		{
			prev = current;
			if (current->key > key)
			{
				l_r = 0;
				current = current->left;
			}
			else if (current->key < key)
			{
				l_r = 1;
				current = current->right;
			}
		}
		if (current->left == nullptr && current->right == nullptr)
		{
			switch (l_r)
			{
			case 0:
				prev->left = nullptr;
				break;
			case 1:
				prev->right = nullptr;
				break;
			}
			delete current;
		}
		else if (current->left == nullptr && current->right != nullptr)
		{
			switch (l_r)
			{
			case 0:
				prev->left = current->right;
				break;
			case 1:
				prev->right = current->right;
				break;
			}
			delete current;
		}

		else if (current->right == nullptr && current->left != nullptr)
		{
			switch (l_r)
			{
			case 0:
				prev->left = current->left;
				break;
			case 1:
				prev->right = current->left;
				break;
			}
			delete current;
		}


		else if (current->left != nullptr && current->right != nullptr)
		{
			Node* replace = current->left;
			Node* rep_prev = current;
			while (replace->right != nullptr)
			{
				rep_prev = replace;
				replace = replace->right; //Еще провериить, чтобы это не был следующим элементом
			}

			if (rep_prev != current)
			{
				rep_prev->right = replace->left;
				switch (l_r)
				{
				case 0:
					prev->left = replace;
					break;
				case 1:
					prev->right = replace;
					break;
				}
				replace->left = current->left;
				replace->right = current->right;
				delete current;
			}
			else
			{
				switch (l_r)
				{
				case 0:
					prev->left = replace;
					break;
				case 1:
					prev->right = replace;
					break;
				}
				replace->right = current->right;
				delete current;
			}
		}
	}
	void del_root_element(Node*& root)
	{
		if (root->left == nullptr && root->right == nullptr)
		{
			Node* del = root;
			this->root = nullptr;
			delete del;
		}

		else if (root->left == nullptr && root->right != nullptr)
		{
			Node* del = root;
			this->root = root->right;
			delete del;
		}

		else if (root->left != nullptr && root->right == nullptr)
		{
			Node* del = root;
			this->root = root->left;
			delete del;
		}

		else if (root->left != nullptr && root->right != nullptr)
		{
			Node* replace = root->left;
			Node* rep_prev = root;
			Node* del = root;
			while (replace->right != nullptr)
			{
				rep_prev = replace;
				replace = replace->right;
			}

			if (rep_prev != root)
			{
				rep_prev->right = replace->left;
				root = replace;
				root->left = del->left;
				root->right = del->right;
				delete del;

			}
			else
			{
				root = replace;
				root->right = del->right;
				delete del;
			}
		}
	}


	

public:

	void build_tree()
	{
		cout << "Введите размер массива с элементами: ";
		int a;
		cin >> a;
		size = a;
		Node** arr = new Node*[a];
		for (int i = 0; i < a; i++)
		{
			arr[i] = new Node;
		}

		get_arr(arr, a);
		root = arr[0];
		for (int i = 1; i <a; i++)
		{
			Node* current = root;
			while (true)
			{
				if (current->key < arr[i]->key && current->right != nullptr)
				{
					current = current->right;
				}
				else if (current->key < arr[i]->key && current->right == nullptr)
				{
					current->right = arr[i];
					break;
				}
				else if (current->key > arr[i]->key && current->left != nullptr)
				{
					current = current->left;
				}
				else if (current->key > arr[i]->key && current->left == nullptr)
				{
					current->left = arr[i];
					break;
				}
			}

		}

		delete[]arr;
	}

	void print_inf()
	{
		cout << "Как вы хотите вывести информацию?: 1. прямым ходом; 2. обратным ходом; 3. В порядке возрастания ключа?: ";
		int choose;
		cin >> choose;
		switch (choose)
		{
		case 1:
			pre_order(root);
			break;

		case 2:
			post_order(root);
			break;

		case 3:
			in_order(root);
			break;

		}
	}

	void balance_tree_2()
	{
		Node* current = root;
		Node** arr = new Node * [size];
		int a = 0;
		for (int i = 0; i < size; i++)
		{
			arr[i] = new Node;
		}
		get_ballance_arr(arr, current, a);


		sort_arr(arr);
		balance_tree_1(arr, current, 0, size);

		root = current;

		
		delete[]arr;
	}

	void find_element()
	{
		cout << "Введите ключ элемента: ";
		int key;
		cin >> key;
		find_element_private(key, root);

	}

	void new_element()
	{
		Node** arr = new Node*[size];
		int a = 0;
		get_ballance_arr(arr, root, a);
		int key;
		string value;

		while (true)
		{
			bool check = 1;
			cout << "Введите ключ нового элемента: ";
			cin >> key;
			for (int i = 0; i < size; i++)
			{
				if (key == arr[i]->key)
				{
					cout << "Такой ключ уже есть. ";
					check = 0;
					break;
				}
			}
			if (check == 1) break;
		}

		cout << "Введите значение нового элемента: ";
		cin >> value;
		Node* new_element = new Node;
		new_element->key = key;
		new_element->inf = value;
		new_element->left = nullptr;
		new_element->right = nullptr;
		new_element_private(new_element, root);
		size++;
		delete []arr;
	}

	void del_element()
	{
		int key;
		Node** arr = new Node * [size];
		while (true)
		{
			cout << "Введите ключ элемента, которого хотите удалить: ";
			cin >> key;
			
			int a = 0;
			get_ballance_arr(arr, root, a);

			if (check_el(arr, key)) break;
			else
			{
				cout << "Такого элемета нету. ";
				continue;
			}


		}

		if (key != root->key) del_element_private(root, key);
		else del_root_element(root);
		size--;
		delete[]arr;
	}

};

int main()
{
	setlocale(LC_ALL, "rus");
	Tree a;
	a.build_tree();
	while (true)
	{
		cout << "1. Балансировка дерева; 2. По заданному ключу найти информацию и отобразить её; 3. Добавить в дерево поиска новую запись; 4. Удалить из дерева поиска информацию с заданным ключем; 5. Распечатать информацию; 6. свой варик; 7. Закончить выполнение программы: ";
		int choose;
		cin >> choose;
		switch (choose)
		{
		case 1:
			a.balance_tree_2();
			break;
		case 2:
			a.find_element();
			break;
		case 3:
			a.new_element();
			break;
		case 4:
			a.del_element();
			break;
		case 5:
			a.print_inf();
			break;
		case 6:

			break;
		case 7:
			return false;
			break;
		}
	}

}
