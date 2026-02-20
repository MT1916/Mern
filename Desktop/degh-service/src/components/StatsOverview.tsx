import { Package, Clock, CheckCircle, AlertCircle } from 'lucide-react';
import type { BookingWithDetails } from './Dashboard';

interface StatsOverviewProps {
  bookings: BookingWithDetails[];
}

export function StatsOverview({ bookings }: StatsOverviewProps) {
  const activeCount = bookings.filter(b => b.status === 'active').length;
  const returnedCount = bookings.filter(b => b.status === 'returned').length;
  const overdueCount = bookings.filter(b => b.status === 'overdue').length;

  const stats = [
    {
      label: 'Total Bookings',
      value: bookings.length,
      icon: Package,
      color: 'bg-slate-600',
      textColor: 'text-slate-600',
      bgLight: 'bg-slate-50',
    },
    {
      label: 'Active',
      value: activeCount,
      icon: Clock,
      color: 'bg-blue-600',
      textColor: 'text-blue-600',
      bgLight: 'bg-blue-50',
    },
    {
      label: 'Overdue',
      value: overdueCount,
      icon: AlertCircle,
      color: 'bg-red-600',
      textColor: 'text-red-600',
      bgLight: 'bg-red-50',
    },
    {
      label: 'Returned',
      value: returnedCount,
      icon: CheckCircle,
      color: 'bg-emerald-600',
      textColor: 'text-emerald-600',
      bgLight: 'bg-emerald-50',
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      {stats.map((stat) => {
        const Icon = stat.icon;
        return (
          <div
            key={stat.label}
            className={`${stat.bgLight} rounded-xl p-6 shadow-md border-2 border-transparent hover:border-${stat.color.replace('bg-', '')}/20 transition-all`}
          >
            <div className="flex items-center justify-between mb-2">
              <div className={`p-3 ${stat.color} rounded-lg`}>
                <Icon className="text-white" size={24} />
              </div>
              <div className={`text-4xl font-bold ${stat.textColor}`}>
                {stat.value}
              </div>
            </div>
            <div className="text-sm font-medium text-slate-600 uppercase tracking-wide">
              {stat.label}
            </div>
          </div>
        );
      })}
    </div>
  );
}
