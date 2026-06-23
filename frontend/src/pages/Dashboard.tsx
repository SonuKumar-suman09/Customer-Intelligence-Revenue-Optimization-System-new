import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Users, DollarSign, Activity, AlertTriangle } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { getDashboardSummary } from '../services/api';

const data = [
  { name: 'Jan', revenue: 4000, churn: 24 },
  { name: 'Feb', revenue: 3000, churn: 13 },
  { name: 'Mar', revenue: 2000, churn: 98 },
  { name: 'Apr', revenue: 2780, churn: 39 },
  { name: 'May', revenue: 1890, churn: 48 },
  { name: 'Jun', revenue: 2390, churn: 38 },
  { name: 'Jul', revenue: 3490, churn: 43 },
];

const StatCard = ({ title, value, icon: Icon, trend, delay }: any) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay }}
    className="glass-card p-6"
  >
    <div className="flex justify-between items-start">
      <div>
        <p className="text-white/60 text-sm font-medium mb-1">{title}</p>
        <h3 className="text-3xl font-bold text-white">{value}</h3>
      </div>
      <div className="p-3 rounded-lg bg-white/5 border border-white/10">
        <Icon size={24} className="text-primary" />
      </div>
    </div>
    <div className="mt-4 flex items-center gap-2">
      <span className={`text-sm ${trend > 0 ? 'text-secondary' : 'text-red-400'}`}>
        {trend > 0 ? '+' : ''}{trend}%
      </span>
      <span className="text-white/40 text-sm">vs last month</span>
    </div>
  </motion.div>
);

const Dashboard = () => {
  const [summary, setSummary] = useState({
    total_customers: 0,
    total_revenue: 0,
    active_users: 0,
    churn_rate: 0,
    avg_ltv: 0
  });

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const data = await getDashboardSummary();
        setSummary(data);
      } catch (error) {
        console.error("Failed to fetch summary", error);
      }
    };
    fetchSummary();
  }, []);
  return (
    <div className="p-8">
      <header className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Dashboard Overview</h1>
          <p className="text-white/60">Welcome back, here's what's happening with your customers today.</p>
        </div>
        <button className="glass-button bg-primary/20 text-primary hover:bg-primary/30 border-primary/20">
          Generate Report
        </button>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Total Revenue" value={`$${summary.total_revenue.toLocaleString()}`} icon={DollarSign} trend={12.5} delay={0.1} />
        <StatCard title="Active Customers" value={summary.active_users.toLocaleString()} icon={Users} trend={5.2} delay={0.2} />
        <StatCard title="Churn Rate" value={`${(summary.churn_rate * 100).toFixed(1)}%`} icon={AlertTriangle} trend={-1.2} delay={0.3} />
        <StatCard title="Avg. LTV" value={`$${summary.avg_ltv.toLocaleString()}`} icon={Activity} trend={8.4} delay={0.4} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5 }}
          className="glass-card p-6 lg:col-span-2"
        >
          <h3 className="text-xl font-bold text-white mb-6">Revenue Forecast</h3>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data}>
                <defs>
                  <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="name" stroke="rgba(255,255,255,0.5)" />
                <YAxis stroke="rgba(255,255,255,0.5)" />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'rgba(30,41,59,0.9)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '8px' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Area type="monotone" dataKey="revenue" stroke="#3B82F6" fillOpacity={1} fill="url(#colorRevenue)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.6 }}
          className="glass-card p-6"
        >
          <h3 className="text-xl font-bold text-white mb-6">Churn Risk Segmentation</h3>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="name" stroke="rgba(255,255,255,0.5)" />
                <YAxis stroke="rgba(255,255,255,0.5)" />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'rgba(30,41,59,0.9)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '8px' }}
                />
                <Line type="monotone" dataKey="churn" stroke="#10B981" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;
