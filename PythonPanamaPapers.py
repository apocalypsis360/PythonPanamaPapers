
from gremlin_python.driver import client, serializer


ENDPOINT = "034c494b-0ee0-4-231-b9ee.gremlin.cosmosdb.azure.com"
DATABASE="panamapapers"
COLLECTION ="PanamaPapers"
PASSWORD ="htcsHsPbriv2AVBz8ydbKvdqKqvhNVHddxBOCv89IeJvupqVM2lg5lvcuYnaO63bc4qLMvDIgrrpWZsV0lGBFg=="
PORT = 443

VERTICES = [
    "g.addV('PERSON').property('id', 'P1').property('name', 'Tim Cook').property('title', 'CEO')",
    "g.addV('PERSON').property('id', 'P2').property('name', 'Jonathan Ive').property('title', 'Chief Design Officer')",
    "g.addV('COMPANY').property('id', 'C1').property('name', 'Apple').property('location', 'California, USA')",
    "g.addV('SKILL').property('id', 'S1').property('name', 'Leadership')",
    "g.addV('SKILL').property('id', 'S2').property('name', 'Design')",
    "g.addV('SKILL').property('id', 'S3').property('name', 'Innovation')"
]

EDGES = [
    "g.V('P1').addEdge('manages').to(g.V('P2'))",
    "g.V('P2').addE('managed by').to(g.V('P1'))",
    "g.V('P1').addE('works for').to(g.V('C1'))",
    "g.V('P2').addE('works for').to(g.V('C1'))",
    "g.V('P1').addE('competent in').to(g.V('S1'))",
    "g.V('P2').addE('competent in').to(g.V('S1'))",
    "g.V('P2').addE('competent in').to(g.V('S2'))",
    "g.V('P2').addE('competent in').to(g.V('S3'))"
]


def cleanup_graph(gremlin_client):
    cleanCmd = "g.V().drop()"
    callback = gremlin_client.submitAsync(cleanCmd)
    if callback.result() is not None:
        print(" Cleaned up the graph! ")

def insert_vertices(gremlin_clinet):
    for vertex in VERTICES:
        callback = gremlin_clinet.submitAsync(vertex)
        if callback.result() is None:
            print("Something went worng with this query: {0}".fromat(vertex))

def insert_edges(gremlin_client):
    for edge in EDGES:
        callback = gremlin_client.submitAsync(edge)
        if callback.result() is None:
            print("Something went worng with this query: {0}".fromat(edge))

#https://pydoc.net/gremlinpython/3.4.6/gremlin_python.driver.serializer/
#https://github.com/Azure-Samples/azure-cosmos-db-graph-gremlindotnet-getting-started/issues/1 - Florian Hockman
def handler():
    #Initialise client
    print("Initialising client ...")
    gremlin_client = client.Client("wss://"+ ENDPOINT + ":" +str(PORT)+ "/", "g",
                                   message_serializer= serializer.GraphSONSerializersV2d0(),
                                   username = "/dbs/" + DATABASE + "/colls/" + COLLECTION,
                                   password = PASSWORD)

    print("client initlaised!" )

    #Pruge graph
    cleanup_graph(gremlin_client)

    #Insert vertices
    insert_vertices(gremlin_client)

    # Insert edges (nodes)
    insert_edges(gremlin_client)

    print("Finished !")


if __name__ == "__main__":
    handler()