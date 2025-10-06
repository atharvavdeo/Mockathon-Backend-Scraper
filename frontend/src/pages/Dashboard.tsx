import React, { useState } from 'react'
import { Link as LinkIcon, Loader2 } from 'lucide-react'
import { analyzeText, analyzeURL, analyzeImage, CompleteAnalysisResponse } from '../services/api'

const Dashboard: React.FC = () => {
  const [inputTab, setInputTab] = useState<'text'|'url'|'image'>('text')
  
  // Form inputs
  const [textTitle, setTextTitle] = useState('')
  const [textBody, setTextBody] = useState('')
  const [urlInput, setUrlInput] = useState('')
  const [imageFile, setImageFile] = useState<File | null>(null)
  
  // Analysis state
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<CompleteAnalysisResponse | null>(null)

  const handleAnalyze = async () => {
    setError(null)
    setResult(null)
    setLoading(true)

    try {
      let response: CompleteAnalysisResponse

      if (inputTab === 'text') {
        // Validate text input
        if (!textBody || textBody.trim().length < 100) {
          setError('Please enter at least 100 characters of text')
          setLoading(false)
          return
        }
        response = await analyzeText(textBody)
      } else if (inputTab === 'url') {
        // Validate URL input
        if (!urlInput || !urlInput.trim()) {
          setError('Please enter a valid URL')
          setLoading(false)
          return
        }
        response = await analyzeURL(urlInput)
      } else {
        // Validate image input
        if (!imageFile) {
          setError('Please upload an image file')
          setLoading(false)
          return
        }
        response = await analyzeImage(imageFile)
      }

      setResult(response)
    } catch (err: any) {
      setError(err.message || 'Failed to analyze. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setImageFile(file)
    }
  }

  const getVerdictColor = (verdict: string) => {
    switch (verdict) {
      case 'FAKE':
        return 'from-red-500/20 to-red-600/10 border-red-500/40'
      case 'REAL':
        return 'from-green-500/20 to-green-600/10 border-green-500/40'
      case 'UNCERTAIN':
        return 'from-yellow-500/20 to-yellow-600/10 border-yellow-500/40'
      default:
        return 'from-gray-500/20 to-gray-600/10 border-gray-500/40'
    }
  }

  const getVerdictTextColor = (verdict: string) => {
    switch (verdict) {
      case 'FAKE':
        return 'text-red-400'
      case 'REAL':
        return 'text-green-400'
      case 'UNCERTAIN':
        return 'text-yellow-400'
      default:
        return 'text-gray-400'
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">Fake News Detection</h1>
          <p className="text-gray-400">Analyze articles, URLs, and images for misinformation</p>
        </div>
      </div>

      {/* Input Section */}
      <div className="bg-gradient-to-br from-white/10 to-white/5 backdrop-blur rounded-2xl p-6 border border-white/10">
        <h3 className="text-xl font-bold text-white mb-4">Analyze News Article</h3>
        <div className="space-y-5">
          <div className="grid grid-cols-3 gap-3">
            {[
              { id:'text', label:'Text Input', desc:'Paste article text' },
              { id:'url', label:'URL Input', desc:'Enter article link' },
              { id:'image', label:'Image Upload', desc:'Upload screenshot' }
            ].map((t:any)=> (
              <button key={t.id} onClick={()=>setInputTab(t.id)} className={`p-4 rounded-xl border-2 transition-all ${inputTab===t.id? 'bg-blue-500/20 border-blue-500 text-white':'bg-white/5 border-white/10 text-gray-400 hover:border-white/30'}`}>
                <div className="font-semibold">{t.label}</div>
                <div className="text-xs">{t.desc}</div>
              </button>
            ))}
          </div>
          {inputTab==='text' && (
            <div className="space-y-4">
              <div>
                <label className="text-white font-medium mb-2 block">Article Title</label>
                <input 
                  value={textTitle}
                  onChange={(e) => setTextTitle(e.target.value)}
                  className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none" 
                  placeholder="Enter the headline..." 
                />
              </div>
              <div>
                <label className="text-white font-medium mb-2 block">Article Body <span className="text-gray-400 text-xs">(target 200–300 words)</span></label>
                <textarea 
                  rows={6} 
                  value={textBody}
                  onChange={(e) => setTextBody(e.target.value)}
                  className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none resize-none" 
                  placeholder="Paste the full article content here..." 
                />
              </div>
            </div>
          )}
          {inputTab==='url' && (
            <div className="space-y-4">
              <div>
                <label className="text-white font-medium mb-2 block">Article URL</label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                    <LinkIcon className="w-4 h-4" />
                  </span>
                  <input
                    value={urlInput}
                    onChange={(e) => setUrlInput(e.target.value)}
                    className="w-full bg-white/5 border border-white/10 rounded-lg pl-10 pr-4 py-3 text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none"
                    placeholder="Enter URL for the news here"
                  />
                </div>
                <div className="text-gray-400 text-xs mt-2">Fetch timeout guideline: 10–20 seconds</div>
              </div>
            </div>
          )}
          {inputTab==='image' && (
            <div className="space-y-4">
              <div>
                <label className="text-white font-medium mb-2 block">Upload Screenshot/Image</label>
                <label className="border-2 border-dashed border-white/20 rounded-xl p-6 text-center text-gray-400 block cursor-pointer hover:border-white/40">
                  <div className="mb-2">
                    {imageFile ? `Selected: ${imageFile.name}` : 'Drop image here or click to upload'}
                  </div>
                  <div className="text-xs">Supported: PNG, JPG</div>
                  <input 
                    type="file" 
                    accept="image/*" 
                    className="hidden" 
                    onChange={handleImageChange}
                  />
                </label>
              </div>
            </div>
          )}
          {error && (
            <div className="bg-red-500/20 border border-red-500/40 rounded-lg p-4 text-red-300">
              <strong>Error:</strong> {error}
            </div>
          )}
          <button 
            onClick={handleAnalyze}
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white py-3 rounded-lg font-bold text-lg transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Analyzing...
              </>
            ) : (
              'Analyze'
            )}
          </button>
        </div>
      </div>

      {/* Results Section - Shows backend response */}
      {result && (
        <div className="space-y-6">
          <div className={`bg-gradient-to-br ${getVerdictColor(result.evidence_analysis.verdict)} backdrop-blur rounded-2xl p-6 border-2`}>
            <div className="flex items-start justify-between">
              <div>
                <div className={`text-3xl font-bold ${getVerdictTextColor(result.evidence_analysis.verdict)}`}>
                  {result.evidence_analysis.verdict}
                </div>
                <div className={getVerdictTextColor(result.evidence_analysis.verdict)}>
                  {result.evidence_analysis.verdict === 'FAKE' ? 'High confidence detection' :
                   result.evidence_analysis.verdict === 'REAL' ? 'Verified as authentic' :
                   'Needs additional verification'}
                </div>
              </div>
              <div className="text-right text-white/80">
                Confidence: {result.evidence_analysis.confidence_value}%
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
              <h4 className="text-lg font-bold text-white mb-3">Key Warning Signals</h4>
              {result.evidence_analysis.warning_signals && result.evidence_analysis.warning_signals.length > 0 ? (
                <ul className="text-gray-300 list-disc ml-5 space-y-1">
                  {result.evidence_analysis.warning_signals.map((signal, idx) => (
                    <li key={idx}>{signal}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-400 text-sm">No warning signals detected</p>
              )}
            </div>

            <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
              <h4 className="text-lg font-bold text-white mb-3">Extracted Topics</h4>
              {result.evidence_analysis.extracted_topics && result.evidence_analysis.extracted_topics.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {result.evidence_analysis.extracted_topics.map((topic, idx) => (
                    <span key={idx} className="px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-sm font-medium">
                      {topic}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-gray-400 text-sm">No topics extracted</p>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
              <h4 className="text-lg font-bold text-white mb-3">Analysis Details</h4>
              <div className="space-y-2 text-gray-300 text-sm">
                <div className="flex items-center justify-between">
                  <span>Title:</span>
                  <span className="font-semibold text-white">{result.processed_input.title}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Word Count:</span>
                  <span className="font-semibold text-white">{result.processed_input.word_count}</span>
                </div>
                {result.processed_input.source_url && (
                  <div className="flex items-center justify-between">
                    <span>Source:</span>
                    <a href={result.processed_input.source_url} target="_blank" rel="noopener noreferrer" className="font-semibold text-blue-400 hover:underline truncate max-w-xs">
                      {result.processed_input.source_url}
                    </a>
                  </div>
                )}
                {result.processed_input.image_text && (
                  <div className="mt-2">
                    <span className="block mb-1">Extracted Text:</span>
                    <span className="text-gray-400 text-xs">{result.processed_input.image_text.substring(0, 100)}...</span>
                  </div>
                )}
              </div>
            </div>

            <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
              <h4 className="text-lg font-bold text-white mb-3">Explanation</h4>
              <div className="text-gray-300 text-sm whitespace-pre-line">
                {result.evidence_analysis.explanation}
              </div>
            </div>
          </div>

          {result.evidence_analysis.evidence.sources.length > 0 && (
            <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
              <h4 className="text-lg font-bold text-white mb-3">Evidence Sources</h4>
              <div className="space-y-3">
                {result.evidence_analysis.evidence.sources.map((source, index) => (
                  <div key={index} className="bg-white/5 rounded-lg p-4 border border-white/10">
                    <div className="flex items-start justify-between mb-2">
                      <a
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-400 hover:underline font-medium flex-1"
                      >
                        {source.title}
                      </a>
                      <span className={`text-xs px-2 py-1 rounded ml-2 ${
                        source.similarity === 'High' ? 'bg-green-500/20 text-green-400' :
                        source.similarity === 'Medium' ? 'bg-yellow-500/20 text-yellow-400' :
                        'bg-gray-500/20 text-gray-400'
                      }`}>
                        {source.similarity}
                      </span>
                    </div>
                    <p className="text-gray-400 text-sm">{source.snippet}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="bg-white/5 backdrop-blur rounded-xl p-6 border border-white/10">
            <h4 className="text-lg font-bold text-white mb-3">Processed Content</h4>
            <p className="text-gray-300 text-sm leading-relaxed">
              {result.processed_input.body}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard


