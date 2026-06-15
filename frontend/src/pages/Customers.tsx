import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter, Download, MoreVertical } from 'lucide-react';
import { getCustomers } from '../services/api';

const Customers = () => {
  const [customers, setCustomers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const data = await getCustomers();
        setCustomers(data);
      } catch (error) {
        console.error("Failed to fetch customers", error);
      } finally {
        setLoading(false);
      }
    };
    fetchCustomers();
  }, []);

  return (
    <div className="p-8">
      <header className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Customers</h1>
          <p className="text-white/60">Manage your customer data and view ML insights.</p>
        </div>
        <div className="flex gap-4">
          <button className="glass-button flex items-center gap-2">
            <Download size={18} /> Export CSV
          </button>
          <button className="glass-button bg-primary/20 text-primary hover:bg-primary/30 border-primary/20">
            Add Customer
          </button>
        </div>
      </header>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card"
      >
        <div className="p-6 border-b border-white/10 flex justify-between items-center">
          <div className="relative w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-white/40" size={18} />
            <input 
              type="text" 
              placeholder="Search customers..." 
              className="glass-input pl-10"
            />
          </div>
          <button className="glass-button flex items-center gap-2">
            <Filter size={18} /> Filter
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-white/10 bg-white/5">
                <th className="p-4 text-white/60 font-medium">Customer Name</th>
                <th className="p-4 text-white/60 font-medium">Email</th>
                <th className="p-4 text-white/60 font-medium">Segment</th>
                <th className="p-4 text-white/60 font-medium">Predicted CLV</th>
                <th className="p-4 text-white/60 font-medium">Churn Risk</th>
                <th className="p-4 text-white/60 font-medium">Status</th>
                <th className="p-4 text-white/60 font-medium"></th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={7} className="p-4 text-center text-white/60">Loading customers...</td>
                </tr>
              ) : (
                customers.map((c) => (
                  <tr key={c.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                  <td className="p-4 font-medium">{c.name}</td>
                  <td className="p-4 text-white/70">{c.email}</td>
                  <td className="p-4">
                    <span className="px-3 py-1 rounded-full text-xs font-medium bg-blue-500/20 text-blue-400 border border-blue-500/20">
                      {c.segment}
                    </span>
                  </td>
                  <td className="p-4 font-medium">{c.clv}</td>
                  <td className="p-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium border ${
                      c.churnRisk === 'High' ? 'bg-red-500/20 text-red-400 border-red-500/20' : 
                      c.churnRisk === 'Medium' ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/20' : 
                      'bg-green-500/20 text-green-400 border-green-500/20'
                    }`}>
                      {c.churnRisk}
                    </span>
                  </td>
                  <td className="p-4">
                    <div className="flex items-center gap-2">
                      <div className={`w-2 h-2 rounded-full ${c.status === 'Active' ? 'bg-green-500' : 'bg-red-500'}`}></div>
                      <span className="text-white/70">{c.status}</span>
                    </div>
                  </td>
                  <td className="p-4">
                    <button className="text-white/40 hover:text-white transition-colors">
                      <MoreVertical size={18} />
                    </button>
                  </td>
                </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  );
};

export default Customers;
