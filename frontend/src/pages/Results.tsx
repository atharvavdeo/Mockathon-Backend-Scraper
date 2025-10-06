import React, { useMemo, useState } from 'react'
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, LineChart, Line, Legend } from 'recharts'
import { AlertTriangle } from 'lucide-react'

type Point = { date: string; real: number; fake: number }

function generateSeries(days: number): Point[] {
  const labels7 = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
  const labels30 = Array.from({length: 30}, (_,i)=>`D${i+1}`)
  const labels90 = Array.from({length: 90}, (_,i)=>`D${i+1}`)
  const labels = days===7?labels7:days===30?labels30:labels90
  const out: Point[] = []
  let realBase = 40
  let fakeBase = 28
  for (let i=0;i<labels.length;i++) {
    const r = realBase + Math.round(Math.sin(i/3)*8 + Math.cos(i/5)*4)
    const f = fakeBase + Math.round(Math.cos(i/4)*10 + Math.sin(i/6)*5)
    const real = Math.max(10, r)
    const fake = Math.max(8, f)
    out.push({ date: labels[i], real, fake })
  }
  return out
}

const Results: React.FC = () => {
  const [range, setRange] = useState<'7d'|'30d'|'90d'>('7d')
  const [metricView, setMetricView] = useState<'volume'|'ratio'>('volume')

  const rawData = useMemo(()=>generateSeries(range==='7d'?7:range==='30d'?30:90),[range])
  const chartData = useMemo(()=>{
    if (metricView==='volume') return rawData
    return rawData.map(p=>{
      const total = p.real + p.fake
      const real = Math.round((p.real/total)*100)
      const fake = 100 - real
      return { date: p.date, real, fake }
    })
  },[rawData, metricView])

  const yDomain: [number, number] | undefined = metricView==='volume'?undefined:[0,100]

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (!active || !payload) return null
    const items = [...payload].filter(Boolean).sort((a,b)=> (b.value as number) - (a.value as number))
    const unit = metricView==='ratio' ? '%' : ''
    return (
      <div className="bg-slate-800/95 border border-white/10 rounded-md px-3 py-2 text-sm">
        <div className="text-gray-300 mb-1">{label}</div>
        {items.map((it:any, idx:number)=> (
          <div key={idx} className="flex items-center gap-2">
            <span className="inline-block w-2 h-2 rounded-full" style={{ background: it.color }} />
            <span className="text-gray-400">{it.dataKey}</span>
            <span className="text-white font-semibold">{it.value}{unit}</span>
          </div>
        ))}
        {items.length>=2 && metricView==='ratio' && (
          <div className="mt-1 text-xs text-gray-500">Total: {(items[0].value as number)+(items[1].value as number)}%</div>
        )}
      </div>
    )
  }

  const last = chartData[chartData.length-1]
  const realPct = metricView==='ratio' ? (last?.real ?? 0) : Math.round(((last?.real ?? 0) / (((last?.real ?? 0)+(last?.fake ?? 0))||1))*100)

  return (
    <div className="space-y-6">
      {/* Verdict header */}
      <div className="bg-gradient-to-br from-red-500/20 to-red-600/10 backdrop-blur rounded-2xl p-6 border-2 border-red-500/40">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-8 h-8 text-red-400" />
            <div>
              <div className="text-3xl font-bold text-white">LIKELY FAKE</div>
              <div className="text-red-300">High confidence detection</div>
            </div>
          </div>
          <div className="text-right text-white/80">Confidence: {realPct}%</div>
        </div>
      </div>

      {/* Controls */}
      <div className="flex items-center gap-2">
        <div className="bg-white/10 border border-white/10 rounded-lg overflow-hidden">
          {(['7d','30d','90d'] as const).map(v => (
            <button key={v} onClick={() => setRange(v)} className={`px-3 py-2 text-sm ${range===v?'bg-blue-500 text-white':'text-gray-300 hover:bg-white/10'}`}>{v}</button>
          ))}
        </div>
        <div className="bg-white/10 border border-white/10 rounded-lg overflow-hidden">
          {(['volume','ratio'] as const).map(v => (
            <button key={v} onClick={() => setMetricView(v)} className={`px-3 py-2 text-sm capitalize ${metricView===v?'bg-blue-500 text-white':'text-gray-300 hover:bg-white/10'}`}>{v}</button>
          ))}
        </div>
      </div>

      {/* Trends */}
      <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
        <h3 className="text-xl font-bold text-white mb-4">Detection Trends</h3>
        <ResponsiveContainer width="100%" height={260}>
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="colorReal" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#10b981" stopOpacity={0.1}/>
              </linearGradient>
              <linearGradient id="colorFake" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#ef4444" stopOpacity={0.1}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="date" stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" domain={yDomain} />
            <Tooltip content={<CustomTooltip />} />
            <Area type="monotone" dataKey="real" stackId="1" stroke="#10b981" fill="url(#colorReal)" />
            <Area type="monotone" dataKey="fake" stackId="1" stroke="#ef4444" fill="url(#colorFake)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Line compare */}
      <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
        <h3 className="text-xl font-bold text-white mb-4">Real vs Fake (Line)</h3>
        <ResponsiveContainer width="100%" height={240}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="date" stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" domain={yDomain} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Line type="monotone" dataKey="real" stroke="#10b981" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="fake" stroke="#ef4444" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default Results


