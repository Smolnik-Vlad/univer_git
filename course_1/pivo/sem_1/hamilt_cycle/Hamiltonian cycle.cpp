
#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
using namespace std;

int** get_info(int& nodes, int& edges)   //(ребра и вершины)
{
	ifstream fileo;
	fileo.open("input.txt");
	fileo >> nodes >> edges;

	int** inc_matrix = new int* [nodes];
	for (int i = 0; i < nodes; i++)
	{
		inc_matrix[i] = new int[edges];
	}

	for (int i = 0; i < nodes; i++)
	{
		for (int j = 0; j < edges; j++)
		{
			fileo >> inc_matrix[i][j];
		}
	}
	fileo.close();
	return inc_matrix;
}

bool cycle_find(int** matrix, int nodes, int edges, int step, vector<int> way, int vertex, vector<int>& result)
{
	way.push_back(vertex); //добавление текущего элемента в цикл
	if (step == nodes - 1) //Гамильтонов цикл - это такой цикл, в котором проходт по каждой вершине, поэтому шагов будет столько же, сколько и вершин, но так как мы начинаем с шага = 0, то и последний шаг на один меньше
	{
		result = way;
		result.push_back(way[0]); //добавляем первый элемент для образования цепи
		for (int i = 0; i < edges; i++) {
			if (matrix[way[0]][i] != 0 && matrix[vertex][i] != 0)
			{
				return true;
			}
		}

		return false;

	}

	vector<int> child_vertex;
	for (int i = 0; i < edges; i++)
	{
		if (matrix[vertex][i] != 0)
		{
			for (int j = 0; j < nodes; j++)
			{
				if (j != vertex && matrix[j][i] != 0 && find(way.begin(), way.end(), j) == way.end())
				{
					child_vertex.push_back(j);
					break;
				}
			}
		}
	}

	for (int i = 0; i < child_vertex.size(); i++)
	{
		bool success = cycle_find(matrix, nodes, edges, step + 1, way, child_vertex[i], result);
		if (success == 1)
		{
			return (1);
		}
	}
	return false;

};


int main()
{
	int edges, nodes;
	int** inc_matrix = get_info(nodes, edges);


	vector<int> result;
	if (cycle_find(inc_matrix, nodes, edges, 0, vector<int>(), 0, result))
	{
		for (int i = 0; i < result.size(); i++)
		{
			cout << result[i];
			if (i != result.size() - 1) {
				cout << "->";
			}
		}
	}
	else cout << "Fu*k";

	for (int i = 0; i < nodes; i++) {
		delete[] inc_matrix[i];
	}

	delete[] inc_matrix;
}
