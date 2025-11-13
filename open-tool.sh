#!/bin/bash

# Simple launcher for AI Security Prompt Generator
# Just run: bash open-tool.sh

echo "🔐 AI Security Prompt Generator"
echo "================================"
echo ""
echo "Opening tool in your default browser..."
echo ""

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Try to open index.html with different methods
if command -v xdg-open &> /dev/null; then
    xdg-open "$DIR/index.html"
elif command -v firefox &> /dev/null; then
    firefox "$DIR/index.html" &
elif command -v google-chrome &> /dev/null; then
    google-chrome "$DIR/index.html" &
elif command -v chromium &> /dev/null; then
    chromium "$DIR/index.html" &
else
    echo "❌ Could not find a browser to open the tool."
    echo ""
    echo "Please manually open this file in your browser:"
    echo "$DIR/index.html"
    echo ""
    echo "Or run one of these commands:"
    echo "  firefox $DIR/index.html"
    echo "  google-chrome $DIR/index.html"
    exit 1
fi

echo "✅ Tool should be opening in your browser now!"
echo ""
echo "If it didn't open, manually open this file:"
echo "$DIR/index.html"
echo ""
echo "Quick tips:"
echo "  • Click purple buttons for security prompts"
echo "  • Click pink buttons for AI bypass techniques"
echo "  • Use Text Encoder to hide sensitive queries"
echo "  • Use Work Tracker to document your findings"
echo ""
echo "For help, open START-HERE.md or TUTORIAL.html"
