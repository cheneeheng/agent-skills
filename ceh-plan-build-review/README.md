# ceh-plan-build-review

The plan-driven development loop as one plugin: **plan** a fullstack app (one release at a
time, or all the way to MVP in a single session), **build** it by implementing the plan
section by section, and **review** the implementation against the plan.

All four skills share the same plan document schema (`SKELETON.md` / `ITER_NN.md`, including
version-tagged families like `SKELETON_v2.md`), so artifacts produced by the planning skills
are directly consumable by the implement and review skills.

## Skills

| Skill | When it loads | What it does |
|-------|---------------|--------------|
| `plan-fullstack-app-iteratively` | You want to plan the next release, feature, or a greenfield skeleton | Produces one scoped plan artifact per session — a `SKELETON.md` or the next `ITER_NN.md` — never the finished product. |
| `plan-fullstack-app-to-mvp` | You want the complete build plan to a working MVP in one session | Produces the skeleton plus every iteration to MVP upfront; a complexity gate hands off to the iterative planner when upfront planning is unsafe. |
| `implement-from-plan` | You point at a plan and ask to build it | Implements a `SKELETON.md` / `ITER_NN.md` section by section in scope order (§01–§06), resolving iteration pointers to the authoritative spec. |
| `review-against-plan` | You ask to audit a plan against the code | Checks each in-scope section against the spec, finds gaps/deviations/errors, then fixes them. |

**Manual triggers**

- `plan-fullstack-app-iteratively` — `"plan the next feature"`, `"plan this iteration"`, `"create a skeleton plan"`, or describe one piece of work to plan.
- `plan-fullstack-app-to-mvp` — `"plan this whole app to MVP"`, `"plan everything upfront"`, `"lay out all the iterations"`.
- `implement-from-plan` — `"implement from plan"`, `"build from the plan"`, or point at a `SKELETON.md` / `ITER_NN.md` and ask to build it.
- `review-against-plan` — `"review against plan"`, `"verify the plan is implemented"`, or point at a plan file and ask to audit it.

## The loop

```
plan-fullstack-app-iteratively ──┐
                                 ├──► SKELETON.md / ITER_NN.md ──► implement-from-plan ──► review-against-plan
plan-fullstack-app-to-mvp ───────┘
```

The plan document schema is defined in `skills/implement-from-plan/references/plan-schema.md`
(consumed by `implement-from-plan` and `review-against-plan`); the two planning skills carry
their own `references/section-specs.md` describing the same artifact format from the
producer side.

> **Intentional duplication.** The reference files are duplicated across the skills on purpose:
> the skills are also used standalone in other tools outside this plugin, so each skill folder
> carries its own copy of the shared material instead of pointing at a common file. This is the
> **only** sanctioned exception to the repo's normal rule against duplicating reference material;
> the copies are registered in the root `CROSS_REFERENCES.md` ("Plan document schema" entry) and
> must be kept in sync.
