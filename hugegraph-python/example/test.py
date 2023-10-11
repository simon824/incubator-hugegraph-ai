from src.connection import PyHugeClient

if __name__ == '__main__':
    client = PyHugeClient("127.0.0.1", "8080", user="admin", pwd="admin", graph="test")

    """schema"""
    schema = client.schema()
    schema.propertyKey("name").asText().ifNotExist().create()
    schema.propertyKey("birthDate").asText().ifNotExist().create()
    schema.vertexLabel("Person").properties("name", "birthDate").usePrimaryKeyId().primaryKeys(
        "name").ifNotExist().create()
    schema.vertexLabel("Movie").properties("name").usePrimaryKeyId().primaryKeys("name").ifNotExist().create()
    schema.edgeLabel("ActedIn").sourceLabel("Person").targetLabel("Movie").ifNotExist().create()

    print(schema.getVertexLabels())
    print(schema.getEdgeLabels())
    print(schema.getRelations())

    """graph"""
    g = client.graph()
    # add Vertex
    p1 = g.addVertex("Person", {"name": "Al Pacino", "birthDate": "1940-04-25"})
    p2 = g.addVertex("Person", {"name": "Robert De Niro", "birthDate": "1943-08-17"})
    m1 = g.addVertex("Movie", {"name": "The Godfather"})
    m2 = g.addVertex("Movie", {"name": "The Godfather Part II"})
    m3 = g.addVertex("Movie", {"name": "The Godfather Coda The Death of Michael Corleone"})

    # add Edge
    g.addEdge("ActedIn", p1.id, m1.id, {})
    g.addEdge("ActedIn", p1.id, m2.id, {})
    g.addEdge("ActedIn", p1.id, m3.id, {})
    g.addEdge("ActedIn", p2.id, m2.id, {})

    # update property
    g.eliminateVertex("vertex_id", {"property_key": "property_value"})


    print(g.getVertexById(p1.id).label)
    # g.removeVertexById("12:Al Pacino")
    g.close()

    """gremlin"""
    g = client.gremlin()
    print("gremlin.exec: ", g.exec("g.V().limit(10)"))

    """graphs"""
    g = client.graphs()
    print("get_graph_info: ", g.get_graph_info())
    print("get_all_graphs: ", g.get_all_graphs())
    print("get_version: ", g.get_version())
    print("get_graph_config: ", g.get_graph_config())
