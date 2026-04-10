# High Level Design (HLD)

## 1. Introduction
The objective of this chatbot system is to interface with consumers to capture their complaints, classify the specific product the complaint is targeting, and seamlessly route this data to the correct department within the regulatory body.

## 2. Architecture Overview
The system follows a typical microservice architecture encompassing:
1. **User Interface (UI):** A web widget or messaging platform where consumers chat.
2. **Chatbot Service:** Powered by an LLM or NLU framework to manage dialogue state and handle user inputs.
3. **Classification Engine:** An ML service (using TF-IDF/Random Forest or a fine-tuned Transformer) that predicts the `Product` category and `Dispute` probability based on the gathered narrative.
4. **Data Store:** A database mapping unstructured chat logs to structural complaint records.

## 3. Data Flow
1. User initiates a chat.
2. Chatbot requests issue details organically.
3. Once the narrative is obtained, the Chatbot Service calls the Classification Engine.
4. Classification Engine returns product tags and metadata.
5. Chatbot confirms details with the user.
6. The system persists the complaint and pushes a routing event to the internal queuing system (e.g., Kafka / RabbitMQ).
