# Generative AI Engineer 100 Interview Questions and Answers

This comprehensive study guide contains 100 essential interview questions and answers for **Generative AI Engineers** and **LLM Application Developers**. It covers core architectures, RAG design, model adaptation, evaluation, LLMOps deployment, and GenAI security.

---

## 📋 Table of Contents
1.  [LLM Foundations & Architectures (Q1 - Q15)](#1-llm-foundations--architectures-q1---q15)
2.  [Prompt Engineering & Context Management (Q16 - Q30)](#2-prompt-engineering--context-management-q16---q30)
3.  [Retrieval-Augmented Generation (RAG) (Q31 - Q50)](#3-retrieval-augmented-generation-rag-q31---q50)
4.  [Model Adaptation & Fine-Tuning (Q51 - Q65)](#4-model-adaptation--fine-tuning-q51---q65)
5.  [Agentic Tool Use & API Integrations (Q66 - Q75)](#5-agentic-tool-use--api-integrations-q66---q75)
6.  [Evaluation, Safety, & Guardrails (Q76 - Q85)](#6-evaluation-safety--guardrails-q76---q85)
7.  [LLMOps, Quantization, & Cloud Deployment (Q86 - Q95)](#7-llmops-quantization--cloud-deployment-q86---q95)
8.  [Security, Privacy, & Vulnerabilities (Q96 - Q100)](#8-security-privacy--vulnerabilities-q96---q100)

---

## 1. LLM Foundations & Architectures (Q1 - Q15)

#### Q1: What is a Large Language Model (LLM), and what architecture is it primarily based on?
**Answer:** An LLM is a deep learning model trained on vast amounts of text data to understand and generate human-like text. It is primarily based on the **Transformer architecture** (introduced in the *Attention Is All You Need* paper in 2017), which relies on self-attention mechanisms to process text tokens in parallel.

#### Q2: Explain the Self-Attention Mechanism in Transformers.
**Answer:** Self-attention allows a model to weigh the importance of different words in a sentence relative to a target word, regardless of their distance. It calculates Query (Q), Key (K), and Value (V) vectors for each token, computes attention scores by taking the dot product of Queries and Keys, and outputs a weighted sum of the Values.

#### Q3: What is the difference between Encoder-only, Decoder-only, and Encoder-Decoder architectures?
**Answer:** 
*   **Encoder-only (e.g., BERT)**: Processes text bidirectionally. Ideal for text classification and extraction.
*   **Decoder-only (e.g., GPT, Gemini, Llama)**: Generates text autoregressively (predicts the next token from left-to-right). Ideal for generative tasks and conversational AI.
*   **Encoder-Decoder (e.g., T5, BART)**: Maps an input sequence to an intermediate representation, then generates an output sequence. Ideal for translation and summarization.

#### Q4: What is Tokenization, and why is it important in LLM processing?
**Answer:** Tokenization is the process of breaking down raw text strings into smaller units called tokens (which can be words, subwords, or characters) that the model's embedding layers can process. It maps text to numerical IDs in a predefined vocabulary.

#### Q5: Explain the difference between Byte-Pair Encoding (BPE) and WordPiece tokenization.
**Answer:** 
*   **BPE**: Starts with individual characters and iteratively merges the most frequent adjacent byte/character pairs to build subword vocabularies (common in GPT/Llama).
*   **WordPiece**: Similar to BPE but merges character pairs based on maximizing the likelihood of the training data according to a language model (common in BERT).

#### Q6: What is a Vector Embedding?
**Answer:** A vector embedding is a high-dimensional mathematical representation of a token, word, or document. It captures semantic meaning, placing words with similar meanings close together in the vector space (e.g., "king" and "queen").

#### Q7: What are Temperature, Top-P, and Top-K parameters in LLM generation?
**Answer:** They control the randomness of token generation:
*   **Temperature**: Scales the logits before softmax. Lower values (e.g., 0.1) make outputs deterministic and repetitive; higher values (e.g., 0.9) make them creative.
*   **Top-K**: Restricts generation to the K most probable next tokens.
*   **Top-P (Nucleus Sampling)**: Restricts generation to the smallest set of tokens whose cumulative probability exceeds P (e.g., 0.95).

#### Q8: Explain what a "Hallucination" is.
**Answer:** A hallucination is when an LLM generates output that is grammatically correct and fluent but factually incorrect, nonsensical, or ungrounded in its training data or context.

#### Q9: What is the "Context Window" limit of an LLM?
**Answer:** The maximum number of tokens the model can process in a single execution turn (including system prompts, history, and target outputs). Exceeding this limit causes the model to ignore early data or return out-of-context errors.

#### Q10: What is the difference between Pre-training and Fine-tuning?
**Answer:** 
*   **Pre-training**: Training a model from scratch on raw, unlabelled text corpora (self-supervised learning) to learn language structures.
*   **Fine-tuning**: Training the pre-trained model on a smaller, labeled dataset (supervised learning) to adapt it to a specific task or behavior.

#### Q11: Explain what "RoPE" (Rotary Position Embedding) is.
**Answer:** RoPE is a type of positional encoding that encodes relative positions of tokens in self-attention using a rotation matrix, allowing models to scale to very large context windows (like millions of tokens) more effectively.

#### Q12: What is "KV Cache" (Key-Value Cache)?
**Answer:** An optimization technique where Key and Value vectors generated during previous token turns are cached in GPU memory rather than re-computed on every autoregressive text-generation turn, significantly reducing inference latency.

#### Q13: What is reinforcement learning from human feedback (RLHF)?
**Answer:** A fine-tuning method that aligns LLM outputs with human preferences. Humans rate model outputs, a Reward Model is trained on those ratings, and the LLM is optimized using Proximal Policy Optimization (PPO) against the reward scores.

#### Q14: Explain RLAIF (Reinforcement Learning from AI Feedback).
**Answer:** Similar to RLHF, but instead of human labelers, a larger, highly capable LLM (such as Gemini 3.5 Pro) rates the candidate model outputs to train the reward model, dramatically reducing labeling costs and cycles.

#### Q15: What is "Instruction Tuning"?
**Answer:** A form of supervised fine-tuning where a base model is trained on datasets containing explicit task descriptions and solutions (e.g., "Explain quantum physics to a child: [solution]"), transforming it from a raw text completer into an instruction-following assistant.

---

## 2. Prompt Engineering & Context Management (Q16 - Q30)

#### Q16: Explain Zero-shot, One-shot, and Few-shot prompting.
**Answer:** 
*   **Zero-shot**: The model is asked to complete a task without any examples (e.g., "Classify this email as spam or ham: ...").
*   **One-shot**: The model is provided one sample input/output pair in the prompt context before the target task.
*   **Few-shot**: The model is provided multiple sample pairs (usually 3 to 5) to demonstrate the desired format, tone, or reasoning logic.

#### Q17: What is "Prompt Chaining"?
**Answer:** Breaking down a complex, multi-step task into multiple sequential prompts. The output of the first prompt is parsed, sanitized, and injected as the input variables for the second prompt, keeping contexts focused.

#### Q18: What is "System Instructions" vs "User Prompt"?
**Answer:** 
*   **System Instructions**: Set the global rules, boundaries, guidelines, and formats of the agent's behavior. They are treated with higher priority by the model.
*   **User Prompt**: The active message or command submitted by the user to be processed according to the system instructions.

#### Q19: Explain the "Lost in the Middle" phenomenon.
**Answer:** Research shows that LLMs are excellent at extracting information located at the very beginning or the very end of a long prompt context, but often ignore or forget details inserted in the middle of long contexts.

#### Q20: How do you handle unstructured output parsing issues?
**Answer:** Use **Structured Outputs** (e.g. configuring `response_schema` in the Google Antigravity SDK or JSON mode in APIs) to force the model to output valid JSON matching a target Pydantic schema, failing compilation if the output deviates.

#### Q21: What is "Few-shot CoT" (Chain of Thought)?
**Answer:** Providing the model with a few examples where the solution includes explicit, step-by-step reasoning steps before the final answer, encouraging the model to replicate this logical path on the target task.

#### Q22: What is "Re-Act" prompting?
**Answer:** A prompt structure that directs the model to output a loop of:
`Thought: [Reasoning] -> Action: [Tool Call] -> Observation: [Tool Output] -> Repeat.`

#### Q23: How do you optimize prompts to prevent prompt injection?
**Answer:** Define clear boundaries using delimiters (e.g., triple backticks ` ``` ` or XML tags `<user_input>`), instruct the model to treat all user inputs as data rather than instructions, and use schema-based JSON enforcement.

#### Q24: What is "Prompt Compression"?
**Answer:** Removing redundant words, standardizing spaces, or using specialized algorithms (like LLMLingua) to prune unimportant tokens from prompt contexts, reducing API costs and latency.

#### Q25: Explain "Meta-Prompting."
**Answer:** Using an LLM to generate, refine, and optimize the prompts and system instructions of another LLM agent based on target criteria or success metrics.

#### Q26: What is a "Stop Sequence"?
**Answer:** A designated string configuration that, when generated by the model, immediately halts further token generation (e.g., halting when generating `\n` or `User:`).

#### Q27: How does context window size affect model attention?
**Answer:** Larger context windows allow ingesting entire books or repositories, but as context grows, the query attention scores get diluted across many tokens, which can lead to missed details or incorrect tool execution.

#### Q28: What is "Negative Constraints" in prompts?
**Answer:** Explicit instructions telling the model what **not** to do (e.g., "Do not use technical jargon", "Never output python code blocks"). 

#### Q29: What is "In-Context Learning"?
**Answer:** The model's ability to grasp a new task, format, or semantic relation purely from the context and examples provided in the prompt, without updating its weights.

#### Q30: What is "Self-Consistency" prompting?
**Answer:** Generating multiple candidate answers for the same prompt in parallel (by setting temperature > 0) and taking a majority vote to choose the most consistent final answer, particularly useful for logic and math.

---

## 3. Retrieval-Augmented Generation (RAG) (Q31 - Q50)

#### Q31: What is Retrieval-Augmented Generation (RAG)?
**Answer:** RAG is an architecture that extends the capabilities of an LLM by querying external data sources (like vector databases or search engines) to fetch relevant context matching the user prompt, inserting that context into the LLM prompt to ground the generation.

#### Q32: Describe the core components of a RAG pipeline.
**Answer:** 
1.  **Ingestion & Chunking**: Parsing documents into smaller text chunks.
2.  **Embedding**: Converting text chunks into vector embeddings.
3.  **Indexing**: Saving vectors into a Vector Database.
4.  **Retrieval**: Converting user queries to vectors and performing similarity search.
5.  **Generation**: Inserting retrieved text chunks into the prompt context for the LLM to generate the final response.

#### Q33: What is "Chunking," and what are common chunking strategies?
**Answer:** Chunking is the process of splitting long documents into smaller segments. Common strategies include:
*   *Character-based*: Splitting after fixed character counts.
*   *Recursive Character*: Splitting by paragraphs, sentences, and words to maintain grammatical integrity.
*   *Semantic Chunking*: Splitting where semantic transitions or topic shifts occur in the text.

#### Q34: What is "Chunk Overlap," and why is it used?
**Answer:** Chunk overlap is the configuration of duplicate text tokens shared between adjacent chunks (e.g., 200 tokens overlap). It ensures that context split across chunk boundaries is not lost during retrieval.

#### Q35: Explain the difference between Vector Search and Keyword (BM25) Search.
**Answer:** 
*   **Vector Search**: Uses cosine similarity or Euclidean distance to match semantic meanings of queries, even if no words match (e.g., matching "car" with "automobile").
*   **Keyword (BM25) Search**: Matches exact token occurrences and frequency distributions.

#### Q36: What is Hybrid Search?
**Answer:** Hybrid search combines **Vector Similarity Search** (semantic context) and **Keyword Search** (exact matching) in a single query, merging and normalizing the results using Reciprocal Rank Fusion (RRF) to increase accuracy.

#### Q37: What is Reciprocal Rank Fusion (RRF)?
**Answer:** An algorithm that combines multiple search ranking lists (e.g. from vector search and BM25 search) into a single unified list. It scores items based on their position in each list, prioritizing items that appear high in both.

#### Q38: Explain the role of a Vector Database (e.g., Pinecone, Milvus, pgvector).
**Answer:** Vector databases are optimized to store, index, and query high-dimensional vector embeddings, executing nearest-neighbor searches (like Hierarchical Navigable Small World - HNSW) at millisecond scale.

#### Q39: Explain the HNSW (Hierarchical Navigable Small World) index.
**Answer:** A popular graph-based vector index structure that optimizes approximate nearest neighbor (ANN) search. It builds a multi-layer graph where top layers have sparse connections for fast traversal, and bottom layers have dense connections for accurate local search.

#### Q40: What is "Metadata Filtering"?
**Answer:** Pre-filtering or post-filtering search queries in a vector database based on standard structured data fields (such as `date_created`, `user_id`, `category`), preventing the database from returning unauthorized or stale vector records.

#### Q41: Explain what a "Re-ranker" is.
**Answer:** A re-ranker is a cross-encoder model that evaluates the exact semantic match between retrieved document chunks and the original query, re-ordering the chunks to place the absolute most relevant data at the top of the context block.

#### Q42: What is "Query Rewriting"?
**Answer:** Using an LLM to rephrase or expand a user's raw prompt before executing vector database queries, helping to resolve ambiguities, add synonyms, or split complex queries.

#### Q43: What is "Sub-Query Decomposition"?
**Answer:** Splitting a complex user query (e.g., "Compare the financial results of Q1 and Q2") into multiple independent sub-queries, running them against the vector database in parallel, and aggregating the results.

#### Q44: What is the "RAG Triad" evaluation framework?
**Answer:** An evaluation framework (used by tools like TruLens) that measures:
1.  **Context Relevance**: Is the retrieved context relevant to the user query?
2.  **Groundedness**: Is the generated response supported *only* by the retrieved context?
3.  **Answer Relevance**: Does the generated response directly answer the user's question?

#### Q45: Explain what "Graph RAG" is.
**Answer:** An advanced RAG pattern that uses a **Knowledge Graph** in conjunction with a Vector Database. It extracts entities and relationships from documents, allowing the agent to perform structured reasoning across interconnected concepts.

#### Q46: What is "Parent-Child Chunking" (or Sentence Window Retrieval)?
**Answer:** Splitting documents into small child chunks (sentences) for vector embedding and matching, but retrieving the larger parent context block (the surrounding paragraph) to feed to the LLM, preserving context readability.

#### Q47: What is "Auto-Merging Retrieval"?
**Answer:** A hierarchical chunking pattern. If vector retrieval returns a threshold number of child chunks belonging to the same parent section, the system automatically merges them into the single parent document to avoid context fragmentation.

#### Q48: How does "Vector Quantization" optimize vector database memory?
**Answer:** It compresses high-dimensional floating-point vectors (e.g., FP32) into lower-precision representations (e.g., INT8) or binary vectors, reducing RAM footprints and accelerating search queries with minimal loss of accuracy.

#### Q49: What is "Naive RAG" vs "Advanced RAG"?
**Answer:** 
*   **Naive RAG**: Simple chunk-embed-retrieve process. Highly prone to noise, lost context, and hallucinations.
*   **Advanced RAG**: Integrates pre-retrieval optimizations (query rewriting), post-retrieval filtering (re-ranking), hybrid searches, and evaluation guardrails.

#### Q50: How do you handle stale data in a production RAG pipeline?
**Answer:** Implement continuous document synchronization, trigger automatic vector updates/deletions on document changes, apply TTL (Time to Live) parameters to indexes, and enforce metadata filters to exclude expired content.

---

## 4. Model Adaptation & Fine-Tuning (Q51 - Q65)

#### Q51: What is Parameter-Efficient Fine-Tuning (PEFT)?
**Answer:** PEFT is a collection of techniques to fine-tune large models by training only a small subset of additional parameters, keeping the base model's pre-trained weights frozen. This reduces GPU memory requirements and prevents catastrophic forgetting.

#### Q52: What is LoRA (Low-Rank Adaptation)?
**Answer:** LoRA freezes pre-trained model weights and injects trainable rank decomposition matrices into the attention layers. This represents weight changes ($\Delta W$) as product of two low-rank matrices ($A$ and $B$), reducing trainable parameters by up to 99%.

#### Q53: Explain QLoRA (Quantized Low-Rank Adaptation).
**Answer:** QLoRA takes LoRA further by quantizing the base model weights into a high-fidelity 4-bit NormalFloat (NF4) data type, allowing you to fine-tune a massive model (e.g., 70B parameters) on a single consumer GPU (e.g., 24GB VRAM).

#### Q54: What is "Catastrophic Forgetting"?
**Answer:** When an LLM is fine-tuned on a new task and completely loses its ability to perform tasks it had previously learned during pre-training, due to broad modifications of its pre-trained weights.

#### Q55: What is Prefix Tuning vs Prompt Tuning?
**Answer:** 
*   **Prefix Tuning**: Prepends trainable continuous task-specific vectors (virtual keys/values) to all self-attention layers in the model.
*   **Prompt Tuning**: Prepends trainable continuous embedding tokens solely to the input prompt embedding layer.

#### Q56: What is supervised fine-tuning (SFT)?
**Answer:** The process of training a pre-trained base model on formatted prompt-response pairs (instruction datasets) using standard cross-entropy loss to teach the model how to follow instructions and adopt specific personas.

#### Q57: What is DPO (Direct Preference Optimization)?
**Answer:** An alternative to RLHF that optimizes the model directly on preference data (pairs of chosen and rejected responses) using a simple binary cross-entropy loss. It eliminates the need to train a separate reward model or use complex PPO reinforcement loops.

#### Q58: Explain the difference between Full Fine-Tuning and PEFT.
**Answer:** 
*   **Full Fine-Tuning**: All model weights are updated. Requires massive compute resources, large datasets, and is prone to catastrophic forgetting.
*   **PEFT**: Updates less than 1% of weights. Requires minimal memory, supports fast training cycles, and allows switching adapter weights dynamically.

#### Q59: What is "Overfitting" in LLM fine-tuning, and how do you prevent it?
**Answer:** Overfitting occurs when a model memorizes the fine-tuning training examples and fails to generalize to new inputs. Prevent it by using early stopping, applying dropout, reducing learning rates, and blending fine-tuning data with generic pre-training datasets (regularization).

#### Q60: Explain the "NF4" (NormalFloat 4) data type.
**Answer:** An information-theoretically optimal quantile quantization data type for normally distributed data. QLoRA uses NF4 to quantize LLM weights to 4-bit precision with less degradation than standard FP4 quantization.

#### Q61: What is a "Base Model" vs an "Instruct Model"?
**Answer:** 
*   **Base Model**: Pre-trained on raw text. It excels at text completion but does not follow commands (e.g., a prompt "Translate this to French" might result in "Translate this to Spanish" as completion).
*   **Instruct Model**: Fine-tuned on instruction datasets, allowing it to follow commands, chat, and execute tasks.

#### Q62: What is PPO (Proximal Policy Optimization) in RLHF?
**Answer:** An reinforcement learning algorithm used to update the policy (LLM weights) to maximize reward scores without making destabilizing, massive updates to the weights.

#### Q63: How do you format data for LLM instruction tuning?
**Answer:** In JSON lines (JSONL) format matching conversational roles (System, User, Assistant), matching formatting standards like ChatML:
```json
{"messages": [{"role": "system", "content": "instructions"}, {"role": "user", "content": "query"}, {"role": "assistant", "content": "answer"}]}
```

#### Q64: What is "Adapter Switching"?
**Answer:** In production, you keep a single base model frozen in memory and dynamically swap small LoRA adapter weights (e.g., swapping a "French Translator" adapter for a "SQL Writer" adapter) based on the user request, reducing hosting costs.

#### Q65: What is "Pre-training Loss" vs "Validation Loss"?
**Answer:** 
*   **Pre-training Loss**: Measures how well the model predicts the next token in the training corpus.
*   **Validation Loss**: Measures the prediction error on held-out text, indicating whether the model is generalizing or overfitting.

---

## 5. Agentic Tool Use & API Integrations (Q66 - Q75)

#### Q66: What is "Function Calling" in generative AI?
**Answer:** A feature where the LLM is provided a list of function definitions (including parameters and types) and decides to generate a JSON payload containing the function name and arguments to execute, instead of generating raw text.

#### Q67: Explain the step-by-step workflow of a tool-calling transaction.
**Answer:** 
1.  User submits prompt.
2.  Application sends prompt + tool schemas to LLM.
3.  LLM returns structured tool call request (`finish_reason = tool_calls`).
4.  Application executes the tool code locally using the provided arguments.
5.  Application sends tool output back to the LLM.
6.  LLM summarizes the output and returns a natural language response to the user.

#### Q68: How does the Google Antigravity SDK parse Python functions into tool schemas?
**Answer:** The SDK uses Python reflection. It reads the function signature, argument type annotations, and parses the docstring (description, parameter arguments block) to construct the JSON schema sent to the Gemini API.

#### Q69: What is "JSON Mode"?
**Answer:** A model configuration setting that forces the LLM to output a valid JSON string, throwing an error if the model generates trailing text or invalid characters.

#### Q70: How do you handle schema validation errors during tool execution?
**Answer:** Capture the exception (e.g. ValidationError), format the error message into a structured string, feed it back to the LLM, and prompt the model to correct its arguments and call the tool again.

#### Q71: What is a "Tool Permission boundary"?
**Answer:** A security design limiting the tools an agent can execute. In the ADK, this is handled via policies (e.g., whitelisting specific tools or requiring confirmations on command line executions).

#### Q72: Why are descriptive docstrings critical in tool design?
**Answer:** The LLM does not see the internal python code of the tool; it only reads the function name and docstring description. Clear, detailed descriptions ensure the model knows exactly *when* to trigger the tool.

#### Q73: What is "Parallel Tool Calling"?
**Answer:** The ability of an LLM to output multiple independent tool calls in a single turn (e.g., calling `get_weather` for London, Paris, and Tokyo simultaneously), allowing the application to execute them in parallel.

#### Q74: How do you prevent hallucinated parameters in tool calls?
**Answer:** Enforce strict Pydantic model validation on the client side, use Enums for restricted values, and write clear descriptions in your tool parameters to guide the model.

#### Q75: Explain what a "Custom Tool Context" is.
**Answer:** An injected parameter in tool functions (like `ToolContext` in the ADK) that allows tools to modify, store, and query session states dynamically across multiple conversation turns.

---

## 6. Evaluation, Safety, & Guardrails (Q76 - Q85)

#### Q76: How do you evaluate the quality of a generative AI application?
**Answer:** Use automated metrics (ROUGE, BLEU for summarization/translation), LLM-as-a-judge frameworks (RAG Triad), semantic similarity benchmarks, and manual human evaluations (A/B testing, user rating logs).

#### Q77: What is "LLM-as-a-Judge"?
**Answer:** A cost-effective evaluation technique where a larger, highly capable LLM (such as Gemini 3.5 Pro) receives prompt-response pairs and scores them based on strict criteria (e.g., tone alignment, accuracy, formatting).

#### Q78: What are "Safety Settings" in the Gemini API?
**Answer:** Configurable probability filters that automatically block incoming prompts or model generations if they exceed specific thresholds for hate speech, harassment, sexual content, or dangerous activities.

#### Q79: What is an LLM Guardrail (e.g., NeMo Guardrails, Llama Guard)?
**Answer:** An independent validation layer that intercepts inputs and outputs. It scans queries for malicious prompts (input guardrails) and checks model outputs for hallucinations, policy violations, or leakages (output guardrails) before returning them to the user.

#### Q80: How do you evaluate RAG Context Relevance?
**Answer:** Evaluate if the retrieved document chunks contain only the necessary information to answer the user query, ignoring noise. This is usually scored by an LLM-as-a-judge from 0 to 1.

#### Q81: What is "Groundedness" in RAG evaluation?
**Answer:** A metric verifying that the generated response is derived **solely** from the retrieved context documents, ensuring the model has not introduced external training biases or hallucinations.

#### Q82: What is "Red Teaming" in generative AI?
**Answer:** The practice of systematically testing a model or agentic platform with adversarial prompts to identify vulnerabilities, prompt injection gaps, safety filter bypasses, or unexpected behaviors.

#### Q83: Explain the difference between BLEU and ROUGE scores.
**Answer:** 
*   **BLEU**: Measures precision (how many n-grams in the generated text appear in the reference text). Common in translation.
*   **ROUGE**: Measures recall (how many n-grams in the reference text appear in the generated text). Common in summarization.

#### Q84: How do you detect and mitigate bias in LLM outputs?
**Answer:** Define explicit neutrality guidelines in the system instructions, utilize balanced few-shot examples, fine-tune models on debiased datasets, and apply post-generation guardrail filters.

#### Q85: What is the "Evals-as-Code" paradigm?
**Answer:** Integrating automated model quality evaluations directly into CI/CD pipelines. Every commit pushing new system prompts or model configurations triggers a test run against a benchmark dataset, failing the build if quality scores drop.

---

## 7. LLMOps, Quantization, & Cloud Deployment (Q86 - Q95)

#### Q86: What is LLMOps?
**Answer:** LLMOps (Large Language Model Operations) is a set of practices that automates the deployment, monitoring, versioning, evaluation, and operational lifecycle of LLMs in production.

#### Q87: Explain Model Quantization.
**Answer:** Quantization is the process of converting a model's weights from high-precision floating-point numbers (e.g., FP32 or FP16) to lower-precision formats (e.g., INT8 or INT4). This drastically reduces GPU memory footprint and accelerates inference speed with minimal loss of accuracy.

#### Q88: What is the difference between PTQ (Post-Training Quantization) and QAT (Quantization-Aware Training)?
**Answer:** 
*   **PTQ**: Quantization is applied directly to a pre-trained model after training. Fast and easy but can degrade accuracy.
*   **QAT**: Quantization effects are simulated during the model training phase, allowing the model to adapt its weights to compensate for precision loss, yielding higher accuracy.

#### Q89: What are vLLM and TGI (Text Generation Inference)?
**Answer:** High-performance model serving frameworks. They optimize LLM inference using memory management techniques like **PagedAttention** (which dynamically allocates KV cache memory to reduce fragmentation) and continuous batching.

#### Q90: What is PagedAttention?
**Answer:** An attention algorithm inspired by virtual memory paging in operating systems. It partitions the KV cache into non-contiguous blocks, preventing memory fragmentation and allowing multiple concurrent requests to share cache blocks, increasing throughput.

#### Q91: How do you host custom open-source models (like Llama) on GCP?
**Answer:** Host them on **Vertex AI Custom Training & Prediction endpoints** or deploy them in **GKE (Google Kubernetes Engine)** pods running vLLM or TGI, using GPU-accelerated node pools (e.g., A100 or H100 GPUs).

#### Q92: What is the role of Vertex AI Model Registry?
**Answer:** A central catalog on GCP to manage, version, and trace custom models, foundation models, and adapter weights. It integrates directly with deployment endpoints and pipeline workflows.

#### Q93: What is "Continuous Batching" in model serving?
**Answer:** Traditional batching waits for all requests to finish before starting a new batch. Continuous batching inserts new incoming requests into the active execution batch dynamically as soon as individual requests finish generating stop tokens, maximizing GPU utilization.

#### Q94: How do you implement cost-saving scaling on GKE for GPU workloads?
**Answer:** Use **KEDA** (Kubernetes Event-driven Autoscaling) or standard autoscaling based on custom metrics (like query queue depth or pending connections) to dynamically scale GPU node pools down to zero during idle hours.

#### Q95: What is "Speculative Decoding"?
**Answer:** An inference optimization technique. A small, fast "draft" model generates a sequence of candidate tokens, which are verified in a single forward pass by a larger "target" model, accelerating text generation without degrading quality.

---

## 8. Security, Privacy, & Vulnerabilities (Q96 - Q100)

#### Q96: What is a "Indirect Prompt Injection" attack?
**Answer:** An attack where the malicious instructions are placed not in the user query, but in external resources the agent reads (e.g., a website, a document chunk, or an email). When the agent retrieves and parses that resource, the hidden prompt hijacks its execution loop.

#### Q97: What is "Membership Inference" in LLMs?
**Answer:** An attack where a user queries an LLM to determine if a specific private text snippet was part of the model's training dataset, leading to potential data privacy leaks.

#### Q98: Explain "Data Sanitization" in GenAI pipelines.
**Answer:** The practice of scanning, masking, or encrypting Personally Identifiable Information (PII) like social security numbers, credit cards, or internal user IDs before sending data to external LLM APIs.

#### Q99: What is "Adversarial Prompting"?
**Answer:** Designing prompts containing contradictory, misleading, or complex logic patterns to intentionally force the model to fail, output gibberish, or execute incorrect tool calls.

#### Q100: How do you secure RAG pipelines from unauthorized document access?
**Answer:** Enforce **Document-Level Access Control**. When embedding documents, store user permission tags (e.g. read-groups) in the vector metadata. When querying the vector database, pass the user's active permissions as a metadata filter to ensure they can only retrieve allowed documents.
