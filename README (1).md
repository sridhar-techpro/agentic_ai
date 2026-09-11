# WebGenie — Agentic Browser Automation Architecture

## Overview

WebGenie is an agentic browser automation and analysis system designed to understand user prompts, analyze multiple browser tabs and documents, apply relevant skill files and application context, and execute browser or enterprise automation tasks.

The proposed architecture uses **Cline-based agents in two places**:

1. **Extension-side Cline** — specialized for browser understanding and element discovery.
2. **Backend Cline** — specialized for planning, reasoning, skills, application context, and orchestration.

A **Native Messaging Host** provides a secure local boundary for credential/token handling and optional local-machine capabilities.

The backend runs the centralized agent infrastructure, model integration, scheduling, policies, persistence, and enterprise integrations.

---

## Architecture Goals

- Analyze multiple open browser tabs based on user intent.
- Identify relevant UI elements instead of blindly selecting the first N elements.
- Analyze opened documents and application context.
- Dynamically identify and apply relevant skill files.
- Support agent mode for multi-step browser automation.
- Support scheduled and recurring agent workflows.
- Support Azure OpenAI and Claude model endpoints.
- Keep sensitive long-lived credentials out of backend caches.
- Provide centralized enterprise policy, authentication, auditing, and model routing.
- Avoid introducing a Vector DB unless scale actually requires semantic retrieval.

---

# High-Level Architecture

```text
                              User
                               |
                               v
                    +----------------------+
                    |   WebGenie Extension |
                    |----------------------|
                    | UI / User Prompt     |
                    | Tab Access            |
                    | DOM / Page Context    |
                    | Browser Automation    |
                    +----------+-----------+
                               |
                  +------------+-------------+
                  |                          |
                  v                          v
        +------------------+       +----------------------+
        | Extension Cline  |       | Native Messaging Host|
        |------------------|       |----------------------|
        | Browser Agent    |       | Credential Broker    |
        | Element Discovery|       | OS Credential Store  |
        | Tab Analysis     |       | Optional OS Tools    |
        +--------+---------+       +----------+-----------+
                 |                            |
                 +-------------+--------------+
                               |
                               v
                     +-------------------+
                     | WebGenie Backend  |
                     | ECS / FastAPI     |
                     |-------------------|
                     | Backend Cline     |
                     | Agent Orchestration|
                     | Skills            |
                     | App Context       |
                     | Scheduler         |
                     | Policy / Auth     |
                     | Audit / State    |
                     +---------+---------+
                               |
                     +---------+---------+
                     |                   |
                     v                   v
              +------------+       +------------+
              | Azure      |       | Claude     |
              | OpenAI     |       | Endpoints  |
              +------------+       +------------+
```

---

# Component Responsibilities

## 1. WebGenie Browser Extension

The extension owns browser-specific capabilities.

### Responsibilities

- Receive user prompts.
- Maintain browser/session UI state.
- Discover open tabs.
- Extract page/DOM/accessibility information.
- Perform browser navigation.
- Click elements.
- Fill forms.
- Extract page content.
- Read selected text.
- Capture relevant document/page context.
- Request user approval for sensitive actions.
- Communicate with the backend.
- Communicate with the Native Messaging Host.

The extension should **not** contain long-lived enterprise credentials.

---

# 2. Extension-Side Cline

The extension-side Cline is a specialized **Browser Agent**.

Its main purpose is not broad business reasoning. Its job is to understand the browser environment and identify what is relevant to the user's task.

### Example

User:

> Click the Submit Order button for the Acme order.

A naive implementation might do:

```text
querySelectorAll("button")
    -> take first 20 buttons
    -> send them to the model
```

Instead:

```text
DOM
  |
  v
Interactive element extraction
  |
  v
Semantic candidate generation
  |
  v
Extension Cline
  |
  v
Relevant element selection
```

Example candidate:

```json
{
  "id": "el_482",
  "role": "button",
  "text": "Submit Order",
  "ariaLabel": "Submit Acme Order",
  "nearbyText": "Acme Corp",
  "visible": true,
  "enabled": true
}
```

Cline can determine that `el_482` is the relevant target.

### Extension Cline responsibilities

- Understand user intent at the browser level.
- Identify relevant tabs.
- Identify relevant page sections.
- Identify relevant UI elements.
- Resolve ambiguous element references.
- Determine which page/document contains relevant information.
- Support browser-specific multi-step operations.
- Return structured observations/actions to the backend agent.

### Important design principle

Do not send the entire DOM to the model whenever possible.

Use:

```text
DOM
 -> Accessibility tree
 -> Interactive elements
 -> Semantic metadata
 -> Candidate filtering
 -> Cline
```

This reduces token usage, latency, and hallucination risk.

---

# 3. Backend — ECS / FastAPI

The backend is the centralized WebGenie control plane.

### Responsibilities

- Backend Cline runtime.
- Agent orchestration.
- Model routing.
- Azure OpenAI integration.
- Claude integration.
- Authentication and authorization.
- Enterprise policy enforcement.
- Scheduler.
- Persistent agent/task state.
- Audit logging.
- Usage/token tracking.
- Enterprise integrations.
- Skill catalog.
- Application context management.
- Communication with browser extensions.

The backend should generally be the location for long-running agent processes and centralized enterprise functionality.

---

# 4. Backend Cline

Backend Cline is the primary **Reasoning and Orchestration Agent**.

Its responsibilities include:

- Understand the complete user objective.
- Plan multi-step workflows.
- Determine required skills.
- Analyze application context.
- Analyze multiple documents.
- Determine what browser information is required.
- Ask the extension-side agent for relevant browser context.
- Decide which tools to invoke.
- Execute enterprise integrations.
- Maintain task/agent state.
- Decide when a workflow is complete.

### Example

User:

> Analyze the three open API documentation tabs, compare authentication approaches, check our security skills, and update the Jira ticket with the recommendation.

Backend Cline can reason:

```text
1. Need API documentation.
2. Ask extension to identify relevant tabs.
3. Read relevant content.
4. Identify authentication-related skills.
5. Read those skill files.
6. Compare the approaches.
7. Produce recommendation.
8. Ask for Jira update.
9. Apply policy/approval.
10. Update Jira.
```

---

# 5. Two-Agent Model

The two Cline instances should **not behave as two independent general-purpose agents**.

They should have clearly separated responsibilities.

```text
                 Backend Cline
                Reasoning Agent
                      |
                Agent Protocol
                      |
                      v
              Extension Cline
               Browser Agent
```

## Backend Cline

Focus:

- Planning
- Reasoning
- Skills
- Application context
- Business logic
- Orchestration
- Enterprise actions

## Extension Cline

Focus:

- Browser context
- Tabs
- DOM
- Accessibility information
- Element discovery
- Browser actions
- Page/document extraction

This separation keeps the browser agent focused and prevents unnecessary browser data from being sent to the backend.

---

# 6. Agent Communication Protocol

The agents should communicate using structured messages rather than unrestricted natural-language instructions.

Example action:

```json
{
  "action": "CLICK",
  "target": {
    "elementId": "el_482",
    "confidence": 0.96
  },
  "reason": "Submit Order button associated with Acme"
}
```

Example result:

```json
{
  "success": true,
  "elementId": "el_482",
  "result": "Order submitted"
}
```

For browser context:

```json
{
  "request": "GET_RELEVANT_TABS",
  "intent": "Find API authentication documentation relevant to OAuth"
}
```

Response:

```json
{
  "tabs": [
    {
      "tabId": 12,
      "title": "Authentication API",
      "relevance": 0.94
    },
    {
      "tabId": 18,
      "title": "OAuth Integration Guide",
      "relevance": 0.91
    }
  ]
}
```

---

# 7. Multitab Analysis

WebGenie should not blindly send all open tabs to the backend.

Example:

```text
Tab 1 -> Product documentation
Tab 2 -> API documentation
Tab 3 -> Internal application
Tab 4 -> Security policy
Tab 5 -> Jira
```

User:

> Compare the authentication implementation with our security requirements.

The system should determine:

```text
Relevant:
  Tab 2 -> API documentation
  Tab 4 -> Security policy
  Tab 3 -> Internal application

Potentially irrelevant:
  Tab 1
  Tab 5
```

Flow:

```text
User Prompt
    |
    v
Backend Cline
    |
    | "Find relevant tabs"
    v
Extension Cline
    |
    +--> Tab 1  X
    +--> Tab 2  YES
    +--> Tab 3  YES
    +--> Tab 4  YES
    +--> Tab 5  X
    |
    v
Relevant content
    |
    v
Backend Cline
```

This provides intent-driven context selection rather than arbitrary tab selection.

---

# 8. Skills Architecture

Skills should be treated as structured knowledge/instructions that the Backend Cline can discover and apply.

Example:

```text
skills/
  security/
    authentication.md
    authorization.md
    oauth.md

  browser/
    navigation.md
    form-automation.md

  application/
    onboarding.md
    customer-management.md
```

A lightweight skill catalog can be maintained:

```json
{
  "skill": "security-review",
  "description": "Security requirements for web applications",
  "tags": [
    "security",
    "authentication",
    "authorization"
  ],
  "files": [
    "security/authentication.md",
    "security/authorization.md"
  ]
}
```

The agent can:

```text
User request
   |
   v
Backend Cline
   |
   v
Identify relevant skills
   |
   v
Read only relevant skill files
   |
   v
Apply skill instructions
```

---

# 9. Vector DB Decision

A Vector DB is **not required initially**.

The first implementation can use:

```text
Skill catalog
     |
     v
Metadata / tags / names
     |
     v
Cline identifies relevant skills
     |
     v
Read relevant files
```

This avoids creating a traditional:

```text
Embedding
   ->
Vector DB
   ->
Similarity Search
   ->
RAG
   ->
LLM
```

architecture before it is actually needed.

## Why avoid it initially?

- Less infrastructure.
- Lower operational complexity.
- Easier debugging.
- Skills remain human-readable.
- Agent can reason over the actual source files.
- Easier skill updates.
- No embedding synchronization problem.

## When should Vector DB be considered?

If the system eventually has:

- thousands of skills,
- very large application documentation,
- millions of lines of contextual information,
- large historical knowledge bases,

then semantic retrieval can be introduced as an optimization.

The architecture can evolve to:

```text
Backend Cline
     |
     +--> Skill Catalog
     |
     +--> Keyword / metadata retrieval
     |
     +--> Vector Search (optional)
     |
     +--> Application context
```

Vector search should be an implementation optimization, not a mandatory architectural dependency.

---

# 10. Native Messaging Host

The Native Messaging Host should be kept small and security-focused.

Its primary responsibility is to provide a local credential boundary.

```text
WebGenie Extension
       |
       v
Native Messaging
       |
       v
Native Host
       |
       v
OS Credential Manager
```

### Recommended responsibilities

```text
getAccessToken(resource)
refreshAccessToken(resource)
getCredentialStatus(resource)
deleteCredential(resource)
```

The Native Host should not initially become another full agent runtime.

Avoid making it responsible for:

```text
runAgent()
execute arbitrary commands()
read arbitrary filesystem()
run Python()
```

unless those capabilities are explicitly required and protected by a strong security model.

---

# 11. OBO / Token Handling

The architecture should avoid storing long-lived user credentials in backend caches.

Conceptually:

```text
Extension
    |
    v
Native Host
    |
    v
OS Secure Credential Store
    |
    v
Obtain/refresh short-lived access token
    |
    v
Backend
```

Important:

An Entra ID OBO access token is normally a short-lived token issued for a specific downstream audience. It should not be treated as a permanent credential.

The Native Host should therefore act as a **credential/token broker**, while the backend receives only the short-lived token required for a particular operation.

---

# 12. Agent Mode and Automation

WebGenie should support both interactive and scheduled agent workflows.

## Interactive

```text
User
 |
 v
Prompt
 |
 v
Backend Cline
 |
 v
Extension Cline
 |
 v
Browser action
 |
 v
Result
 |
 v
Backend Cline
 |
 v
Next action
```

## Scheduled

```text
Scheduler
    |
    v
Backend Cline
    |
    v
Determine required context
    |
    v
Extension online?
    |
    +---- YES ---> Request browser context
    |
    +---- NO ----> Continue backend-only task
                    or request user/browser availability
```

The backend is the preferred location for scheduling because it can run independently of the browser process.

---

# 13. Backend + Native Host Together

Both can coexist.

```text
                         WebGenie
                            |
             +--------------+--------------+
             |                             |
             v                             v
       Chrome Extension              Native Host
             |                             |
       Browser tools                Credential tools
             |                             |
             +--------------+--------------+
                            |
                            v
                     Backend / ECS
                            |
                      Backend Cline
                            |
             +--------------+--------------+
             |                             |
             v                             v
          Scheduler                  Enterprise APIs
             |
             v
       Azure OpenAI / Claude
```

### Backend handles

- Scheduling
- Agent execution
- Enterprise integrations
- Authentication
- Authorization
- Policy
- Audit
- Model routing
- Persistent task state

### Native Host handles

- Local secure credentials
- Token acquisition/refresh
- Optional local OS capabilities

### Extension handles

- Browser context
- Tabs
- DOM
- Browser actions
- User interaction

---

# 14. Model Provider Abstraction

The backend should have a model-provider abstraction so WebGenie is not coupled to one model vendor.

```text
                  Model Gateway
                       |
          +------------+------------+
          |                         |
          v                         v
     Azure OpenAI                Claude
          |                         |
     GPT deployment         Anthropic/Azure
```

Example conceptual interface:

```python
class ModelProvider:
    async def chat(self, messages, tools):
        ...

    async def stream(self, messages, tools):
        ...
```

Then implementations can support:

```text
AzureOpenAIProvider
ClaudeProvider
```

This allows model selection based on:

- task type
- organization policy
- cost
- latency
- model capability
- user/team configuration

---

# 15. Tool Architecture

The Backend Cline should see capabilities as tools.

### Browser tools

```text
get_open_tabs()
get_tab_content()
search_tabs()
find_element()
click_element()
fill_element()
navigate()
extract_document()
```

### Native tools

```text
get_access_token()
refresh_access_token()
get_credential_status()
```

### Backend tools

```text
read_skill()
search_skills()
get_application_context()
create_jira_ticket()
update_jira_ticket()
send_notification()
schedule_task()
```

The agent chooses the tool; each tool executes within its appropriate security boundary.

---

# 16. Security Boundaries

Recommended boundaries:

```text
                 +-----------------------+
                 |       Browser         |
                 | Untrusted web content  |
                 +-----------+-----------+
                             |
                       Extension
                             |
                  +----------+----------+
                  |                     |
                  v                     v
           Browser tools          Native Host
                                        |
                                        v
                               Secure Credential Store
                                        |
                                        v
                                  Short-lived token
                                        |
                                        v
                                  Backend API
                                        |
                              +---------+---------+
                              |                   |
                              v                   v
                         Agent/Policy          Model API
```

Important principles:

1. Do not place long-lived provider credentials in the extension.
2. Do not expose unrestricted OS commands to the agent.
3. Require approval for sensitive browser/enterprise actions.
4. Validate tool arguments server-side.
5. Enforce authorization before executing enterprise actions.
6. Log security-sensitive actions.
7. Keep browser-originated content separate from trusted system instructions.
8. Treat page content as potentially untrusted input.

---

# 17. Recommended Initial Implementation

Do not implement everything simultaneously.

## Phase 1 — Browser Agent

```text
Extension
   |
   +--> DOM candidate extraction
   |
   +--> Extension Cline
   |
   +--> Browser actions
```

Focus on:

- Multitab analysis
- Relevant element selection
- Page/document extraction
- User prompt interpretation

## Phase 2 — Backend Agent

```text
Extension
    |
    v
FastAPI
    |
    v
Backend Cline
    |
    +--> Skills
    +--> Application context
    +--> Model providers
```

## Phase 3 — Native Messaging

Add:

```text
Extension
    |
    v
Native Host
    |
    v
OS Credential Manager
```

for secure local credential/token handling.

## Phase 4 — Automation

Add:

```text
Scheduler
   |
   v
Backend Cline
   |
   +--> Extension
   +--> Native Host
   +--> Enterprise tools
```

## Phase 5 — Retrieval Optimization

Only when the knowledge base becomes large:

```text
Skill Catalog
     +
Metadata Search
     +
Optional Vector Search
```

---

# 18. Key Architectural Decision

The recommended design is:

> **Cline is the agent framework, not the browser automation layer.**

WebGenie owns the tools and security boundaries.

```text
Cline
  = reasoning + planning + orchestration

WebGenie Extension
  = browser context + browser execution

Native Host
  = local credential/token boundary

FastAPI/ECS
  = centralized agent infrastructure + scheduler +
    policy + persistence + enterprise integrations

Azure OpenAI / Claude
  = model providers
```

This keeps the architecture modular and allows each component to evolve independently.

---

# 19. Target Architecture

```text
                           USER
                            |
                            v
                  +---------------------+
                  | WebGenie Extension  |
                  +----------+----------+
                             |
                +------------+------------+
                |                         |
                v                         v
       +------------------+     +--------------------+
       | Extension Cline  |     | Native Messaging   |
       | Browser Agent    |     | Host               |
       +--------+---------+     +---------+----------+
                |                         |
                |                    OS Credential
                |                       Manager
                |                         |
                +------------+------------+
                             |
                             v
                   +---------------------+
                   | WebGenie Backend    |
                   | ECS / FastAPI       |
                   +----------+----------+
                              |
                     +--------+--------+
                     |                 |
                     v                 v
             +---------------+   +------------+
             | Backend Cline  |   | Scheduler  |
             +-------+-------+   +------+-----+
                     |                  |
          +----------+----------+       |
          |          |          |       |
          v          v          v       |
       Skills    App Context  Tools     |
          |          |          |       |
          +----------+----------+-------+
                     |
                     v
              +--------------+
              | Model Gateway|
              +------+-------+
                     |
             +-------+-------+
             |               |
             v               v
        Azure OpenAI       Claude
```

---

## Summary

The recommended WebGenie architecture is a **hybrid agent architecture**:

- **Extension Cline** handles browser-specific reasoning and relevant element/tab discovery.
- **Backend Cline** handles deeper reasoning, skills, application context, planning, and orchestration.
- **Native Messaging Host** provides a small local security boundary for credential/token management and optional OS capabilities.
- **FastAPI/ECS** hosts centralized agent infrastructure, scheduler, policy, persistence, audit, and enterprise integrations.
- **Azure OpenAI and Claude** are accessed through a provider abstraction.
- **Vector DB is optional**, not required for the first implementation.
- **Skills should initially be discovered through a catalog/metadata approach and read directly by the agent.**
- The two Cline instances should communicate through a **structured agent/tool protocol**, not operate as unrelated autonomous agents.

This architecture provides a path from a browser-only assistant to a full enterprise agent capable of browser automation, local credential handling, application-context reasoning, skills-based workflows, and scheduled automation.
