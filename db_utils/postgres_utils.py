import psycopg2

def get_schema_metadata_pg(host, port, dbname, user, password, schema="public"):
    conn = psycopg2.connect(
        host=host, port=port, dbname=dbname, user=user, password=password
    )
    cursor = conn.cursor()

    query = """
    SELECT
        table_name,
        column_name,
        data_type
    FROM
        information_schema.columns
    WHERE
        table_schema = %s
    ORDER BY
        table_name, ordinal_position
    """

    cursor.execute(query, (schema,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# ✅ NOVA FUNÇÃO
def format_schema_context(schema_data):
    context = {}
    for table_name, col_name, col_type in schema_data:
        if table_name not in context:
            context[table_name] = {
                "table_comment": "",
                "columns": []
            }
        context[table_name]["columns"].append({
            "name": col_name,
            "type": col_type,
            "comment": ""
        })
    return context

def context_to_text(context):
    return "\n".join([
        f"Tabela: {t} ({v['table_comment']})\n" +
        "\n".join([f"  - {c['name']} ({c['type']}): {c['comment']}" for c in v['columns']])
        for t, v in context.items()
    ])
