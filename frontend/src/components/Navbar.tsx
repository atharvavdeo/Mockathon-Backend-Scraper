import React from 'react'
import { Shield } from 'lucide-react'
import ShinyText from './ShinyText'
import { Link, useLocation } from 'react-router-dom'

type NavbarProps = {
  onMenuClick?: () => void
}

const Navbar: React.FC<NavbarProps> = ({ onMenuClick }) => {
  return (
    <div className="bg-black/30 backdrop-blur-sm border-b border-white/10 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="text-white font-bold text-4xl flex items-center gap-2">
            <Shield className="w-8 h-8 text-blue-400" />
            <Link to="/" className="inline-block"><ShinyText text="Reason Net" speed={3} /></Link>
          </div>
          <NavLinks />
          <button 
            onClick={onMenuClick}
            className="md:hidden bg-white/10 p-2 rounded-lg"
            aria-label="Open menu"
          >
            {/* placeholder for menu icon if needed */}
          </button>
        </div>
      </div>
    </div>
  )
}

export default Navbar

function NavLinks() {
  const location = useLocation()
  const tabs = [
    { to: '/', label: 'Home' },
    { to: '/dashboard', label: 'Dashboard' },
    { to: '/results', label: 'Results' }
  ]
  return (
    <div className="hidden md:flex gap-2">
      {tabs.map(t => (
        <Link key={t.to} to={t.to} className={`glass-tab ${location.pathname===t.to ? 'bg-white/20 border-white/30 text-white' : ''}`}>
          {t.label}
        </Link>
      ))}
    </div>
  )
}

