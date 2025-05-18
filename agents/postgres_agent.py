from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI

class QueryGraphState(dict):
    pass

from langchain_community.chat_models import ChatOpenAI

def generate_sql(state: dict) -> dict:
    """Gera uma query SQL com base no schema e no comando em linguagem natural."""
    print("🧪 [DEBUG] Conteúdo do state recebido:")
    print(state)

    prompt = f"""
    Você é um assistente que gera apenas queries SQL válidas para PostgreSQL, com base no schema abaixo.

    Schema:
    {state.get('schema_text', '[SCHEMA NÃO DETECTADO]')}

    Comando do usuário:
    {state.get('user_input', '[COMANDO NÃO INFORMADO]')}

    Responda apenas com a query SQL completa e válida, sem explicações.
    """

    print("📝 Prompt enviado ao modelo:\n", prompt)
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    response = llm.invoke(prompt)
    print("🧠 Resposta do LLM:", response)


    # ✅ extrair o texto
    state["generated_sql"] = response.content if hasattr(response, "content") else str(response)
    return state




def show_result(state: QueryGraphState) -> QueryGraphState:
    print(f"\nQuery gerada:\n{state.get('generated_sql', '[nada gerado]')}")
    return state

def build_graph():
    builder = StateGraph(dict)
    builder.add_node("generate_sql", generate_sql)
    builder.add_node("show_result", show_result)
    builder.set_entry_point("generate_sql")
    builder.add_edge("generate_sql", "show_result")
    return builder.compile()