document.addEventListener("alpine:init", () => {
  Alpine.data("bacissPortal", () => ({
    activeModuleId: "phase1",
    activeTab: "steps",
    copiedTarget: null,

    commands: {
      uvWin:
        'powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.13.7/install.ps1 | iex"',
      uvMac: "curl -LsSf https://astral.sh/uv/0.13.7/install.sh | sh",
      clone: "git clone https://github.com/ujblockchain/community-voice-app.git\ncd community-voice-app",
      sync: "uv python install 3.12\nuv sync --locked",
      env: "cp .env.example .env",
      seed: "uv run python -m community_voice.auth.seed",
      ollama: "ollama pull llama3.2:3b",
      frontend: "cd frontend && npm ci && cp .env.example .env.local && cd ..",
      pytest: "uv run pytest",
      runApi: "uv run uvicorn community_voice.api.main:app --port 8800",
      runStreamlit: "uv run streamlit run app/streamlit_app.py",
      runNext: "cd frontend && npm run dev",
      adminEmail: "admin@communityvoice.test",
      cit1Email: "citizen1@communityvoice.test",
      cit2Email: "citizen2@communityvoice.test",
      tree: `src/community_voice/     The application
  core/                  Settings (.env) and tracing setup
  auth/                  Password hashing, login tokens and the test-account seed
  schemas/               Pydantic models: the shape of data passed between steps
  llm/                   Which model (Gemini, Groq or local Ollama) each agent uses
  privacy/               The privacy filter: removes personal details before the cloud
  agents/                Triage, routing, context check, drafter and chat assistant agents
  tools/                 What the agents can call: directory lookup, policy search, web search, duplicate search
  rag/                   Search indexes (Chroma): policy documents and past reports
  graph/                 The LangGraph workflow: state, steps, pauses for humans, saved progress and memory
  db/                    SQLite storage for reports, reviews, drafts and users
  media/                 Voice-note transcription and photo checks
  api/                   FastAPI endpoints and streaming of progress
  mcp_server/            Directory tools served over Model Context Protocol (MCP demo)
app/                     Streamlit screens: sign in, submit, my reports, messages, review queue, dashboard
frontend/                Next.js app (TypeScript, Tailwind CSS 4, shadcn/ui)
data/                    knowledge_base/, sample_reports/ (audio files), evals/
evals/                   Scoring code and baseline regressions
notebooks/               Step-by-step interactive phases 01 to 12`,
    },

    initHighlighting() {
      this.$nextTick(() => {
        if (window.Prism) Prism.highlightAll();
      });
    },

    selectModule(id) {
      this.activeModuleId = id;
      this.$nextTick(() => {
        if (window.Prism) Prism.highlightAll();
      });
    },

    switchTab(tab) {
      this.activeTab = tab;
      this.$nextTick(() => {
        if (window.Prism) Prism.highlightAll();
      });
    },

    async copyText(text, targetId) {
      let success = false;

      // 1. Try modern clipboard API if in secure context
      if (navigator.clipboard && window.isSecureContext) {
        try {
          await navigator.clipboard.writeText(text);
          success = true;
        } catch (err) {
          console.warn(
            "navigator.clipboard blocked or failed, attempting fallback...",
            err,
          );
        }
      }

      // 2. Headless textarea fallback (works reliably everywhere: file://, HTTP, iframes)
      if (!success) {
        try {
          const textArea = document.createElement("textarea");
          textArea.value = text;
          textArea.style.position = "fixed";
          textArea.style.left = "-999999px";
          textArea.style.top = "-999999px";
          textArea.setAttribute("readonly", "");
          document.body.appendChild(textArea);
          textArea.focus();
          textArea.select();
          success = document.execCommand("copy");
          document.body.removeChild(textArea);
        } catch (err) {
          console.error("All clipboard methods failed:", err);
        }
      }

      // 3. Trigger visual checkmark tick
      if (success) {
        this.copiedTarget = targetId;
        setTimeout(() => {
          if (this.copiedTarget === targetId) {
            this.copiedTarget = null;
          }
        }, 2000);
      }
    },

    modules: [
      {
        id: "phase1",
        phase: "01",
        title: "Phase 1: Structured output with the Triage Agent",
        file: "01_triage_structured_output.ipynb",
        desc: "Pydantic contracts, multi-language reports & schema validation.",
        concept:
          "A language model normally answers in free text. Our software needs reliable fields such as category and urgency. So we describe the answer we want as a Pydantic model (a contract), ask the model to follow it, and Pydantic checks the result. If the model breaks the contract we get an error, not silent bad data.",
        agent:
          "This is our first agent, the Triage Agent. It has no tools: it reads one citizen report and decides the language, an English translation, the category, a summary and the urgency.",
        whatToNotice: [
          "The model returned typed fields we can rely on, in any of five languages.",
          "The answers are checked against the contract: an unknown category would raise an error.",
          "Changing the urgency guide in src/community_voice/agents/triage.py changes the model's behaviour.",
        ],
        steps: [
          {
            stepNumber: 1,
            title: "1. Load the code and settings",
            explanation:
              "The real logic lives in src/community_voice/. This notebook only imports it.",
            code: `import json
from pathlib import Path

import community_voice
from community_voice.agents.triage import triage
from community_voice.core.config import get_settings
from community_voice.schemas.report import ReportIn, SampleReport
from community_voice.schemas.triage import TriageResult

ROOT = Path(community_voice.__file__).resolve().parents[2]
settings = get_settings()
print("Gemini model:", settings.gemini_model)
print("Groq model:  ", settings.groq_model)`,
          },
          {
            stepNumber: 2,
            title: "2. The contract",
            explanation:
              "These are the fields the model must fill in. The descriptions are sent to the model, so they act as instructions.",
            code: `for name, field in TriageResult.model_fields.items():
    print(f"{name:16} {field.description}")`,
          },
          {
            stepNumber: 3,
            title: "3. Triage one report",
            explanation:
              "An isiZulu report about a leaking water pipe in Umlazi. We never tell the model the language.",
            code: `report = ReportIn(
    text="Amanzi ayaphuma emgwaqeni e-Umlazi V Section, "
    "kuvuza ipayipi elikhulu kusukela izolo."
)
result = triage(report)
print(result.model_dump_json(indent=2))`,
          },
          {
            stepNumber: 4,
            title: "4. Triage all 10 sample reports",
            explanation:
              "These fictional reports are in English, isiZulu, isiXhosa, Afrikaans and Sesotho. Each has the answer we expect, so we can check the agent.",
            code: `path = ROOT / "data" / "sample_reports" / "reports.json"
samples = [
    SampleReport.model_validate(item)
    for item in json.loads(path.read_text(encoding="utf-8"))
]
print(len(samples), "sample reports loaded")

results = []
for sample in samples:
    result = triage(ReportIn(text=sample.text))
    results.append(result)
    cat_ok = result.category == sample.expected_category
    urg_ok = result.urgency == sample.expected_urgency
    print(
        f"{sample.id}  {result.language.value:5} {result.category.value:12}"
        f" {result.urgency.value:9} category ok: {cat_ok!s:5}"
        f" urgency ok: {urg_ok!s:5}"
    )

pairs = list(zip(samples, results, strict=True))
category_hits = sum(r.category == s.expected_category for s, r in pairs)
urgency_hits = sum(r.urgency == s.expected_urgency for s, r in pairs)
print(f"Category matches our label: {category_hits}/{len(samples)}")
print(f"Urgency matches our label:  {urgency_hits}/{len(samples)}")

for sample, result in pairs:
    print(sample.id, "|", result.summary)
    print("     urgency:", result.urgency.value, "-", result.urgency_reason)`,
          },
          {
            stepNumber: 5,
            title: "5. Swap the model provider",
            explanation:
              "Our provider layer lets an agent use a different model by changing one word. Here we run the same report on Groq. Some models do not support structured output, so if this fails the error is shown instead of stopping the notebook.",
            code: `try:
    groq_result = triage(ReportIn(text=samples[1].text), provider="groq")
    print(groq_result.model_dump_json(indent=2))
except Exception as error:
    print("Groq structured output failed:", type(error).__name__, error)`,
          },
        ],
      },
      {
        id: "phase2",
        phase: "02",
        title: "Phase 2: Tools and ReAct (Routing Agent)",
        file: "02_react_routing.ipynb",
        desc: "Area-to-municipality and department tool chaining.",
        concept:
          "An agent can call tools. In a ReAct loop it reasons, acts (calls a tool), reads the result, and repeats until it can answer.",
        agent:
          "Our Routing Agent has two tools and must chain them: area to municipality, then municipality to department.",
        whatToNotice: [
          "The agent chose which tool to call, and in what order.",
          "It used the first tool's result as input to the second.",
          "With no match, it asked for a human instead of guessing.",
          "To use Gemini instead of Groq, pass provider='gemini' to run_routing_agent.",
        ],
        steps: [
          {
            stepNumber: 1,
            title: "1. The tools",
            explanation:
              "Plain Python functions with @tool. The docstring tells the agent when to use each one.",
            code: `import json
from pathlib import Path

import community_voice
from community_voice.agents.routing import run_routing_agent
from community_voice.agents.triage import triage
from community_voice.schemas.report import ReportIn, SampleReport
from community_voice.schemas.triage import TriageResult
from community_voice.tools.directory import find_municipality, lookup_department

ROOT = Path(community_voice.__file__).resolve().parents[2]

print(find_municipality.invoke({"area": "Umlazi"}))
print(lookup_department.invoke({"municipality": "eThekwini", "category": "water"}))`,
          },
          {
            stepNumber: 2,
            title: "2. Route one report",
            explanation:
              "Triage first, then route. show_trace prints each tool call (ACT) and what came back (RESULT).",
            code: `def show_trace(state):
    for message in state["messages"]:
        if message.type == "ai" and message.tool_calls:
            for call in message.tool_calls:
                if call["name"] != "RoutingResult":
                    print("ACT   ", call["name"], call["args"])
        elif message.type == "tool" and message.name != "RoutingResult":
            print("RESULT", message.content)

report = ReportIn(
    text="Amanzi ayaphuma emgwaqeni e-Umlazi V Section, "
    "kuvuza ipayipi elikhulu kusukela izolo."
)
triaged = triage(report)
state = run_routing_agent(triaged)
show_trace(state)
print(state["structured_response"].model_dump_json(indent=2))`,
          },
          {
            stepNumber: 3,
            title: "3. Route all 10 sample reports",
            explanation:
              "Runs triage and routing for all sample citizen reports and displays routing conclusions.",
            code: `path = ROOT / "data" / "sample_reports" / "reports.json"
samples = [
    SampleReport.model_validate(item)
    for item in json.loads(path.read_text(encoding="utf-8"))
]
for sample in samples:
    triaged = triage(ReportIn(text=sample.text))
    routing = run_routing_agent(triaged)["structured_response"]
    print(
        f"{sample.id}  {triaged.category.value:11}"
        f" {str(triaged.area_mentioned):17} {routing.municipality:19}"
        f" {routing.department:22} human: {routing.needs_human}"
    )`,
          },
          {
            stepNumber: 4,
            title: "4. An area that is not in the directory",
            explanation:
              "The agent must not guess. It should answer unknown and ask for a human.",
            code: `unknown = TriageResult(
    language="en",
    english_text="No water since Monday.",
    category="water",
    summary="Water outage.",
    urgency="high",
    urgency_reason="Outage for days.",
    area_mentioned="Thornville Heights",
)
state = run_routing_agent(unknown)
show_trace(state)
print(state["structured_response"].model_dump_json(indent=2))`,
          },
        ],
      },
      {
        id: "phase3",
        phase: "03",
        title: "Phase 3: RAG (retrieval-augmented generation)",
        file: "03_rag_policy_search.ipynb",
        desc: "Vector embeddings and policy retrieval with ChromaDB.",
        concept:
          "A model only knows what it was trained on, so it guesses about documents it has never seen. RAG stores our documents as searchable chunks, retrieves the closest ones to a question, and gives them to the model. Search works by meaning (embeddings), not keywords.",
        agent:
          "RAG policy agent with search_policy tool answering strictly from retrieved context.",
        whatToNotice: [
          "Search found the right section without matching keywords.",
          "Without retrieval the model guessed. With it, the answer comes from our document and names the source.",
          "Change a time in data/knowledge_base/policies/water_charter.md, run section 1 again, and ask again.",
        ],
        steps: [
          {
            stepNumber: 1,
            title: "1. Build the index",
            explanation:
              "Each ## section becomes a chunk. Chroma embeds every chunk on your machine. The first run downloads the embedding model, so it can take a while.",
            code: `from langchain.agents import create_agent

from community_voice.llm.providers import get_chat_model
from community_voice.rag.store import build_index, search
from community_voice.tools.policy import search_policy

print(build_index(), "chunks indexed")`,
          },
          {
            stepNumber: 2,
            title: "2. Search by meaning",
            explanation:
              "The queries share few words with the documents. A smaller distance means a closer match.",
            code: `queries = [
    "No lights on our street at night",
    "How long until a burst pipe is fixed?",
    "My rubbish was not collected",
]
for query in queries:
    print(query)
    for hit in search(query, n_results=2):
        title = hit["text"].splitlines()[0]
        print(f"  {hit['distance']:.2f}  {title}")`,
          },
          {
            stepNumber: 3,
            title: "3. Ask without retrieval",
            explanation:
              "The model has never seen our charters, so it guesses.",
            code: `question = (
    "Under our service charter, within how many working days must a faulty "
    "streetlight at a dangerous intersection be repaired?"
)
print(get_chat_model("groq").invoke(question).text)`,
          },
          {
            stepNumber: 4,
            title: "4. Ask with retrieval",
            explanation:
              "Same question, but the agent can call search_policy and must answer from what it finds.",
            code: `agent = create_agent(
    model=get_chat_model("groq"),
    tools=[search_policy],
    system_prompt=(
        "Answer only from the search_policy results and name the source file. "
        "If the answer is not there, say so."
    ),
)
result = agent.invoke({"messages": [{"role": "user", "content": question}]})
print(result["messages"][-1].text)`,
          },
        ],
      },
      {
        id: "phase4",
        phase: "04",
        title: "Phase 4: MCP (Model Context Protocol)",
        file: "04_mcp_tools.ipynb",
        desc: "Decoupling tools into a separate MCP server process.",
        concept:
          "MCP is a standard way to offer tools from a separate server. Any MCP-capable app can use them, with no custom glue code.",
        agent:
          "Our server (mcp_server/server.py) offers three tools. The Routing Agent connects to it and uses them.",
        whatToNotice: [
          "The tools live in a separate server process. The agent only knows their names and descriptions.",
          "The agent code did not change, only where its tools come from.",
          "Any other MCP client could use this server too.",
          "Stop the server with Ctrl+C in its terminal when you are done.",
        ],
        steps: [
          {
            stepNumber: 1,
            title: "1. Tools from the server",
            explanation:
              "The client connects to the running server and asks what it offers. Names and descriptions come from the server's code.",
            code: `from community_voice.agents.routing import arun_routing_agent
from community_voice.agents.triage import triage
from community_voice.mcp_server.client import get_mcp_tools
from community_voice.schemas.report import ReportIn

tools = await get_mcp_tools()
for tool in tools:
    print(tool.name, "-", tool.description.splitlines()[0])`,
          },
          {
            stepNumber: 2,
            title: "2. Call a tool through MCP",
            explanation:
              "Direct invocation of a remote MCP tool using asynchronous ainvoke.",
            code: `find = next(tool for tool in tools if tool.name == "find_municipality")
print(await find.ainvoke({"area": "Umlazi V Section"}))`,
          },
          {
            stepNumber: 3,
            title: "3. Route a report with MCP tools",
            explanation:
              "The same Routing Agent as Phase 2. Only the source of its tools changed.",
            code: `def show_trace(state):
    for message in state["messages"]:
        if message.type == "ai" and message.tool_calls:
            for call in message.tool_calls:
                if call["name"] != "RoutingResult":
                    print("ACT   ", call["name"], call["args"])
        elif message.type == "tool" and message.name != "RoutingResult":
            print("RESULT", message.text)

report = ReportIn(
    text="Amanzi ayaphuma emgwaqeni e-Umlazi V Section, "
    "kuvuza ipayipi elikhulu kusukela izolo."
)
triaged = triage(report)
state = await arun_routing_agent(triaged, tools)
show_trace(state)
print(state["structured_response"].model_dump_json(indent=2))`,
          },
        ],
      },
      {
        id: "phase5",
        phase: "05",
        title: "Phase 5: Web search (Context Check agent)",
        file: "05_context_check.ipynb",
        desc: "Tavily web search to verify planned municipal outages.",
        concept:
          "Is a reported problem already a known or planned outage? The Context Check agent searches the web with Tavily and answers with cited sources.",
        agent:
          "It only receives the service, area and municipality, never the report text, so no personal details can reach a search. Results come from the live web.",
        whatToNotice: [
          "The agent chose its own search words and could search again.",
          "Every source is a page the search returned.",
          "With no evidence, it said so.",
          "Web text is untrusted: the prompt tells the agent to treat it as data.",
        ],
        steps: [
          {
            stepNumber: 1,
            title: "1. A raw search",
            explanation:
              "The tool returns the last month's results as title, URL and a short snippet.",
            code: `from community_voice.agents.context_check import run_context_check
from community_voice.tools.web_search import web_search

print(web_search.invoke({"query": "Soweto power outage Johannesburg"}))`,
          },
          {
            stepNumber: 2,
            title: "2. Check an area",
            explanation:
              "show prints each search the agent makes (ACT), what came back (RESULT, shortened), and the final answer.",
            code: `def show(state):
    for message in state["messages"]:
        if message.type == "ai" and message.tool_calls:
            for call in message.tool_calls:
                if call["name"] != "ContextCheckResult":
                    print("ACT   ", call["name"], call["args"])
        elif message.type == "tool" and message.name != "ContextCheckResult":
            print("RESULT", message.text[:150].replace("\\n", " "))
    print(state["structured_response"].model_dump_json(indent=2))

show(run_context_check("electricity", "Soweto", "Johannesburg"))
show(run_context_check("water", "Soshanguve", "Tshwane"))`,
          },
          {
            stepNumber: 3,
            title: "3. An area with nothing to find",
            explanation:
              "The area is made up. The agent should say nothing_found, with low confidence and no sources, instead of inventing a link.",
            code: `show(run_context_check("water", "Zzyzx Heights", "eThekwini"))`,
          },
        ],
      },
      {
        id: "phase6",
        phase: "06",
        title: "Phase 6: Orchestration with LangGraph",
        file: "06_graph_workflow.ipynb",
        desc: "State graphs, conditional branching, duplicate checks.",
        concept:
          "So far each agent ran alone. A LangGraph graph connects them: every step reads and writes a shared state, and conditional edges choose the next step.",
        agent:
          "Flow: triage, routing, web check, duplicate check. Critical reports skip the web check, and a planned outage ends early.",
        whatToNotice: [
          "One shared state: each step adds its result and later steps read it.",
          "Different reports take different paths through the same graph.",
          "The duplicate check compares with earlier reports and asks a model to confirm.",
          "If the first report hit the planned-outage path, it was not stored, so the duplicate is not found.",
        ],
        steps: [
          {
            stepNumber: 1,
            title: "1. The graph",
            explanation:
              "The diagram as text. Paste it into any Mermaid viewer (for example mermaid.live) to see it drawn.",
            code: `from langgraph.checkpoint.memory import InMemorySaver

from community_voice.db.repository import reset_database
from community_voice.graph.workflow import build_graph
from community_voice.rag.reports import reset_reports
from community_voice.schemas.report import ReportIn

graph = build_graph(InMemorySaver())
print(graph.get_graph().draw_mermaid())`,
          },
          {
            stepNumber: 2,
            title: "2. Run a report and watch each step",
            explanation:
              "graph.stream returns each step's update as soon as it finishes.",
            code: `def run(report_id, text):
    inputs = {"report_id": report_id, "report": ReportIn(text=text)}
    config = {"configurable": {"thread_id": report_id}}
    for chunk in graph.stream(inputs, config, stream_mode="updates", version="v2"):
        if chunk["type"] != "updates":
            continue
        for node, update in chunk["data"].items():
            print(f"[{node}]")
            for key, value in update.items():
                print(f"   {key}: {str(value)[:160]}")

reset_database()
reset_reports()
run(
    "r02",
    "Amanzi ayaphuma emgwaqeni e-Umlazi V Section, "
    "kuvuza ipayipi elikhulu kusukela izolo.",
)`,
          },
          {
            stepNumber: 3,
            title: "3. A critical report",
            explanation:
              "Live wires near a hospital. Look for the web check: it should be skipped.",
            code: `run(
    "r05",
    "After last night's storm there are live wires hanging low over the "
    "road near Tembisa Hospital. Children walk under them to get to school.",
)`,
          },
          {
            stepNumber: 4,
            title: "4. A duplicate",
            explanation:
              "The same burst pipe in Umlazi, reported again in different words.",
            code: `run(
    "r02b",
    "A big pipe has burst in Umlazi V Section and water has been running "
    "down the street since yesterday.",
)`,
          },
        ],
      },
      {
        id: "phase7",
        phase: "07",
        title: "Phase 7: Human review and persistence",
        file: "07_review_and_persistence.ipynb",
        desc: "SQLite checkpointer, thread IDs, and interrupt-resume cycle.",
        concept:
          "The graph now saves each report and pauses until a person reviews it. Its state is stored in SQLite, so a paused report survives a restart. One report is one thread (thread_id = report id). The saved state of a thread is the graph's short-term memory.",
        agent:
          "Human-in-the-loop review agent with SQLite checkpoints and Command resume.",
        whatToNotice: [
          "The graph stopped and waited, then continued from the same place after a restart.",
          "The reviewer's correction was applied and the review was recorded.",
          "Code before interrupt() runs again on resume, so that step has no side effects. Saving happens in separate steps.",
          "A report that the web check finds to be a planned outage skips review, so it would not appear in the queue.",
        ],
        steps: [
          {
            stepNumber: 1,
            title: "1. Start fresh",
            explanation:
              "Clear the report database and the similarity index from earlier runs.",
            code: `import json

from community_voice.db.repository import list_pending, reset_database
from community_voice.graph.persistence import get_checkpointer
from community_voice.graph.workflow import build_graph
from community_voice.rag.reports import reset_reports
from community_voice.schemas.report import ReportIn

reset_database()
reset_reports()`,
          },
          {
            stepNumber: 2,
            title: "2. Submit a report",
            explanation:
              "Live wires near a hospital: critical report skips web check and reaches review. The graph runs, saves, and pauses.",
            code: `graph = build_graph(get_checkpointer())
config = {"configurable": {"thread_id": "r05"}}
inputs = {
    "report_id": "r05",
    "report": ReportIn(
        text="After last night's storm there are live wires hanging low over the "
        "road near Tembisa Hospital. Children walk under them to get to school."
    ),
}
result = graph.invoke(inputs, config, version="v2")
print("Paused at:", graph.get_state(config).next)
print(json.dumps(result.interrupts[0].value, indent=2, ensure_ascii=False))`,
          },
          {
            stepNumber: 3,
            title: "3. The review queue",
            explanation: "Read from the database, most urgent first.",
            code: `for report in list_pending():
    print(report.id, report.urgency, report.status, report.department)`,
          },
          {
            stepNumber: 4,
            title: "4. Restart the kernel",
            explanation:
              "Click Restart in the toolbar. Everything in memory is gone, including the graph. The report is safe on disk. Then run only the cells below.",
            code: `from langgraph.types import Command

from community_voice.db.repository import get_report, list_pending, list_reviews
from community_voice.graph.persistence import get_checkpointer
from community_voice.graph.workflow import build_graph

graph = build_graph(get_checkpointer())
waiting = list_pending()
print([report.id for report in waiting])`,
          },
          {
            stepNumber: 5,
            title: "5. Resume with a correction",
            explanation:
              "The reviewer approves, but sends it to the emergency line. The answer becomes the return value of interrupt().",
            code: `report_id = waiting[0].id
config = {"configurable": {"thread_id": report_id}}
answer = {
    "action": "approve",
    "department": "Ekurhuleni Electricity department (emergency line)",
    "note": "Live wires near a hospital and a school: send the emergency crew.",
}
result = graph.invoke(Command(resume=answer), config, version="v2")
print("Status:", result.value["status"])`,
          },
          {
            stepNumber: 6,
            title: "6. What is in the database",
            explanation:
              "Verifies stored report status, recorded reviews, and remaining pending queue.",
            code: `print(get_report(report_id).model_dump_json(indent=2))
print(list_reviews(report_id))
print("Still waiting:", list_pending())`,
          },
        ],
      },
      {
        id: "phase8",
        phase: "08",
        title: "Phase 8: Long-term memory and the Drafter",
        file: "08_memory_and_drafting.ipynb",
        desc: "Cross-report memory nudges and dual review approval.",
        concept:
          "Long-term memory keeps what reviewers corrected, so similar reports get hints next time. The Drafter writes a suggested reply, and a person approves it before it is ready to send. Nothing is ever sent without getting human approval. Memory here is hints in the prompt, not model training.",
        agent:
          "Drafter agent generating policy-grounded replies with two human approval gates.",
        whatToNotice: [
          "Memory is shared across reports. Short-term memory belongs to one report.",
          "Only a real change by a reviewer is remembered.",
          "The Drafter works from our policy documents, but it can still pick the wrong figure. A person checks the draft.",
          "A person approves twice before a reply is ready to send.",
        ],
        steps: [
          {
            stepNumber: 1,
            title: "1. Start fresh",
            explanation:
              "Creates the memory file, data/memory.db, and clears old memory using the local embedding model.",
            code: `import json
from uuid import uuid4

from langgraph.types import Command

from community_voice.agents.triage import triage
from community_voice.db.repository import get_draft, reset_database
from community_voice.graph.memory import (
    NAMESPACE,
    find_hints,
    get_store,
    remember_correction,
    reset_memory,
)
from community_voice.graph.persistence import get_checkpointer
from community_voice.graph.workflow import build_graph
from community_voice.rag.reports import reset_reports
from community_voice.schemas.report import ReportIn
from community_voice.schemas.review import ReviewDecision
from community_voice.schemas.triage import TriageResult

store = get_store()
reset_memory(store)
reset_database()
reset_reports()`,
          },
          {
            stepNumber: 2,
            title: "2. Triage without memory",
            explanation:
              "A school with no water. A model would normally call this high, not critical.",
            code: `new_report = ReportIn(
    text="The taps at Sizwe Primary School in Gqeberha have been dry since Monday."
)
before = triage(new_report)
print(before.urgency.value, "-", before.urgency_reason)`,
          },
          {
            stepNumber: 3,
            title: "3. A reviewer corrects a similar report",
            explanation:
              "Triage said high, and reviewer changed it to critical. Only real changes are remembered.",
            code: `earlier_text = (
    "There has been no water at Thandi Primary School in Soshanguve for three days."
)
ai_said = TriageResult(
    language="en",
    english_text=earlier_text,
    category="water",
    summary="No water at a primary school.",
    urgency="high",
    urgency_reason="Essential service out for days.",
    area_mentioned="Soshanguve",
)
reviewer = ReviewDecision(
    action="approve",
    urgency="critical",
    note="A school without water is always critical here.",
)
saved = remember_correction(
    store, "r10", earlier_text, ai_said, "Tshwane Water and Sanitation", reviewer
)
print("Remembered:", saved)`,
          },
          {
            stepNumber: 4,
            title: "4. Hints for a similar report",
            explanation: "Search by meaning. A higher score is a closer match.",
            code: `unrelated = "A large pothole on Main Road in Woodstock damaged my tyre."
for query in (new_report.text, unrelated):
    print(query[:50])
    for item in store.search(NAMESPACE, query=query, limit=1):
        print("  ", round(item.score, 2), item.value["summary"])
hints = find_hints(store, new_report.text)
print(hints)`,
          },
          {
            stepNumber: 5,
            title: "5. Triage again, with the hints",
            explanation:
              "Re-runs triage injecting retrieved long-term memory hints.",
            code: `after = triage(new_report, hints=hints)
print(after.urgency.value, "-", after.urgency_reason)`,
          },
          {
            stepNumber: 6,
            title: "6. The Drafter and the second approval",
            explanation:
              "Graph pauses twice: first for report approval, second for draft approval.",
            code: `graph = build_graph(get_checkpointer(), store)
report_id = f"r05-{uuid4().hex[:6]}"
config = {"configurable": {"thread_id": report_id}}
inputs = {
    "report_id": report_id,
    "report": ReportIn(
        text="After last night's storm there are live wires hanging low over "
        "the road near Tembisa Hospital. Children walk under them to get to "
        "school."
    ),
}
result = graph.invoke(inputs, config, version="v2")
print("Paused at:", graph.get_state(config).next)

result = graph.invoke(Command(resume={"action": "approve"}), config, version="v2")
print("Paused at:", graph.get_state(config).next)
print(json.dumps(result.interrupts[0].value["draft"], indent=2))`,
          },
          {
            stepNumber: 7,
            title: "7. Approve the draft with an edit",
            explanation:
              "Reviewer edits draft and approves. Status transitions to ready_to_send.",
            code: `draft = result.interrupts[0].value["draft"]["body"]
edited = draft + "\\n\\nPlease keep children away from the wires."
answer = {"action": "approve", "text": edited}
result = graph.invoke(Command(resume=answer), config, version="v2")
print("Status:", result.value["status"])
print(get_draft(report_id)["body"])`,
          },
        ],
      },
      {
        id: "phase9",
        phase: "09",
        title: "Phase 9: The API and streaming",
        file: "09_api_and_streaming.ipynb",
        desc: "FastAPI HTTP endpoints and Server-Sent Events (SSE).",
        concept:
          "FastAPI puts the workflow behind HTTP endpoints, so any app can use it. Progress is streamed as server-sent events: one message per finished step.",
        agent: "RESTful streaming pipeline over HTTP.",
        whatToNotice: [
          "Each step arrived as soon as it finished, not all at the end.",
          "The API only moves a report forward when it is waiting for that decision.",
          "A screen can use the same calls: stream the steps, show the queue, send decisions.",
        ],
        steps: [
          {
            stepNumber: 1,
            title: "1. Is it running?",
            explanation:
              "Connects to running uvicorn instance and checks /health endpoint.",
            code: `import json

import httpx

BASE = "http://127.0.0.1:8800"


def stream(path, payload):
    """POST and print each event as it arrives. Returns all events."""
    events = []
    name = None
    with httpx.stream("POST", BASE + path, json=payload, timeout=180) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if line.startswith("event:"):
                name = line.split(":", 1)[1].strip()
            elif line.startswith("data:"):
                data = json.loads(line.split(":", 1)[1])
                events.append((name, data))
                shown = data.get("message") or data.get("report_id") or data
                print(f"{name:8}", str(shown)[:100])
    return events

print(httpx.get(BASE + "/health").json())`,
          },
          {
            stepNumber: 2,
            title: "2. Submit a report and watch it stream",
            explanation:
              "Critical report streams updates via SSE until it halts waiting for human review.",
            code: `report = {
    "text": "After last night's storm there are live wires hanging low over "
    "the road near Tembisa Hospital. Children walk under them to get to school."
}
events = stream("/reports", report)
report_id = events[0][1]["report_id"]`,
          },
          {
            stepNumber: 3,
            title: "3. The review queue and the report",
            explanation: "Inspect waiting queue and verify report status.",
            code: `for item in httpx.get(BASE + "/reviews").json():
    print(item["id"], item["urgency"], item["status"])
detail = httpx.get(f"{BASE}/reports/{report_id}").json()
print("Waiting for:", detail["waiting_for"])`,
          },
          {
            stepNumber: 4,
            title: "4. Send the review",
            explanation:
              "Reviewer approves report, triggering Drafter node stream until draft approval pause.",
            code: `events = stream(f"/reports/{report_id}/review", {"action": "approve"})
draft = events[-1][1]["payload"]["draft"]["body"]
print(draft)`,
          },
          {
            stepNumber: 5,
            title: "5. Approve the draft",
            explanation: "Final approval call moves report to ready_to_send.",
            code: `response = httpx.post(
    f"{BASE}/reports/{report_id}/draft", json={"action": "approve"}, timeout=60
)
print(response.json()["status"])`,
          },
          {
            stepNumber: 6,
            title: "6. Answering at the wrong time",
            explanation:
              "The report is finished, so submitting another draft decision is refused with 400 error.",
            code: `response = httpx.post(
    f"{BASE}/reports/{report_id}/draft", json={"action": "approve"}, timeout=60
)
print(response.status_code, response.json())`,
          },
        ],
      },
      {
        id: "phase10",
        phase: "10",
        title: "Phase 10: Voice notes and photos",
        file: "10_voice_and_photos.ipynb",
        desc: "Gemini audio transcription and EXIF GPS metadata stripping.",
        concept:
          "A report can arrive as a voice note. Speech-to-text (Gemini) turns it into text, and the citizen checks that text before it enters the same pipeline. Photos are optional and only for the human reviewer.",
        agent:
          "Multimodal input ingestion with citizen validation and privacy scrubbing.",
        whatToNotice: [
          "The voice note became text, and the pipeline did not change.",
          "Every transcript carries a warning, even English.",
          "The photo is optional, checked by decoding it, and its metadata is gone.",
        ],
        steps: [
          {
            stepNumber: 1,
            title: "1. One voice note",
            explanation:
              "Converts audio file to text transcript using Gemini speech-to-text.",
            code: `import io
import re

import httpx
from PIL import Image

from community_voice.agents.triage import triage
from community_voice.core.config import PROJECT_ROOT
from community_voice.media.photos import InvalidPhoto, clean_photo
from community_voice.media.transcribe import transcribe
from community_voice.schemas.report import ReportIn

AUDIO = PROJECT_ROOT / "data" / "sample_reports" / "audio"

path = AUDIO / "English.mp3"
transcript = transcribe(path.read_bytes(), path.name)
transcript`,
          },
          {
            stepNumber: 2,
            title: "2. Every language",
            explanation:
              "Gemini is not told the language. Every transcript comes with a warning so the citizen checks.",
            code: `for path in sorted(AUDIO.glob("*.mp3")):
    t = transcribe(path.read_bytes(), path.name)
    print(f"{path.stem}:")
    print("  ", t.text[:150])
print(t.warning)`,
          },
          {
            stepNumber: 3,
            title: "3. Into the same pipeline",
            explanation:
              "After the citizen confirms the text, it is an ordinary report.",
            code: `report = ReportIn(text=transcript.text)
result = triage(report)
print(result.category.value, result.urgency.value)
print(result.summary)`,
          },
          {
            stepNumber: 4,
            title: "4. Photos",
            explanation:
              "Phone photos carry hidden GPS data. We build a photo with fake metadata, decode to prove real, resize, and re-save stripped.",
            code: `exif = Image.Exif()
exif[0x010F] = "TestPhone"
exif.get_ifd(0x8825)[1] = "S"  # a GPS entry

buffer = io.BytesIO()
Image.new("RGB", (3200, 2400), "grey").save(buffer, "JPEG", exif=exif.tobytes())
original = buffer.getvalue()
cleaned = clean_photo(original)


def describe(data):
    image = Image.open(io.BytesIO(data))
    return (
        f"{image.size}, {len(image.getexif())} metadata entries, {len(data) // 1024} KB"
    )


print("before:", describe(original))
print("after: ", describe(cleaned))

try:
    clean_photo(b"this is not a photo")
except InvalidPhoto as error:
    print(error)`,
          },
          {
            stepNumber: 5,
            title: "5. Through the API",
            explanation:
              "Submits voice audio and photo attachments through the FastAPI service endpoints.",
            code: `BASE = "http://127.0.0.1:8800"

with (AUDIO / "English.mp3").open("rb") as file:
    response = httpx.post(
        BASE + "/transcriptions", files={"audio": ("English.mp3", file)}, timeout=60
    )
voice = response.json()
voice

response = httpx.post(BASE + "/reports", json={"text": voice["text"]}, timeout=180)
report_id = re.search(r"r-\\w+", response.text).group()
report_id

files = {"photo": ("pothole.jpg", original, "image/jpeg")}
print(httpx.put(f"{BASE}/reports/{report_id}/photo", files=files).json())
print(httpx.get(f"{BASE}/reports/{report_id}").json()["has_photo"])

bad = {"photo": ("x.jpg", b"not a photo", "image/jpeg")}
response = httpx.put(f"{BASE}/reports/{report_id}/photo", files=bad)
print(response.status_code, response.json())`,
          },
        ],
      },
      {
        id: "phase12",
        phase: "12",
        title: "Phase 12: Tracing and evals",
        file: "12_tracing_and_evals.ipynb",
        desc: "LangSmith tracing, evaluation scoring, and regression baselines.",
        concept:
          "Tracing records every model call and step of a run, so you can see what happened. Evals score the agents on labelled reports, so you know whether a change made things better or worse.",
        agent:
          "Target workflow evaluated against curated ground-truth datasets.",
        whatToNotice: [
          "A trace shows how an answer was produced, not just the answer.",
          'The "missed" lines show exactly where the agent and the labels disagree.',
          "A low score can mean a bad label or a bad scorer, not only a bad agent. Check before blaming the agent.",
        ],
        steps: [
          {
            stepNumber: 1,
            title: "1. One traced run",
            explanation:
              "Triage and routing run on one labelled report (live wires near hospital). Trace is logged to smith.langchain.com.",
            code: `import json
import sys

import langsmith as ls

from community_voice.core.config import PROJECT_ROOT
from community_voice.core.tracing import load_env

sys.path.insert(0, str(PROJECT_ROOT))

from evals import scoring  # noqa: E402
from evals.run_evals import BASELINE, load_examples, target  # noqa: E402

load_env()  # puts .env into the environment so LangSmith can see it

example = load_examples()[4]
with ls.tracing_context(enabled=True, metadata={"demo": "phase-12"}):
    output = target(example["inputs"])
output`,
          },
          {
            stepNumber: 2,
            title: "2. Score it",
            explanation:
              "Each score compares agent answer with label. not scored means it does not apply.",
            code: `for evaluator in scoring.EVALUATORS:
    result = evaluator(output, example["outputs"])
    print(f"{evaluator.__name__:20}", result.get("score", "not scored"))`,
          },
          {
            stepNumber: 3,
            title: "3. The regression check",
            explanation:
              "The baseline holds accepted scores. A run fails if a score drops more than 0.10 below it.",
            code: `baseline = json.loads(BASELINE.read_text())
worse = {**baseline, "category": 0.6}
print("Pretend run:", scoring.regressions(worse, baseline))
print("Same as baseline:", scoring.regressions(baseline, baseline))`,
          },
          {
            stepNumber: 4,
            title: "4. The full evaluation",
            explanation:
              "Run all 20 reports from a terminal:\nuv run python -m evals.run_evals --refresh",
            code: `# Terminal execution command:
# uv run python -m evals.run_evals --refresh`,
          },
        ],
      },
    ],

    get currentModule() {
      return (
        this.modules.find((m) => m.id === this.activeModuleId) ||
        this.modules[0]
      );
    },

    getFullCode(mod) {
      return mod.steps.map((s) => s.code).join("\n\n");
    },
  }));
});

// background particles
(async () => {
  if (window.tsParticles) {
    await window.tsParticles.load("particles-container", {
      background: { color: { value: "transparent" } },
      fpsLimit: 60,
      particles: {
        color: { value: ["#ffffff", "#F26522"] },
        links: {
          color: "#ffffff",
          distance: 130,
          enable: true,
          opacity: 0.08,
          width: 1,
        },
        move: { enable: true, speed: 0.5 },
        number: { density: { enable: true, area: 900 }, value: 35 },
        opacity: { value: 0.25 },
        shape: { type: "circle" },
        size: { value: { min: 1, max: 2.5 } },
      },
    });
  }
})();
