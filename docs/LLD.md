# Low Level Design (LLD)

## 1. Main Components

### 1.1 `bot.dialogue_manager`
Manages the state of the conversation using LangChain concepts. Tracks missing entities that need to be collected (e.g., Company Name, Incident Date, Core Issue).
- **Functions:**
  - `process_message(session_id, user_message)`: Takes the user input and generates the next system response.
  - `extract_entities(text)`: Runs NER or a customized prompt to pull out key fields.

### 1.2 `models.classifier`
Handles text classification locally.
- **Functions:**
  - `predict_product(complaint_text) -> str`: Uses the trained ML model to output the product category.
  - `predict_dispute_risk(complaint_text, metadata) -> float`: Calculates the probability of a consumer dispute.

### 1.3 `api.routes`
FastAPI routes that serve the chatbot to the frontend.
- **Endpoints:**
  - `POST /chat`: Receives incoming messages and returns the bot's response.
  - `GET /health`: Health check endpoint.

## 2. Sequence Diagram
*(To be detailed with Mermaid/PlantUML upon further implementation)*

## 3. Database Schema
- **Conversations:** `session_id`, `created_at`, `status`
- **Messages:** `message_id`, `session_id`, `role`, `content`, `timestamp`
- **Complaints:** `complaint_id`, `session_id`, `predicted_product`, `narrative`, `routed_to`
