# TikZ-Hunter Frontend

This directory contains the React-based user interface for TikZ-Hunter.

## Quick Start

To set up the local development environment, follow these steps.

### 1. Create the React App

If you are starting from scratch, use `create-react-app` to bootstrap the project.

```bash
npx create-react-app . --template typescript
```

### 2. Install Dependencies

We'll need a WebSocket client library.

```bash
npm install use-websocket
```

### 3. Replace `src/App.tsx`

Replace the contents of `src/App.tsx` with the code below. This component fetches existing snippets and listens for new ones via WebSockets, displaying them in a real-time feed.

```typescript
// src/App.tsx
import React, { useState, useEffect } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws';

interface Snippet {
  uid: string;
  hash: string;
  status: string;
  source_url: string;
  created_at: string;
  snippet: {
    topic: string;
    reaction: string;
    particles: string[];
    description: string;
    tikz_code: string;
    process_type: string;
    source_type: string;
  };
}

const SnippetCard: React.FC<{ snippet: Snippet }> = ({ snippet }) => (
  <div className="card">
    <h3>{snippet.snippet.topic}</h3>
    <p><strong>Reaction:</strong> <code>{snippet.snippet.reaction}</code></p>
    <p><strong>Description:</strong> {snippet.snippet.description}</p>
    <pre><code>{snippet.snippet.tikz_code}</code></pre>
    <div className="meta">
      <span>Source: <a href={snippet.source_url} target="_blank" rel="noopener noreferrer">{snippet.snippet.source_type}</a></span>
      <span>Process: {snippet.snippet.process_type}</span>
      <span>Added: {new Date(snippet.created_at).toLocaleString()}</span>
    </div>
  </div>
);

function App() {
  const [snippets, setSnippets] = useState<Snippet[]>([]);
  const { lastJsonMessage, readyState } = useWebSocket<{ snippet: Snippet }>(WS_URL, {
    onOpen: () => console.log('WebSocket connection established.'),
    shouldReconnect: (closeEvent) => true,
  });

  useEffect(() => {
    // Fetch initial snippets
    fetch(`${API_URL}/api/snippets?limit=50`)
      .then(response => response.json())
      .then(data => setSnippets(data))
      .catch(error => console.error('Error fetching initial snippets:', error));
  }, []);

  useEffect(() => {
    if (lastJsonMessage && lastJsonMessage.snippet) {
      // Add the new snippet to the top of the list
      setSnippets(prevSnippets => [lastJsonMessage.snippet, ...prevSnippets]);
    }
  }, [lastJsonMessage]);

  const connectionStatus = {
    [ReadyState.CONNECTING]: 'Connecting',
    [ReadyState.OPEN]: 'Open',
    [ReadyState.CLOSING]: 'Closing',
    [ReadyState.CLOSED]: 'Closed',
    [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  }[readyState];

  return (
    <div className="App">
      <header className="App-header">
        <h1>TikZ-Hunter Dashboard</h1>
        <p>WebSocket Status: {connectionStatus}</p>
      </header>
      <main className="feed-container">
        {snippets.map(s => <SnippetCard key={s.hash} snippet={s} />)}
      </main>
    </div>
  );
}

export default App;
```

### 4. Basic Styling in `src/App.css`

Add some basic CSS to `src/App.css` to make the dashboard readable.

```css
/* src/App.css */
body {
  background-color: #282c34;
  color: white;
  font-family: sans-serif;
}
.App-header {
  text-align: center;
  padding: 20px;
  border-bottom: 1px solid #444;
}
.feed-container {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}
.card {
  background: #3c4049;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}
.card h3 {
  margin-top: 0;
  color: #61dafb;
}
.card pre {
  background: #20232a;
  padding: 15px;
  border-radius: 4px;
  white-space: pre-wrap;
  word-wrap: break-word;
}
.card .meta {
  font-size: 0.8em;
  color: #aaa;
  display: flex;
  justify-content: space-between;
}
.card .meta a {
  color: #61dafb;
}
```

### 5. Run the App

```bash
npm start
```