import os
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Carrega as chaves diretamente das variáveis de ambiente
openai_api_key = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["SERPER_API_KEY"] = serper_api_key

llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)
busca = SerperDevTool()
raspagem = ScrapeWebsiteTool()

# Agentes
planejador = Agent(
    role="Planejador de Conteúdo",
    goal="Planejar conteúdo envolvente e factual sobre {tópico}",
    backstory="Você estrutura o conteúdo de forma clara e organizada.",
    tools=[busca, raspagem],
    llm=llm
)

escritor = Agent(
    role="Redator de Conteúdo",
    goal="Redigir um artigo em português do Brasil, baseado no esboço do planejador",
    backstory="Você escreve com base no planejamento e pesquisa.",
    tools=[busca, raspagem],
    llm=llm
)

editor = Agent(
    role="Editor",
    goal="Revisar e ajustar o artigo para clareza e coesão",
    backstory="Você finaliza o texto com qualidade editorial.",
    tools=[],
    llm=llm
)

# Tarefas
planejamento = Task(
    description="Criar um esboço detalhado com base em tópicos atuais sobre {tópico}.",
    expected_output="Esboço em markdown com subtítulos",
    agent=planejador
)

escrita = Task(
    description="Escrever um artigo com base no esboço, com 3 seções e conclusão.",
    expected_output="Artigo em markdown com título, seções e conclusão",
    agent=escritor
)

edicao = Task(
    description="Revisar o artigo final garantindo clareza, estrutura e português correto.",
    expected_output="Artigo final pronto para publicação",
    agent=editor
)

# Execução
crew = Crew(
    agents=[planejador, escritor, editor],
    tasks=[planejamento, escrita, edicao],
    verbose=True
)

print("🚀 Gerando artigo...")
resultado = crew.kickoff(inputs={"tópico": "Plano de Gestão dos Institutos Federais"})

# Salvar como HTML
os.makedirs("site", exist_ok=True)
with open("site/index.html", "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><title>Artigo Gerado</title></head>
<body><h1>Artigo: Plano de Gestão dos Institutos Federais</h1>
<pre>{resultado}</pre>
</body></html>""")

print("✅ site/index.html criado com sucesso.")
