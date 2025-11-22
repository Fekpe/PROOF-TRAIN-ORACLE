import React, { useState } from 'react'
import Home from './pages/Home'
import Datasets from './pages/Datasets'
import Models from './pages/Models'
import Docs from './pages/Docs'
import Logo from './logo.svg'

function Nav({ page, setPage }) {
  return (
    <nav className="nav">
      <div className="nav-left">
        <img src={Logo} alt="Proof Train Oracle" className="logo" />
        <div className="brand">PROOF OF TRAIN ORACLE</div>
      </div>

      <div className="links">
        <button onClick={() => setPage('home')} className={page === 'home' ? 'active' : ''}>Home</button>
        <button onClick={() => setPage('datasets')} className={page === 'datasets' ? 'active' : ''}>Dataset</button>
        <button onClick={() => setPage('models')} className={page === 'models' ? 'active' : ''}>Model</button>
        <button onClick={() => setPage('docs')} className={page === 'docs' ? 'active' : ''}>Docs</button>
      </div>

      <div className="nav-right">
        <a href="https://github.com/Fekpe" target="_blank" rel="noreferrer" aria-label="GitHub" className="social">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M12 .5C5.7.5.5 5.7.5 12c0 5.1 3.3 9.4 7.9 10.9.6.1.8-.3.8-.6v-2.1c-3.2.7-3.9-1.4-3.9-1.4-.6-1.6-1.4-2-1.4-2-1.2-.8.1-.8.1-.8 1.3.1 2 1.3 2 1.3 1.2 2 3.2 1.4 4 .1.1-.8.5-1.4.9-1.7-2.6-.3-5.3-1.3-5.3-5.8 0-1.3.5-2.4 1.3-3.2-.1-.3-.6-1.6.1-3.3 0 0 1-.3 3.3 1.2.9-.2 1.9-.3 2.9-.3s2 .1 2.9.3C18 4.1 19 4.4 19 4.4c.7 1.7.2 3 .1 3.3.8.8 1.3 1.9 1.3 3.2 0 4.5-2.7 5.5-5.3 5.8.5.4.9 1.1.9 2.2v3.2c0 .3.2.7.8.6C20.7 21.4 24 17.1 24 12 24 5.7 18.3.5 12 .5z"/></svg>
        </a>
        <a href="https://x.com/FavEkpe" target="_blank" rel="noreferrer" aria-label="X" className="social">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M22.46 6c-.77.35-1.6.59-2.46.7.89-.54 1.58-1.4 1.9-2.42-.83.5-1.75.86-2.73 1.06A4.2 4.2 0 0 0 12 8.5c0 .33.04.66.11.97C8.01 9.3 4.47 7.4 2.15 4.1c-.36.62-.57 1.34-.57 2.11 0 1.46.75 2.75 1.88 3.5-.7-.02-1.36-.22-1.94-.53v.05c0 2.03 1.44 3.72 3.35 4.10-.35.1-.72.15-1.10.15-.27 0-.53-.03-.78-.07.53 1.66 2.05 2.87 3.86 2.9A8.45 8.45 0 0 1 2 19.54 11.9 11.9 0 0 0 8.29 21.5c7.55 0 11.68-6.26 11.68-11.68v-.53c.8-.58 1.48-1.3 2.02-2.12-.73.32-1.5.54-2.31.64z"/></svg>
        </a>
      </div>
    </nav>
  )
}

export default function App() {
  const [page, setPage] = useState('home')

  return (
    <div className="app">
      <Nav page={page} setPage={setPage} />
      <main className="container">
        {page === 'home' && <Home />}
        {page === 'datasets' && <Datasets />}
        {page === 'models' && <Models />}
        {page === 'docs' && <Docs />}
      </main>
    </div>
  )
}
