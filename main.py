from langchain.agents import create_agent
from langchain.tools import tool
from datetime import datetime

@tool
def cafe_esta_aberto() -> str:
    """Vê se o café está aberto com base no horário atual."""
    data_atual = datetime.now()
    if 1 <= data_atual.weekday() <= 5 and 8 <= data_atual.hour < 18:
        return"O Café Lua de Vidro está aberto! Venha nos visitar."
    else:
        return"O Café Lua de Vidro está fechado. Nosso horário de funcionamento é de terça a sábado, das 8h às 18h."

@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"



SYSTEM_PROMPT="""Você é a Lia, atendente virtual do Café Lua de Vidro, em Joinville.

Regras:
- Responda em português, em no máximo 2 frases.
- Use APENAS as informações abaixo.
- Se a informação não estiver abaixo, diga: "Não tenho essa informação."
- Use a ferramenta get_weather somente em perguntas sobre o clima.
- Use a ferramenta cafe_esta_aberto somente em perguntas sobre o horário de funcionamento.

Informações:
- Horário: terça a sábado, das 8h às 18h. Fechado domingo e segunda.
- Cardápio: espresso R$ 6, cappuccino R$ 11, pão de queijo R$ 5, bolo de cenoura R$ 9.
- Promoção: às quartas, cappuccino + pão de queijo por R$ 13.
- Pagamento: Pix e cartão. Não aceitamos dinheiro.
"""

agent = create_agent(
    model="ollama:llama3.2:3b",
    tools=[get_weather, cafe_esta_aberto],
    system_prompt=SYSTEM_PROMPT
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Vocês estão abertos agora?"}]}
)
print(result["messages"][-1].content_blocks)