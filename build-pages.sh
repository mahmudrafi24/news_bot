#!/bin/sh
set -eu

cd "$(dirname "$0")"
mkdir -p public
cp site/index.html site/october-market-review.html site/market-brief-2026-11-18.html site/style.css site/share.js public/
