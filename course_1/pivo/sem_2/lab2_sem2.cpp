#include <iostream>
#include <vector>
#include<fstream>
#include <list>
#include <ctime>
using namespace std;

struct Edge  //ребра
{
	int from_number;
	int to_number; // в какой узел
	int flow; //Поток

	bool operator == (const Edge& Other) const {   //Это что такое???
		return
			from_number == Other.from_number &&
			to_number == Other.to_number;
	}

	Edge(int from_number, int to_number, int flow)
	{
		this->from_number = from_number;
		this->to_number = to_number;
		this->flow = flow;
	}

	Edge() {};
};

struct Node  //узлы
{
	int number; //номер узла
	vector<Edge*> adjanced; //вектор смежных ребер 

	Node(int number, vector<Edge*> adjanced)
	{
		this->number = number;
		this->adjanced = adjanced;
	}
};

int get_inf(vector<Node*>& Graph)
{
	int get_size;
	ifstream file("party.in");
	int numbs_of_cows, max_dish, numbs_of_dish; //количество коров, максимальное количество блюд, количество различных типов блюд
	file >> numbs_of_cows >> max_dish >> numbs_of_dish;


	vector<int> numbs_of_different_dish(numbs_of_dish); //максимальное количество блюда определенного типа
	for (int i = 0; i < numbs_of_dish; i++)
	{
		file >> numbs_of_different_dish[i];
	}

	vector<vector<int>> cows_and_dishes;

	for (int i = 0; i < numbs_of_cows; i++) //бюлюда и коровы
	{
		file >> get_size;
		vector<int> current_cow_and_dish(get_size);
		for (int i = 0; i < get_size; i++)
		{
			file >> current_cow_and_dish[i];
		}
		cows_and_dishes.push_back(current_cow_and_dish);
	}


	//Заполняем список инцидентности
	vector<Edge*> adjanced; //вектор с ребрами между узлами

	for (int i = 1; i < numbs_of_cows + 1; i++) //От истока к коровам
	{
		Edge* cows = new Edge(0, i, max_dish);
		adjanced.push_back(cows);
	}
	Node* istock = new Node(0, adjanced);
	Graph.push_back(istock);
	adjanced = {};
	adjanced.resize(0);

	for (int i = 0; i < cows_and_dishes.size(); i++)  //от коров к блюдам
	{
		for (int j = 0; j < cows_and_dishes[i].size(); j++)
		{
			Edge* dish_and_cow = new Edge(i + 1, cows_and_dishes[i][j] + numbs_of_cows, 1);
			adjanced.push_back(dish_and_cow);
		}
		Node* cow = new Node(i + 1, adjanced);
		Graph.push_back(cow);
		adjanced = {};
		adjanced.resize(0);
	}


	for (int i = 0; i < numbs_of_dish; i++)
	{

		Edge* dishes = new Edge(numbs_of_cows + i + 1, numbs_of_cows + numbs_of_dish + 1, numbs_of_different_dish[i]);
		adjanced.push_back(dishes);

		Node* dish = new Node(i + numbs_of_cows + 1, adjanced);
		Graph.push_back(dish);

		adjanced = {};
		adjanced.resize(0);
	}

	Node* last = new Node(numbs_of_cows + numbs_of_dish + 1, {});
	Graph.push_back(last);
	return last->number;

}

bool dfs(vector<Node*>& Graph /*Вектор узлов*/, int src/*Начальный элемент*/, int dst/*Конечный элемент*/, list<Edge*>& path /*Пройденный путь по ребрам*/, list<int>& visited /*посещенные узлы*/)  //поиск в глубину (на вход идет вектор графов, элемент, с которого идет поиск, конечный элемент, список пути, список посещенных элементов)
{
	if (src == dst) return true; //проверка на совпадение начальной и конечной вершины (путь найден), если уже они встретились то пойдет все рекурсивно просто заебись как 

	if (find(visited.begin(), visited.end(), src) != visited.end()) return false; //Поскольку все делатся рекурсивно, то возврат к пройденной вершине обознаает тупик, поэтому исключаем данное ребро

	vector<Edge*>& adjacent = Graph[src]->adjanced; //берем вектор смежных ребер данному узлу
	for (Edge* edge : adjacent) //пробегая по каждому ребру из вектора ребер данного узла
	{
		if (edge->flow <= 0) continue; //Проверяем остаточную пропускную способность, если она не соответствует условию, переходим к следующему элементу
		visited.push_back(src); //добавляем посещенный узел (в цикле, поскольку используется рекурсия и он больше не добавится)
		if (dfs(Graph, edge->to_number, dst, path, visited)) //вызываем рекурсию и провераяем
		{
			path.push_front(edge); //добавляем ребро (его указатель) в путь
			return true;
		}
	}
	return false; //последний выход


}


bool try_get_edge(vector<Node*>& graph, int src, int dst, Edge* OutEdge) //напишем функцию поиска дуги в графе по двум вершинам
{
	vector<Edge*> adjacent = graph[src]->adjanced;
	for (Edge* edge : adjacent)
	{
		if (edge->to_number == dst) {
			OutEdge = edge;
			return true;
		}

	}
	return false;
}

Edge* vector_find_or_add(vector<Edge*>& vector, Edge* edgeToFind) {
	for (Edge* edge : vector) {

		if (edge == edgeToFind) {
			return edge;
		}
	}



	vector.push_back(edgeToFind);
	return *(vector.end() - 1);
}

int ford_fulkerson(vector<Node*>& Graph, int src, int dst)
{

	int resultFlow = 0;

	while (true)
	{
		list<Edge*> path = {};
		list<int> visited = {};
		if (!dfs(Graph, src, dst, path, visited)) break;

		int minFlow = (*path.begin())->flow;

		for (Edge* edge : path) {

			if (minFlow > edge->flow)
			{
				minFlow = edge->flow;
			}
		}

		for (Edge* edge : path) {
			edge->flow -= minFlow;
			const int currentNodeIndex = edge->from_number;
			const int connectedNodeIndex = edge->to_number;
			Node* connectedNode = Graph[edge->to_number];
			Edge* BackwardsEdge = vector_find_or_add(connectedNode->adjanced, new Edge(connectedNodeIndex, currentNodeIndex, 0));
			BackwardsEdge->flow += minFlow;
		}

		resultFlow += minFlow;
	}

	return resultFlow;
}

int main()
{
	vector<Node*> Graph;
	int last;
	last = get_inf(Graph);
	int result = ford_fulkerson(Graph, 0, last);
	ofstream file("party.out");
	file << result;
	file.close();
}




