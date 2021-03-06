
from py2neo import Graph,Node,Relationship,NodeMatcher

class Query():
    def __init__(self):
        self.graph=Graph("http://localhost:7474", username="neo4j",password="neo4j")

    def run(self,cql):
        # find_rela  = test_graph.run("match (n:Person{name:'张学友'})-[actedin]-(m:Movie) return m.title")
        result=[]
        find_rela = self.graph.run(cql,"")
        for i in find_rela:
            result.append(i.items()[0][1])
        return result




if __name__ == '__main__':
    SQL=Query()
    result=SQL.run("match (p:Place)-[]->() where p.title='径山寺' return p.type")
    print(result)