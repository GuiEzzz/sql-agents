from agents.postgres_agent import build_graph
from db_utils.postgres_utils import get_schema_metadata_pg, format_schema_context, context_to_text
from agents.postgres_agent import QueryGraphState
from dotenv import load_dotenv
load_dotenv()



if __name__ == "__main__":
    # Configurações do PostgreSQL
    config = {
        "host": "localhost",
        "port": 5432,
        "dbname": "Agente",
        "user": "postgres",
        "password": "admin",
        "schema": "public"
    }


    user_input = "Liste todos os clientes com pedidos pendentes"

    # Extrair schema
    raw_schema = get_schema_metadata_pg(**config)
    schema_context = format_schema_context(raw_schema)
    schema_text = context_to_text(schema_context)
    print("📊 Schema enviado ao modelo:\n", schema_text)


    # Executar o grafo
    graph = build_graph()
    input_state = {
    "user_input": user_input,
    "schema_text": schema_text
}


    result = graph.invoke(input_state)
    print(result)



