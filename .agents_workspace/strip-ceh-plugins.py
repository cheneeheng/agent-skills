"""Drop stale @ceh-plugins keys from every .claude/settings.local.json under a root.

Dry-run by default; pass --apply to write. Other keys and other plugins are untouched;
a file left with an empty enabledPlugins keeps it (Claude Code repopulates it).
"""
import json, sys, pathlib

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
apply = "--apply" in sys.argv
for f in sorted(root.glob("*/.claude/settings.local.json")) + sorted(root.glob("*/*/.claude/settings.local.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    stale = [k for k in d.get("enabledPlugins", {}) if k.endswith("@ceh-plugins")]
    if not stale:
        continue
    print(f"{'strip' if apply else 'would strip'} {len(stale):2} from {f}  (other keys: {[k for k in d if k != 'enabledPlugins']})")
    if apply:
        for k in stale:
            del d["enabledPlugins"][k]
        f.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")
