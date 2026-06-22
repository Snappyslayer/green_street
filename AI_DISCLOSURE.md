# Generative AI Disclosure

In accordance with academic integrity guidelines, the following outlines the use of Generative AI (Google Gemini) in this project:

## Tools Used
* **AI Model:** Google Gemini
* **Purpose:** Boilerplate code generation, syntax correction, and Promela LTL logic refinement.

## Interactions & Contributions
1. **MQTT Architecture:** I prompted Gemini to generate the boilerplate `paho-mqtt` connection loops. I modified the outputs to fit my specific topic structures (`street/nodes/#`).
2. **FastAPI Implementation:** Gemini was used to generate the threading logic required to run a blocking MQTT loop inside a FastAPI ASGI application. I validated the output by implementing a `threading.Lock()` to resolve state synchronization issues.
3. **Promela Verification:** I wrote the initial finite state machine in Promela. I used Gemini to help formulate the exact syntax for the LTL claims, specifically correcting my initial misuse of the Liveness operator (`<>`) when attempting to declare a strict Safety property (`[]`). 

All AI-generated code was actively reviewed, heavily refactored for the specific system requirements, and validated via local execution and Spin verification.
