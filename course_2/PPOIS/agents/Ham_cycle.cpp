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

using namespace std;
using namespace utils;




namespace exampleModule
{

    vector<ScAddr> get_adjacted_nodes(unique_ptr<ScMemoryContext>& ms_context, ScAddr current_node, ScLog* logger)
    {
        vector <ScAddr> adjacted_nodes = {};
        int vector_size = 0;
        ScIterator3Ptr adjacted_nodes_iterator = ms_context->Iterator3(current_node, ScType::EdgeDCommonConst, ScType::NodeConst);
        while (adjacted_nodes_iterator->Next())
        {
            adjacted_nodes.push_back(adjacted_nodes_iterator->Get(2));
            vector_size++;
        }


        //просто вывод-проверка смежных ребер
        /*
        logger->Message(ScLog::Type::Info, "check adj_nodes: ");
        for (int i=0; i<vector_size; i++)
        {
          ScAddr my_node=adjacted_nodes[i];
          ScIterator3Ptr nodeInfo=ms_context->Iterator3(my_node, ScType::EdgeDCommonConst, ScType::LinkConst);
          while(nodeInfo->Next())
          {
            logger->Message(ScLog::Type::Info, "Node" + CommonUtils::getLinkContent(ms_context.get(), nodeInfo->Get(2)));
          }
        }*/
    }

    bool find_hamiltonian_cycle(unique_ptr<ScMemoryContext>& ms_context, ScAddr current_node, ScAddr first_node, vector<ScAddr>& way, int32_t graph_size, int32_t current_size, ScLog* logger)
    {
        if (current_node == first_node && current_size == graph_size)
        {
            logger->Message(ScLog::Type::Info, "Hamiltonian cycle was found!!!");
            return true;
        }
        /*
        else if(current_node==first_node && current_size!=graph_size)
        {
          return false;
        }*/

        vector <ScAddr> adjacted_nodes = get_adjacted_nodes(ms_context, current_node, logger);



    }

    string GetStringNodeIdtf(unique_ptr<ScMemoryContext>& ms_context, ScAddr node)
    {

        ScIterator3Ptr it3 = ms_context->Iterator3(node, ScType::EdgeDCommonConst, ScType::LinkConst);
        while (it3->Next())
        {
            return CommonUtils::getLinkContent(ms_context.get(), it3->Get(2));
        }
        return CommonUtils::getLinkContent(ms_context.get(), it3->Get(2));
    }



    /*ScAddr get_first_node(unique_ptr<ScMemoryContext> &ms_context, ScAddr param)
    {
      ScAddr f_n;
      ScIterator3Ptr it_for_first_el= ms_context->Iterator3(param, ScType::EdgeAccessConstPosPerm, ScType::NodeConst);
      while(it_for_first_el->Next())
      {
        f_n=it_for_first_el->Get(2);
        break;
      }
      return f_n;
    }*/

    SC_AGENT_IMPLEMENTATION(CourseWorkAgent)
    {
        //Main nodes and tmpSize initialization 
        ScLog* logger = ScLog::GetInstance(); //объ€вление переменной выводы в консоль
        ScAddr questionNode = ms_context->GetEdgeTarget(edgeAddr); //цель дуги, котора€ проведена
        ScAddr param = IteratorUtils::getAnyFromSet(ms_context.get(), questionNode); //присваеваетс€ наш узел с графом
        ScAddr answer = ms_context->CreateNode(ScType::NodeConstStruct); //
        ScAddr res_str = ms_context->CreateLink(ScType::LinkVar);
        ms_context->CreateEdge(ScType::EdgeAccessConstPosPerm, answer, res_str);
        ScAddr visited = ms_context->CreateNode(ScType::NodeConstClass); //посещенные
        ScAddr globalVisited = ms_context->CreateNode(ScType::NodeConstClass); //полностью посещенные




        /*
        ScAddr size_of_graph = ms_context->CreateNode(ScType::LinkVar);
        auto strTmp = CommonUtils::getLinkContent(ms_context.get(), it3->Get(2)); //получить инфу с линки
        ms_context->SetLinkContent(res, to_string(tmp)); записать инфу в линку

        */


        if (!param.IsValid()) //проверка на валидность
            return SC_RESULT_ERROR_INVALID_PARAMS;


        int32_t graph_size = 0; //размер графа
        vector <ScAddr> vector_of_nodes;
        ScIterator3Ptr iter_for_size = ms_context->Iterator3(param, ScType::EdgeAccessConstPosPerm, ScType::NodeConst);

        while (iter_for_size->Next())
        {
            graph_size = graph_size + 1;
            ScAddr current_node = iter_for_size->Get(2);
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



        // ScAddr f_n;
        // ScIterator3Ptr it_for_first_el= ms_context->Iterator3(param, ScType::EdgeAccessConstPosPerm, ScType::NodeConst);
        // while(it_for_first_el->Next())
        // {
        //   f_n=it_for_first_el->Get(2);
        //   break;
        // }

        //ScAddr first_node=get_first_node(ms_context, param);

        ScIterator3Ptr first_inf = ms_context->Iterator3(vector_of_nodes[0], ScType::EdgeDCommonConst, ScType::LinkConst);
        while (first_inf->Next())
        {
            logger->Message(ScLog::Type::Info, "first_element: " + CommonUtils::getLinkContent(ms_context.get(), first_inf->Get(2)));
        }

        vector <ScAddr> cycle = {};

        find_hamiltonian_cycle(ms_context, vector_of_nodes[0], vector_of_nodes[0], cycle, graph_size, 5, logger);


        utils::AgentUtils::finishAgentWork(ms_context.get(), questionNode, answer);//соедин€ет пустой узел и получает ответ;
        return SC_RESULT_OK;
    }
}

