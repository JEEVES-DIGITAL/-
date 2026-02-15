import { useState } from 'react'
import useSWR from 'swr'
import { 
  Zap, 
  Play, 
  Pause, 
  Trash2, 
  Edit2, 
  Plus,
  Clock,
  Home
} from 'lucide-react'
import { automationsApi } from '../services/api'
import toast from 'react-hot-toast'

interface Automation {
  id: string
  alias: string
  description?: string
  is_enabled: boolean
  last_triggered?: string
  trigger_count: number
  trigger: {
    platform: string
    [key: string]: unknown
  }
  action: {
    service: string
    [key: string]: unknown
  }
}

export default function Automations() {
  const { data, mutate } = useSWR('automations', () => automationsApi.list().then(r => r.data))
  const [showModal, setShowModal] = useState(false)
  
  const automations: Automation[] = data || []

  const handleToggle = async (automation: Automation) => {
    try {
      await automationsApi.update(automation.id, {
        is_enabled: !automation.is_enabled
      })
      toast.success(`${automation.alias} 已${automation.is_enabled ? '禁用' : '启用'}`)
      mutate()
    } catch {
      toast.error('操作失败')
    }
  }

  const handleTrigger = async (automation: Automation) => {
    try {
      await automationsApi.trigger(automation.id)
      toast.success(`${automation.alias} 已手动触发`)
      mutate()
    } catch {
      toast.error('触发失败')
    }
  }

  const handleDelete = async (automation: Automation) => {
    if (!confirm(`确定要删除 "${automation.alias}" 吗？`)) return
    
    try {
      await automationsApi.delete(automation.id)
      toast.success('已删除')
      mutate()
    } catch {
      toast.error('删除失败')
    }
  }

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">自动化</h1>
          <p className="text-gray-500">设置智能场景和自动化规则</p>
        </div>
        <button 
          onClick={() => setShowModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-jeeves-700 text-white rounded-lg hover:bg-jeeves-800 transition-colors"
        >
          <Plus size={20} />
          新建自动化
        </button>
      </div>

      {/* 自动化列表 */}
      <div className="grid gap-4">
        {automations.map(automation => (
          <AutomationCard
            key={automation.id}
            automation={automation}
            onToggle={() => handleToggle(automation)}
            onTrigger={() => handleTrigger(automation)}
            onDelete={() => handleDelete(automation)}
          />
        ))}
      </div>

      {automations.length === 0 && (
        <div className="text-center py-12 text-gray-400">
          <Zap size={48} className="mx-auto mb-4" />
          <p>暂无自动化规则</p>
          <p className="text-sm mt-2">点击上方按钮创建您的第一个自动化</p>
        </div>
      )}

      {/* 创建模态框 (简化版) */}
      {showModal && (
        <CreateModal onClose={() => setShowModal(false)} onSuccess={() => {
          setShowModal(false)
          mutate()
        }} />
      )}
    </div>
  )
}

function AutomationCard({ 
  automation, 
  onToggle, 
  onTrigger, 
  onDelete 
}: { 
  automation: Automation
  onToggle: () => void
  onTrigger: () => void
  onDelete: () => void
}) {
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="flex items-start justify-between">
        <div className="flex items-start gap-4">
          <div className={`p-3 rounded-lg ${
            automation.is_enabled ? 'bg-accent-100' : 'bg-gray-100'
          }`}>
            <Zap size={24} className={automation.is_enabled ? 'text-accent-600' : 'text-gray-400'} />
          </div>
          
          <div>
            <h3 className="font-semibold text-gray-800">{automation.alias}</h3>
            {automation.description && (
              <p className="text-sm text-gray-500 mt-1">{automation.description}</p>
            )}
            
            <div className="flex items-center gap-4 mt-2 text-sm text-gray-400">
              <span className="flex items-center gap-1">
                <Clock size={14} />
                {automation.last_triggered 
                  ? `上次触发: ${new Date(automation.last_triggered).toLocaleString()}`
                  : '从未触发'
                }
              </span>
              <span>触发次数: {automation.trigger_count}</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={onTrigger}
            className="p-2 text-gray-400 hover:text-jeeves-600 hover:bg-jeeves-50 rounded-lg transition-colors"
            title="手动触发"
          >
            <Play size={18} />
          </button>
          
          <button
            onClick={onToggle}
            className={`p-2 rounded-lg transition-colors ${
              automation.is_enabled 
                ? 'text-green-500 hover:bg-green-50' 
                : 'text-gray-400 hover:bg-gray-100'
            }`}
            title={automation.is_enabled ? '禁用' : '启用'}
          >
            {automation.is_enabled ? <Pause size={18} /> : <Play size={18} />}
          </button>
          
          <button className="p-2 text-gray-400 hover:text-jeeves-600 hover:bg-jeeves-50 rounded-lg transition-colors">
            <Edit2 size={18} />
          </button>
          
          <button 
            onClick={onDelete}
            className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
          >
            <Trash2 size={18} />
          </button>
        </div>
      </div>
    </div>
  )
}

function CreateModal({ onClose, onSuccess }: { onClose: () => void; onSuccess: () => void }) {
  const [formData, setFormData] = useState({
    alias: '',
    description: '',
    trigger: { platform: 'time', at: '08:00' },
    action: { service: 'light.turn_on', entity_id: '' },
  })
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    
    try {
      await automationsApi.create(formData)
      toast.success('自动化创建成功')
      onSuccess()
    } catch {
      toast.error('创建失败')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 w-full max-w-lg">
        <h2 className="text-xl font-bold text-gray-800 mb-4">新建自动化</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">名称</label>
            <input
              type="text"
              value={formData.alias}
              onChange={e => setFormData({...formData, alias: e.target.value})}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-jeeves-500"
              placeholder="例如：早上开灯"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">描述</label>
            <input
              type="text"
              value={formData.description}
              onChange={e => setFormData({...formData, description: e.target.value})}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-jeeves-500"
              placeholder="可选"
            />
          </div>
          
          <div className="flex justify-end gap-2 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              取消
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="px-4 py-2 bg-jeeves-700 text-white rounded-lg hover:bg-jeeves-800 disabled:opacity-50 transition-colors"
            >
              {isLoading ? '创建中...' : '创建'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
