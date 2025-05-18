from agents.postgres_agent import build_graph
from db_utils.postgres_utils import get_schema_metadata_pg, format_schema_context, context_to_text
from agents.postgres_agent import QueryGraphState
from dotenv import load_dotenv
load_dotenv()
import psycopg2

def listar_tabelas_pg(host, port, dbname, user, password, schema="public"):
    conn = psycopg2.connect(
        host=host, port=port, dbname=dbname, user=user, password=password
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s
    """, (schema,))
    
    tabelas = cursor.fetchall()
    conn.close()

    if not tabelas:
        print("⚠️ Nenhuma tabela encontrada no schema:", schema)
    else:
        print(f"📂 Tabelas no schema '{schema}':")
        for t in tabelas:
            print("  -", t[0])




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

    listar_tabelas_pg(
    config["host"], config["port"], config["dbname"],
    config["user"], config["password"],
    config["schema"]
)



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



