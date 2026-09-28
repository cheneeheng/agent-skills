import type { ComponentType } from "react";

// A canvas component the agent can place by calling a frontend tool of the same name.
// `parameters` is the JSON Schema of the tool arguments; the component receives them as props.
export type CanvasComponent = {
  name: string;
  description: string;
  parameters: Record<string, unknown>;
  // Props are validated only by the agent honouring `parameters`.
  Component: ComponentType<any>;
};

// Empty on purpose: this is the blank canvas. Register components here.
export const registry: CanvasComponent[] = [];
