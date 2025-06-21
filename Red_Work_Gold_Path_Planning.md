## Red Work (Gold Path) Planning

This document outlines the technical objectives, requirements, and roadmap for transitioning Sonny from its current **Silver Calx** state to the fully autonomous and symbolic **Golden Calx**.

### 1. Technical Objectives and Capabilities
- **Proactive Multi-Step Reasoning**: Enable Sonny to autonomously generate, sequence, and execute multi-step tasks without manual prompts.
- **Advanced Symbolic AI**: Expand the `SymbolicState` to support complex event graphs, inference rules, and automated knowledge enrichment.
- **Deep Autonomous Integration**: Integrate backend agents, Codex-powered code generation, and desktop automation into cohesive autonomous workflows.
- **Self-Improving Code Generation**: Implement feedback loops where Sonny evaluates and refines generated scripts based on runtime results.

### 2. Technical Requirements
- **LLMClient Enhancements**: Upgrade to support streaming responses, cancellation, and plugin interfaces for tool calls.
- **SymbolicState Augmentation**: Support nested states, temporal reasoning, and distributed multi-agent synchronization.
- **Prompt-Chaining Framework**: Build reusable templates and chains for dynamic context injection, plan decomposition, and summarization.
- **Backend Orchestration**:
  - Task scheduling and background job management (e.g., Celery, APScheduler).
  - WebSocket or SSE endpoints for real-time UI updates.
- **Frontend Integration Points**:
  - Live plan visualization and step-by-step execution controls.
  - Enhanced error reporting and recovery UI components.
- **Codex/OpenAI API Integrations**: Leverage function-calling, fine-tuning, and embeddings for domain-specific reasoning.

### 3. Roadmap to Golden Calx
1. **Proactive Planner Module**: Design and implement a planning engine to decompose high-level goals into subtasks.
2. **Streaming & Callbacks**: Extend `LLMClient` to stream tokens and support callback hooks for tool invocations.
3. **Stateful Execution Layer**: Build a robust `ExecutionManager` that tracks task progress, state transitions, and rollback.
4. **Real-Time UI Updates**: Integrate WebSockets into Streamlit or migrate to a lightweight web UI for live plan tracking.
5. **Autonomous Code Validation**: Add automatic test generation and validation of generated scripts before execution.
6. **End-to-End Integration Tests**: Develop scenario-based tests covering complex autonomous workflows.

_Next Steps_: Assign development milestones, finalize technical designs, and begin iterative sprints toward Golden Calx.