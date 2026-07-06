#!/usr/bin/env bash
set -euo pipefail

ROOT=/Users/jackgreenberg/Desktop/rank-and-rent
S=$ROOT/David/clones/scripts
PROJ=$ROOT/David/clones/extremebuildouts.com
REFHOST=extreme-reference
VOICE=$S/voice/construction-buildouts.json
PAGES="home=https://extremebuildouts.com/,about=https://extremebuildouts.com/about,contact=https://extremebuildouts.com/contact,index=https://extremebuildouts.com/projects,slug=https://extremebuildouts.com/projects/mechanical-room-buildout"

CFG=$PROJ/home.config.json
MAP=$S/relabel-map-$REFHOST.json
CAP=$ROOT/David/clones/_captures/$REFHOST

[ -f "$CFG" ] || { echo "MISSING $CFG"; exit 1; }
[ -f "$MAP" ] || { echo "MISSING $MAP"; exit 1; }

if [ ! -f "$CAP/public/home.html.ref" ]; then
  node "$S/faithful-home.mjs" --src "https://extremebuildouts.com/" --pages "$PAGES" --dir "$CAP"
fi

mkdir -p "$PROJ/public" "$PROJ/qa-out"
cp "$CAP"/public/*.html.ref "$PROJ/public/" 2>/dev/null || true
if [ -d "$CAP/public/assets-f" ]; then
  rm -rf "$PROJ/public/assets-f"
  cp -R "$CAP/public/assets-f" "$PROJ/public/assets-f"
fi
cp "$CAP"/qa-out/ref-*.png "$PROJ/qa-out/" 2>/dev/null || true

node "$PROJ/scripts/build-rich-taxonomy-content.mjs"
python3 "$S/normalize_content.py" "$PROJ" --voice "$VOICE"

rm -rf "$PROJ/public/ours"
mkdir -p "$PROJ/public/ours"
cp -R "$PROJ/public/images/." "$PROJ/public/ours/"

python3 "$S/relabel_engine.py" --config "$CFG" --map "$MAP" --voice "$VOICE"
rm -rf "$PROJ/public/assets-f/img" "$PROJ/public/assets-f/js"
python3 "$PROJ/scripts/add-project-gallery.py"
node "$PROJ/scripts/scrub-public-output.mjs"
python3 "$S/verify_site.py" "$PROJ" --map "$MAP" --json "$PROJ/qa-out/verify.json"
node "$S/qa_shots.mjs" "$PROJ" --port 4798

echo "BUILD COMPLETE - gates green. Human QA: open $PROJ/qa-out/CONTACT-SHEET.html"
