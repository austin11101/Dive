#!/bin/bash

echo "🚀 Starting CV Revamp Development Environment..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="20.19"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$NODE_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "⚠️  Node.js version $NODE_VERSION detected. Recommended: v$REQUIRED_VERSION or higher."
    echo "   You can continue, but some features might not work properly."
fi

echo "📦 Installing dependencies..."
npm run install:all

echo "🧹 Cleaning up cache files..."
npm run clean

echo "🔥 Starting development servers..."
echo "   Frontend: http://localhost:4200"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Start both servers concurrently
npm run dev 