import React from 'react'

export default function Docs(){
  return (
    <div className="docs container-card" style={{padding:20}}>
      <h1>Proof Train Oracle — Documentation</h1>

      <section>
        <h2>Project overview</h2>
        <p>An experimental oracle that bridges AI model transparency and blockchain accountability. The system evaluates datasets, trains a small model, generates proof metadata (dataset hash, model hash, accuracy) and stores or publishes that metadata to a mock on-chain registry.</p>
      </section>

      <section>
        <h2>Repository layout</h2>
        <ul>
          <li><strong>backend/</strong> — Python scripts that evaluate datasets and train models. Important files: <code>dataset_eval.py</code>, <code>model_train.py</code>, <code>output_metadata.json</code>.</li>
          <li><strong>blockchain/</strong> — Mock smart contract and interaction scripts (<code>contract.move</code>, <code>interactions.py</code>).</li>
          <li><strong>frontend/</strong> — React + Vite dashboard. Key files: <code>src/pages</code> (UI pages), <code>src/styles.css</code>.</li>
          <li><strong>docs/</strong> — Design notes and screenshots.</li>
        </ul>
      </section>

      <section>
        <h2>Quick start</h2>
        <h3>Frontend (dev)</h3>
        <ol>
          <li>Install Node.js (LTS) so <code>node</code> and <code>npm</code> are available.</li>
          <li>From the repo root: <code>cd frontend</code></li>
          <li>Install dependencies and start dev server: <code>npm install</code> then <code>npm run dev</code></li>
        </ol>

        <h3>Backend (python)</h3>
        <p>The backend uses simple Python scripts. To prepare a virtual environment and install dependencies:</p>
        <pre><code>{`python -m venv .venv; .\.venv\\Scripts\\activate; pip install -r requirements.txt`}</code></pre>
        <p>Run evaluation or training directly:</p>
        <pre><code>{`python backend/dataset_eval.py
python backend/model_train.py
python blockchain/interactions.py`}</code></pre>
      </section>

      <section>
        <h2>Frontend — API & integration</h2>
        <p>The frontend expects a couple of optional endpoints if you wire a backend:</p>
        <ul>
          <li><code>GET /backend/output_metadata.json</code> — static metadata file used by the UI to show the most recent trained dataset and accuracy (the app will try this path first).</li>
          <li><code>POST /api/upload</code> — accepts a multipart/form-data field named <code>dataset</code>. If present, the frontend will POST uploaded files here.</li>
          <li><code>POST /api/train</code> — accepts JSON body with <code>{`{ dataset_hash }`}</code> to trigger training on the server side.</li>
        </ul>
        <p>If these endpoints are not available the frontend falls back to a local simulation (computes SHA-256 in-browser and stores metadata in <code>localStorage</code>).</p>
      </section>

      <section>
        <h2>Files of interest</h2>
        <ul>
          <li><code>backend/output_metadata.json</code> — last training run metadata (dataset/model hash and accuracy).</li>
          <li><code>backend/dataset_evaluation.json</code> — example dataset evaluation metrics.</li>
          <li><code>frontend/src/pages/Home.jsx</code> — dashboard hero and upload/train UI.</li>
          <li><code>frontend/src/logo.svg</code> — simple logo used in the header.</li>
        </ul>
      </section>

      <section>
        <h2>How to make uploads real</h2>
        <p>To make uploads and training fully functional wire a small HTTP API in the backend (FastAPI or Flask):</p>
        <pre><code>{`POST /api/upload -> save uploaded file to backend/sample_datasets/, run dataset evaluation, return metadata JSON
POST /api/train -> accept dataset_hash, run model training, return updated output metadata`}</code></pre>
        <p>The repo's Python scripts already produce the expected metadata shape (see <code>backend/output_metadata.json</code>).</p>
      </section>

      <section>
        <h2>Contributing & notes</h2>
        <ul>
          <li>Tests: none included — start by adding unit tests for dataset evaluation and model training scripts.</li>
          <li>Security: the blockchain layer is a mock; do not treat it as production-grade smart contract code.</li>
          <li>Design: drop your preferred background image into <code>frontend/public/assets/hero-bg.jpg</code> to change the home hero background.</li>
        </ul>
      </section>

      <footer style={{marginTop:20}}>
        <small>Generated docs — summary of repository layout, quick-start and integration notes.</small>
      </footer>
    </div>
  )
}
