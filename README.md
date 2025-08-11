# Agentic API Tester

## Overview
Agentic API Tester is a React-based tool for creating, running, and managing API tests with smart assertions and AI-powered suggestions. It provides a user-friendly interface for configuring API requests, validating responses, and automating test workflows.

## Features
- Create, edit, and delete API tests
- Configure HTTP method, URL, headers, and body
- Add and manage assertions for response validation
- Run individual or all tests
- Import/export tests as JSON
- Export test results as Word documents
- AI-powered test and assertion suggestions
- View detailed test results and next recommended API calls

## Setup Instructions
1. **Install dependencies:**
   ```bash
   npm install
   ```
2. **Ensure TypeScript and React support:**
   - Your project should support `.tsx` files.
   - Check `tsconfig.json` for:
     ```json
     {
       "compilerOptions": {
         "jsx": "react-jsx",
         "lib": ["dom", "es2015"],
         "module": "ESNext",
         "moduleResolution": "node"
       }
     }
     ```
   - In `package.json`, set:
     ```json
     {
       "type": "module"
     }
     ```
3. **Start the development server:**
   ```bash
   npm start
   ```

## Usage
### AgenticApiTester.tsx
- Main component for the API testing UI.
- Handles test state, running tests, assertions, AI suggestions, and result display.
- Key hooks: `useState`, `useRef` for managing tests, results, and UI state.
- Functions for running tests, evaluating assertions, importing/exporting, and generating AI suggestions.
- Renders sidebar for test management, main content for configuration, assertions, AI prompts, next calls, and results.

### App.tsx
- Root React component.
- Typically imports and renders `AgenticApiTester`:
  ```tsx
  import AgenticApiTester from './AgenticApiTester';

  function App() {
    return <AgenticApiTester />;
  }

  export default App;
  ```
- Handles global app layout and routing if needed.

## Detailed Steps
1. **Add a new test:**
   - Click "Add Test" in the sidebar.
   - Fill in method, URL, headers, and body.
2. **Configure assertions:**
   - Go to the "Assertions" tab.
   - Add, edit, or remove assertions for response validation.
   - Use AI suggestions for smart assertions.
3. **Run tests:**
   - Click "Run Test" for individual tests or "Run All" for all tests.
   - View results in the "Results" tab.
4. **Import/Export:**
   - Export tests as JSON or Word documents.
   - Import tests from a JSON file.
5. **AI Features:**
   - Use the AI Test Generator for automated test suggestions.
   - View next recommended API calls and detailed prompts.

## Troubleshooting
- Ensure all TypeScript types are correct and state variables are initialized with proper types (e.g., `any[]`).
- If you see module or JSX errors, check your `tsconfig.json` and `package.json` settings.
- For import errors, always specify the file extension (e.g., `import App from './App.js'`).

## License
MIT
