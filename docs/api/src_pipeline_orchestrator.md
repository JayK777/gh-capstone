# `src.pipeline.orchestrator`

orchestrator.py
~~~~~~~~~~~~~~~
Main SDLC Pipeline Orchestrator.

Drives the full 8-step lifecycle from a JIRA story to a GitHub PR.
Each step can also be run independently via the run_step() method.

---

## class `PipelineConfig`

Runtime configuration for the SDLC pipeline.

## class `SDLCOrchestrator`

Drives the 8-step Agentic SDLC pipeline end-to-end.

### `run_all(self)`

Execute all 8 steps in order. Returns the PR URL.

### `run_step(self, step_name)`

Run a single named step.
