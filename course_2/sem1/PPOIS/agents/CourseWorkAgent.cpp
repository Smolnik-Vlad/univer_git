#include <sc-memory/sc_memory.hpp>
#include <sc-memory/sc_link.hpp>
#include <sc-memory/sc_common_templ.hpp>

#include <sc-agents-common/utils/GenerationUtils.hpp>
#include <sc-agents-common/utils/AgentUtils.hpp>
#include <sc-agents-common/utils/IteratorUtils.hpp>
#include <sc-agents-common/utils/CommonUtils.hpp>

#include <sc-memory/kpm/sc_agent.hpp>

#include "CourseWorkAgent.hpp"
#include <map>
#include <vector>

#include <algorithm>

using namespace std;
using namespace utils;




namespace exampleModule
{

vector<ScAddr> get_adjacted_nodes(unique_ptr<ScMemoryContext> &ms_context, ScAddr current_node, ScLog *logger)
{
  vector <ScAddr> adjacted_nodes={};

  ScIterator3Ptr adjacted_nodes_iterator = ms_context->Iterator3(current_node, ScType::EdgeDCommonConst, ScType::NodeConst);
  while(adjacted_nodes_iterator->Next())
  {
    ScAddr adjacted_node = adjacted_nodes_iterator->Get(2);

    adjacted_nodes.push_back(adjacted_node);
  }

    
  return adjacted_nodes;
}

bool find_hamiltonian_cycle(unique_ptr<ScMemoryContext> &ms_context, ScAddr current_node, ScAddr first_node, vector<ScAddr> way, vector<ScAddr> &cycle, int32_t graph_size, int32_t current_size, ScLog *logger)
{

   ScIterator3Ptr nodeInfo = ms_context->Iterator3(current_node, ScType::EdgeDCommonConst, ScType::LinkConst);

  //проверка намсхожесть с первым элементом
  if(current_node==first_node && current_size==graph_size)
  {
    logger->Message(ScLog::Type::Info, "Hamiltonian cycle was found!!!");
    way.push_back(current_node);

    cycle = way;
    return true;
  }
  //проверка, чтобы данного элемента не было в списке
  if (find(way.begin(), way.end(), current_node)!=way.end()) return false;

  //добавляем вершину в путь
  way.push_back(current_node);
  current_size++;

  vector <ScAddr> adjacted_nodes=get_adjacted_nodes(ms_context, current_node, logger);

  

  for (int i=0; i<adjacted_nodes.size(); i++)
  {
    if(find_hamiltonian_cycle(ms_context, adjacted_nodes[i], first_node, way, cycle, graph_size, current_size, logger)) return true;
    
    //else logger->Message(ScLog::Type::Info, "Next node");
  }
  //logger->Message(ScLog::Type::Info, "Go out");
  return false;
  

}

string GetStringNodeIdtf(unique_ptr<ScMemoryContext> &ms_context, ScAddr node)
{
 
 ScIterator3Ptr it3 = ms_context->Iterator3(node, ScType::EdgeDCommonConst, ScType::LinkConst);
 while(it3->Next())
 {
  return CommonUtils::getLinkContent(ms_context.get(), it3->Get(2));
 }
 return CommonUtils::getLinkContent(ms_context.get(), it3->Get(2));
}


SC_AGENT_IMPLEMENTATION(CourseWorkAgent)
{
  //Main nodes and tmpSize initialization 
  ScLog *logger = ScLog::GetInstance(); //объявление переменной выводы в консоль
  ScAddr questionNode = ms_context->GetEdgeTarget(edgeAddr); //цель дуги, которая проведена
  ScAddr param = IteratorUtils::getAnyFromSet(ms_context.get(), questionNode); //присваевается наш узел с графом
  ScAddr answer = ms_context->CreateNode(ScType::NodeConstStruct); //
  ScAddr res_str = ms_context->CreateLink(ScType::LinkVar);
  ms_context->CreateEdge(ScType::EdgeAccessConstPosPerm, answer, res_str);
  ScAddr visited = ms_context->CreateNode(ScType::NodeConstClass); //посещенные
  ScAddr globalVisited = ms_context->CreateNode(ScType::NodeConstClass); //полностью посещенные
  
  

  if (!param.IsValid()) //проверка на валидность
  return SC_RESULT_ERROR_INVALID_PARAMS;


  int32_t graph_size = 0; //размер графа
  vector <ScAddr> vector_of_nodes;
  ScIterator3Ptr iter_for_size = ms_context->Iterator3(param, ScType::EdgeAccessConstPosPerm, ScType::NodeConst);

   while(iter_for_size->Next())
   {
     graph_size=graph_size+1;
     ScAddr current_node=iter_for_size->Get(2);
     vector_of_nodes.push_back(current_node);

    //все что ниже - вывод названий вершин
    //------------------------------------------
    // ScIterator3Ptr nodeInfo=ms_context->Iterator3(current_node, ScType::EdgeDCommonConst, ScType::LinkConst);
    // while(nodeInfo->Next())
    // {
    //   logger->Message(ScLog::Type::Info, CommonUtils::getLinkContent(ms_context.get(), nodeInfo->Get(2)));
    // }
    //----------------------------------------------
   }




  
  ScIterator3Ptr first_inf = ms_context->Iterator3(vector_of_nodes[0], ScType::EdgeDCommonConst, ScType::LinkConst);

  
    vector <ScAddr> path={};
    vector <ScAddr> cycle = {};

    if(!find_hamiltonian_cycle(ms_context, vector_of_nodes[0], vector_of_nodes[0], path, cycle, graph_size, 0, logger))
    {
      logger->Message(ScLog::Type::Info, "Hamiltonian cycle wasn't found");
    }

    else
    {
      for (int i=0; i<cycle.size()-1; i++)
      {
        ScIterator3Ptr nodeInfo = ms_context->Iterator3(cycle[i], ScType::EdgeDCommonConst, ScType::LinkConst);
        while(nodeInfo->Next())
        {
            logger->Message(ScLog::Type::Info, CommonUtils::getLinkContent(ms_context.get(), nodeInfo->Get(2)) + "->");
        }
        
      }
      ScIterator3Ptr nodeInfo = ms_context->Iterator3(cycle[cycle.size()-1], ScType::EdgeDCommonConst, ScType::LinkConst);
        while(nodeInfo->Next())
        {
            logger->Message(ScLog::Type::Info, CommonUtils::getLinkContent(ms_context.get(), nodeInfo->Get(2)));
        }
    }


  utils::AgentUtils::finishAgentWork(ms_context.get(), questionNode, answer);//соединяет пустой узел и получает ответ;
  return SC_RESULT_OK;
}
}

