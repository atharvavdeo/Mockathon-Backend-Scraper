import React from 'react'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Results from './pages/Results'
import Landing from './pages/Landing'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <div className="relative min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
        <Navbar />
        <div className="max-w-7xl mx-auto px-6 py-8 relative z-10 space-y-10">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/results" element={<Results />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  )
}

export default App


