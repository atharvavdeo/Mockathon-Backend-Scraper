import React, { useEffect, useState } from 'react'
import { ArrowRight, FileText, Link as LinkIcon, Image as ImageIcon, Activity, Globe, Zap, Target, Clock, User as UserIcon } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import ShinyText from '../components/ShinyText'
import CountUp from '../components/CountUp'

const Landing: React.FC = () => {
  const navigate = useNavigate()
  const [animatedStats, setAnimatedStats] = useState<number[]>([0, 0, 0, 0])

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedStats([10000, 95, 5, 50000])
    }, 100)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="space-y-4">
      <div className="text-center py-6">
        <div className="inline-flex items-center gap-2 bg-blue-500/20 text-blue-300 px-4 py-2 rounded-full text-sm mb-6 animate-pulse">
          <Zap className="w-4 h-4" />
          AI-Powered Truth Verification
        </div>
        <h1 className="text-6xl font-bold text-white mb-6">
          Stop Fake News<br />
          <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Before It Spreads
          </span>
        </h1>
        <ShinyText 
          text="Our multi-agent AI system analyzes news articles in seconds, providing detailed explanations and verified evidence to help you make informed decisions."
          speed={2}
          className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto font-darker-grotesque"
        />
        <div className="flex gap-4 justify-center">
          <button 
            onClick={() => navigate('/dashboard')}
            className="bg-blue-500 hover:bg-blue-600 text-white px-8 py-4 rounded-lg font-semibold text-lg flex items-center gap-2 transition-all shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            Get Started Free
            <ArrowRight className="w-5 h-5" />
          </button>
          <button 
            onClick={() => navigate('/dashboard')}
            className="bg-white/10 hover:bg-white/20 text-white px-8 py-4 rounded-lg font-semibold text-lg backdrop-blur transition-all"
          >
            View Dashboard
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {[
          { number: animatedStats[0], suffix: '+', label: 'Articles Analyzed', icon: FileText },
          { number: animatedStats[1], suffix: '%', label: 'Accuracy Rate', icon: Target },
          { number: animatedStats[2], prefix: '<', suffix: 's', label: 'Analysis Time', icon: Clock },
          { number: Number((animatedStats[3]/1000).toFixed(0)), suffix: 'K+', label: 'Active Users', icon: UserIcon }
        ].map((stat, i) => {
          const Icon = stat.icon as React.FC<any>
          return (
            <div key={i} className="bg-white/5 backdrop-blur rounded-xl p-6 text-center border border-white/10 hover:border-blue-500/50 transition-all transform hover:scale-105">
              <Icon className="w-8 h-8 text-blue-400 mx-auto mb-3" />
              <div className="text-3xl font-bold text-blue-400 mb-2 transition-all duration-1000">
                {stat.prefix}
                <CountUp to={stat.number} duration={1.2} />
                {stat.suffix}
              </div>
              <div className="text-gray-400">{stat.label}</div>
            </div>
          )
        })}
      </div>

      <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-bold text-white flex items-center gap-2">
            <Activity className="w-6 h-6 text-green-400 animate-pulse" />
            Live Detection Activity
          </h3>
          <span className="text-xs text-green-400 bg-green-400/20 px-2 py-1 rounded-full">LIVE</span>
        </div>
        <div className="space-y-2">
          {[
            { location: 'New York, USA', verdict: 'Fake', time: 'Just now' },
            { location: 'London, UK', verdict: 'Real', time: '2 sec ago' },
            { location: 'Tokyo, Japan', verdict: 'Fake', time: '5 sec ago' },
            { location: 'Mumbai, India', verdict: 'Real', time: '8 sec ago' }
          ].map((item, i) => (
            <div key={i} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
              <div className="flex items-center gap-3">
                <Globe className="w-4 h-4 text-gray-400" />
                <span className="text-white">{item.location}</span>
              </div>
              <div className="flex items-center gap-3">
                <span className={`px-2 py-1 rounded text-xs font-bold ${
                  item.verdict === 'Real' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                }`}>
                  {item.verdict}
                </span>
                <span className="text-gray-500 text-xs">{item.time}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pb-12">
        {[
          { icon: FileText, title: 'Text Analysis', desc: 'Paste any article text for instant verification', color: 'blue' },
          { icon: LinkIcon, title: 'URL Scanning', desc: 'Analyze articles directly from any website', color: 'purple' },
          { icon: ImageIcon, title: 'Image OCR', desc: 'Extract and verify text from screenshots', color: 'green' }
        ].map((feature, i) => {
          const Icon = feature.icon as React.FC<any>
          return (
            <div key={i} className="bg-gradient-to-br from-white/10 to-white/5 backdrop-blur rounded-xl p-6 border border-white/10 hover:border-blue-500/50 transition-all transform hover:scale-105">
              <div className={`w-16 h-16 rounded-xl bg-gradient-to-br from-${feature.color}-500/20 to-${feature.color}-600/10 flex items-center justify-center mb-4`}>
                <Icon className={`w-8 h-8 text-${feature.color}-400`} />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">{feature.title}</h3>
              <p className="text-gray-400 mb-4">{feature.desc}</p>
              <button 
                onClick={() => navigate('/dashboard')}
                className="text-blue-400 hover:text-blue-300 text-sm font-semibold flex items-center gap-1"
              >
                Try Now <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          )
        })}
      </div>
      </div>
  )
}

export default Landing


