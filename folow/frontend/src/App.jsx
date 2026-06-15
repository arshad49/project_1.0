import { useState, useEffect } from 'react'

const API_URL = 'http://localhost:8000'

const TEMPLATES = [
  { value: 'follow_up_basic', label: 'Follow Up' },
  { value: 'festival_offer', label: 'Festival Offer' },
  { value: 'discount_offer', label: 'Discount Offer' }
]

function App() {
  const [customers, setCustomers] = useState([])
  const [loading, setLoading] = useState(false)
  const getDefaultLastVisit = () => {
    return new Date().toISOString().split('T')[0]
  }

  const getDefaultFollowup = () => {
    const date = new Date()
    date.setMonth(date.getMonth() + 2)
    return date.toISOString().split('T')[0]
  }

  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    last_visit: getDefaultLastVisit(),
    next_followup: getDefaultFollowup(),
    template_name: 'follow_up_basic'
  })

  // Fetch customers on mount
  useEffect(() => {
    fetchCustomers()
  }, [])

  const fetchCustomers = async () => {
    try {
      const res = await fetch(`${API_URL}/customers`)
      const data = await res.json()
      setCustomers(data)
    } catch (error) {
      console.error('Error fetching customers:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const res = await fetch(`${API_URL}/customer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (!res.ok) {
        const error = await res.json()
        alert(error.detail || 'Failed to add customer')
        return
      }

      // Clear form and refresh
      setFormData({
        name: '',
        phone: '',
        last_visit: getDefaultLastVisit(),
        next_followup: getDefaultFollowup(),
        template_name: 'follow_up_basic'
      })
      await fetchCustomers()
      alert('Customer added successfully!')
    } catch (error) {
      console.error('Error adding customer:', error)
      alert('Error adding customer')
    } finally {
      setLoading(false)
    }
  }

  const updateStatus = async (id, status) => {
    try {
      await fetch(`${API_URL}/customer/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
      })
      await fetchCustomers()
    } catch (error) {
      console.error('Error updating customer:', error)
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      processing: 'bg-blue-100 text-blue-800',
      sent: 'bg-gray-100 text-gray-800',
      failed: 'bg-red-100 text-red-800',
      returned: 'bg-green-100 text-green-800'
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  const isToday = (date) => {
    if (!date) return false
    const today = new Date().toISOString().split('T')[0]
    return date === today
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Header */}
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Customer Follow-up System
        </h1>

        {/* Add Customer Form */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Add Customer</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Name *</label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Phone *</label>
                <input
                  type="text"
                  required
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="10 digit phone number"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Last Visit Date</label>
                <input
                  type="date"
                  value={formData.last_visit}
                  onChange={(e) => setFormData({...formData, last_visit: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Next Follow-up Date</label>
                <input
                  type="date"
                  value={formData.next_followup}
                  onChange={(e) => setFormData({...formData, next_followup: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Template *</label>
                <select
                  required
                  value={formData.template_name}
                  onChange={(e) => setFormData({...formData, template_name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {TEMPLATES.map(template => (
                    <option key={template.value} value={template.value}>
                      {template.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 transition"
            >
              {loading ? 'Saving...' : 'Save Customer'}
            </button>
          </form>
        </div>

        {/* Customer Table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <h2 className="text-xl font-semibold p-6 pb-0">Customer List</h2>
          
          <div className="overflow-x-auto">
            <table className="w-full mt-4">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Phone</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Next Follow-up</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {customers.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="px-6 py-8 text-center text-gray-500">
                      No customers yet. Add your first customer above.
                    </td>
                  </tr>
                ) : (
                  customers.map(customer => (
                    <tr 
                      key={customer.id} 
                      className={isToday(customer.next_followup) ? 'bg-red-50' : ''}
                    >
                      <td className="px-6 py-4 whitespace-nowrap">{customer.name}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{customer.phone}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {customer.next_followup || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(customer.status)}`}>
                          {customer.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap space-x-2">
                        {customer.status !== 'returned' && (
                          <button
                            onClick={() => updateStatus(customer.id, 'returned')}
                            className="bg-green-500 text-white px-3 py-1 rounded text-sm hover:bg-green-600 transition"
                          >
                            Mark Returned
                          </button>
                        )}
                        {customer.status === 'failed' && (
                          <button
                            onClick={() => updateStatus(customer.id, 'pending')}
                            className="bg-orange-500 text-white px-3 py-1 rounded text-sm hover:bg-orange-600 transition"
                          >
                            Retry
                          </button>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
