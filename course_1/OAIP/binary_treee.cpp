#include<iostream>
#include<vector>
#include<algorithm>
#include <string>
#include <map>
using namespace std;

struct Node
{
	
	string inf;
	int key;
	Node* left;
	Node* right;

	Node(int key, string inf)
	{
		this->left = nullptr;
		this->right = nullptr;
		this->key = key;
		this->inf = inf;
	}

};

class Tree
{
private:
	Node* root;

	/*void print_private(Node* current, int tabs = 0) {
		if (!current) return;
		tabs += 5;
		print_private(current->left, tabs);
		for (int i = 0; i < tabs; i++) {
			cout << " ";
		}
		cout << current->key << endl;
		print_private(current->right, tabs);
		tabs -= 5;
		return;
	}*/

	void get_arr(vector<Node*>& arr_inf)
	{

		bool check = 1;
		int key;
		while (check)
		{
			bool check_revises = false;

			cout << "Введите ключ элемента: ";
			cin >> key;
			for (int i = 0; i < arr_inf.size(); i++)
			{
				if (arr_inf[i]->key == key)
				{
					cout << "Такой ключ уже есть. ";
					check_revises = true;
					break;
				}
			}
			if (check_revises == false) check = 0;
		}

		cout << "Введите значение элемента: ";
		string value;
		cin >> value;
		arr_inf.push_back(new Node(key, value));
		cout << "Добавить ли еще элемент?: 1. Да; 2. Нет: ";
		int choose;
		cin >> choose;
		if (choose == 1) get_arr(arr_inf);
	}

	void get_arr(Node* current, vector<pair<int, string>>& arr)
	{
		if (current->left != nullptr)
		{
			get_arr(current->left, arr);
			delete current->left;
		}
		if (current->right != nullptr)
		{
			get_arr(current->right, arr);
			delete current->right;
		}
		pair<int, string> p = make_pair(current->key, current->inf);
		arr.push_back(p);


	}

	void get_arr(Node* current, vector<int>& arr)
	{
		if (current->left != nullptr)
		{
			get_arr(current->left, arr);
		}
		if (current->right != nullptr)
		{
			get_arr(current->right, arr);
		}
		arr.push_back(current->key);
	}

	void balance_tree_1(Node*& current, int n, int k, vector<pair<int, string>> arr)
	{
		if (n == k)
		{
			current = nullptr;
			return;
		}
		else
		{
			int m = (n + k) / 2;
			current = new Node(arr[m].first, arr[m].second);
			balance_tree_1(current->left, n, m, arr);
			balance_tree_1(current->right, m + 1, k, arr);
		}
	}

	void find_element_private(int key, Node* current)
	{
		if (current == nullptr)
		{
			cout << "Значения с таким ключом нету."<<endl;
			return;
		}
		if (key == current->key)
		{
			cout << "Информация по заданному ключу: "<<current->inf<<endl;
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

		if (new_element->key > current->key)
		{
			new_element_private(new_element, current->right);
			return;
		}

		if (new_element->key < current->key)
		{
			new_element_private(new_element, current->left);
			return;
		}
	}

	void pre_order(Node* current)
	{
		if (current)
		{
			cout << "Ключ: " << current->key << " Значение: " << current->inf<<endl;
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

	void leaves_private(Node* current, int& a)
	{

		if (current!=nullptr && current->left == nullptr && current->right == nullptr) a++;

		if (current)
		{
			leaves_private(current->left, a);
			leaves_private(current->right, a);
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
		vector<Node*> arr_inf;
		get_arr(arr_inf);
		root = arr_inf[0];
		for (int i = 1; i<arr_inf.size(); i++)
		{
			Node* current = root;
			while (true)
			{
				if (current->key < arr_inf[i]->key && current->right != nullptr)
				{
					current = current->right;
				}
				else if (current->key < arr_inf[i]->key && current->right == nullptr)
				{
					current->right = arr_inf[i];
					break;
				}
				else if (current->key > arr_inf[i]->key && current->left != nullptr)
				{
					current = current->left;
				}
				else if (current->key > arr_inf[i]->key && current->left == nullptr)
				{
					current->left = arr_inf[i];
					break;
				}
			}

		}
	}

	void balance_tree_2()
	{
		Node* current=root;
		vector<pair<int, string>> arr;
		get_arr(current, arr);


		sort(arr.begin(), arr.end());
		balance_tree_1(current, 0, arr.size(), arr);

		root = current;

	}

	/*void print()
	{
		print_private(root);
	}*/

	void find_element()
	{
		cout << "Введите ключ элемента: ";
		int key;
		cin >> key;
		find_element_private(key, root);

	}

	void new_element()
	{
		vector<int> arr;
		get_arr(root, arr);
		int key;
		string value;

		while (true)
		{
			bool check = 1;
			cout << "Введите ключ нового элемента: ";
			cin >> key;
			for (int i=0; i<arr.size(); i++)
			{
				if (key == arr[i])
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
		Node* new_element = new Node(key, value);
		new_element_private(new_element, root);
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

	void leaves()
	{
		int a = 0;
		leaves_private(root, a);
		cout << "Количество листьев: " << a << endl;
	}

	void del_element()
	{
		int key;
		while (true)
		{
			cout << "Введите ключ элемента, которого хотите удалить: ";
			cin >> key;
			vector<int> arr;
			get_arr(root, arr);
			if (find(arr.begin(), arr.end(), key) != arr.end()) break;
			else
			{
				cout << "Такого элемета нету. ";
				continue;
			}

			
		}

		if (key != root->key) del_element_private(root, key);
		else del_root_element(root);
		
	}
};

int main()
{
	setlocale(LC_ALL, "rus");
	Tree a;
	a.build_tree(); //Создание дерева
	while (true)
	{
		cout << "1. Балансировка дерева; 2. По заданному ключу найти информацию и отобразить её; 3. Добавить в дерево поиска новую запись; 4. Удалить из дерева поиска информацию с заданным ключем; 5. Распечатать информацию; 6. Подсчитать количество листьев в дереве; 7. Закончить выполнение программы: ";
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
			a.leaves();
			break;
		case 7:
			return false;
			break;
		}
	}
	
}