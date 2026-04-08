---
name: "llm-integration"
description: >
  Load this skill when integrating LLM calls into the application: constructing prompts, defining
  LLM output schemas, validating LLM responses, applying proposed events from LLM output, or
  handling LLM API errors. Auto-load whenever an LLM API call is written, an output model is
  defined, or proposed events from an LLM response are being applied to state.
---

# LLM Integration Safety

The LLM-proposes / backend-validates pattern, output schema requirements, invariant enforcement
before any state commit, and safety rules for logging and retrying. The LLM is a stateless
collaborator — it never has direct write access. All output must be validated against domain
invariants before any mutation occurs.

Read [../architecture-design/references/llm-integration.md](../architecture-design/references/llm-integration.md)
and apply the safety rules and validation pattern defined there.
