### 📄 Spec-Driven Development (SDD) - Excalidraw Customizado

#### 1. Visão Geral da Arquitetura
A aplicação utilizará uma arquitetura cliente-servidor dividida em três pilares principais:
* **Frontend (Interface):** Aplicação React encapsulando o pacote oficial `@excalidraw/excalidraw`. Responsável por capturar os eventos de desenho e empacotar o estado em formato JSON.
* **Backend (API):** Desenvolvido em Python utilizando o framework **FastAPI**. Responsável por receber, validar e armazenar os dados do frontend.
* **Inteligência Artificial:** Integração com o framework **Agno**, que processará o JSON dos desenhos para extrair textos e formas, atuando como um assistente de diagramação.

#### 2. Modelagem de Dados (Banco de Dados)
Para iniciar e facilitar os testes no Colab, usaremos o SQLite. A tabela principal será a de `projetos` (que depois pode virar uma migration formal usando ferramentas como o Alembic no ecossistema Python).

**Tabela: `projetos`**
* `id`: String (UUID) - Identificador único do desenho.
* `nome_projeto`: String - Nome dado ao diagrama.
* `elementos_json`: JSON - O payload bruto gerado pelo Excalidraw contendo coordenadas, formas e textos.
* `data_criacao`: DateTime.
* `data_atualizacao`: DateTime.

#### 3. Contratos da API (Rotas Backend)
O Backend em FastAPI irá expor os seguintes endpoints principais:

* **`POST /api/projetos/salvar`**
    * **Ação:** Cria um novo projeto ou salva uma versão nova.
    * **Payload esperado (Frontend envia):** 
        ```json
        {
          "nome_projeto": "Meu Fluxograma de Teste",
          "elementos_json": [{ "type": "rectangle", "x": 100, "y": 200, "width": 50 }]
        }
        ```
    * **Retorno:** `200 OK` com o `id` do projeto gerado.

* **`GET /api/projetos/{id}`**
    * **Ação:** Recupera o JSON do banco para o Excalidraw renderizar novamente na tela.
    * **Retorno:** O objeto JSON completo do projeto salvo.

* **`POST /api/agente/analisar`**
    * **Ação:** Envia os elementos do desenho atual para o Agente Agno.
    * **Payload esperado:** Apenas a lista de elementos JSON do desenho.
    * **Retorno:** String contendo a análise ou sugestão gerada pela IA.
