#!/bin/sh
# status.json is the single source of truth; this bakes it into status.js so the
# pages need no fetch (works on file://, on phones, and with any CSP).
cd "$(dirname "$0")"
printf 'window.STATUS=' > status.js
cat status.json >> status.js
printf ';\n' >> status.js
echo "status.js rebuilt from status.json"
