import { useState } from 'react'
import useSWR from 'swr'
import { 
  Lightbulb, 
  Thermometer, 
  Shield, 
  Tv, 
  Fan,
  Power,
  MoreVertical
} from 'lucide-react'
import { devicesApi } from '../services/api'
import toast from 'react-hot-toast'

interface Device {
  id: string
  entity_id: string
  name: string
  device_type: string
  area: string
  state: string
  is_available: boolean
  attributes: Record<string, unknown>
}

const deviceIcons: Record<string, React.ElementType> = {
  light: Lightbulb,
  climate: Thermometer,
  sensor: Shield,
  media_player: Tv,
  fan: Fan,
  default: Power,
}

export default function Devices() {
  const { data, mutate } = useSWR('devices', () => devicesApi.list().then(r => r.data))
  const [selectedType, setSelectedType] = useState<string>('all')
  
  const devices: Device[] = data?.devices || []
  
  // 按类型过滤
  const filteredDevices = selectedType === 'all' 
    ? devices 
    : devices.filter(d => d.device_type === selectedType)
  
  // 获取所有类型
  const types = ['all', ...new Set(devices.map(d => d.device_type))]
  
  const handleToggle = async (device: Device) => {
    try {
      const newState = device.state === 'on' ? 'off' : 'on'
      await devicesApi.command(device.id, {
        service: newState === 'on' ? 'turn_on' : 'turn_off',
        data: {}
      })
      toast.success(`${device.name} 已${newState === 'on' ? '开启' : '关闭'}`)
      mutate()
    } catch {
      toast.error('操作失败')
    }
  }

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">设备管理</h1>
          <p className="text-gray-500">管理您的智能家居设备</p>
        </div>
        <button className="px-4 py-2 bg-jeeves-700 text-white rounded-lg hover:bg-jeeves-800 transition-colors">
          添加设备
        </button>
      </div>

      {/* 类型筛选 */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {types.map(type => (
          <button
            key={type}
            onClick={() => setSelectedType(type)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap ${
              selectedType === type
                ? 'bg-jeeves-700 text-white'
                : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
            }`}
          >
            {type === 'all' ? '全部' : type}
          </button>
        ))}
      </div>

      {/* 设备网格 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filteredDevices.map(device => (
          <DeviceCard 
            key={device.id} 
            device={device} 
            onToggle={() => handleToggle(device)}
          />
        ))}
      </div>

      {filteredDevices.length === 0 && (
        <div className="text-center py-12 text-gray-400">
          <Power size={48} className="mx-auto mb-4" />
          <p>暂无设备</p>
        </div>
      )}
    </div>
  )
}

function DeviceCard({ device, onToggle }: { device: Device; onToggle: () => void }) {
  const Icon = deviceIcons[device.device_type] || deviceIcons.default
  const isOn = device.state === 'on'
  
  return (
    <div className={`p-4 rounded-xl border transition-all ${
      isOn 
        ? 'bg-accent-50 border-accent-200' 
        : 'bg-white border-gray-200'
    }`}>
      <div className="flex items-start justify-between mb-3">
        <div className={`p-3 rounded-lg ${
          isOn ? 'bg-accent-500' : 'bg-gray-100'
        }`}>
          <Icon size={20} className={isOn ? 'text-white' : 'text-gray-600'} />
        </div>
        <button className="text-gray-400 hover:text-gray-600">
          <MoreVertical size={16} />
        </button>
      </div>
      
      <div className="mb-3">
        <h3 className="font-semibold text-gray-800">{device.name}</h3>
        <p className="text-sm text-gray-500">{device.area || '未分区'}</p>
      </div>
      
      <div className="flex items-center justify-between">
        <span className={`text-sm ${
          device.is_available ? 'text-green-500' : 'text-red-500'
        }`}>
          {device.is_available ? '在线' : '离线'}
        </span>
        
        <button
          onClick={onToggle}
          className={`w-12 h-6 rounded-full transition-colors relative ${
            isOn ? 'bg-accent-500' : 'bg-gray-300'
          }`}
        >
          <span className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-transform ${
            isOn ? 'left-7' : 'left-1'
          }`} />
        </button>
      </div>
    </div>
  )
}
