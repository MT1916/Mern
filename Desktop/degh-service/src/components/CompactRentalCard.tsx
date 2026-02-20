import { useNavigate } from 'react-router-dom';
import { Calendar, ChevronRight, Clock, CheckCircle, AlertCircle } from 'lucide-react';
import type { BookingWithDetails } from './Dashboard';
import { useMemo } from 'react';

interface CompactRentalCardProps {
    booking: BookingWithDetails;
}

const statusConfig = {
    active: {
        label: 'Active',
        icon: Clock,
        color: 'text-blue-700',
        bg: 'bg-blue-100',
        border: 'border-blue-300',
    },
    returned: {
        label: 'Returned',
        icon: CheckCircle,
        color: 'text-emerald-700',
        bg: 'bg-emerald-100',
        border: 'border-emerald-300',
    },
    overdue: {
        label: 'Overdue',
        icon: AlertCircle,
        color: 'text-red-700',
        bg: 'bg-red-100',
        border: 'border-red-300',
    },
};

export function CompactRentalCard({ booking }: CompactRentalCardProps) {
    const navigate = useNavigate();
    const statusInfo = statusConfig[booking.status];
    const StatusIcon = statusInfo.icon;

    // Calculate total amount
    const totalAmount = useMemo(() => {
        return booking.items.reduce((sum, item) => sum + (item.quantity * item.price_at_booking), 0);
    }, [booking.items]);

    // Format date helper
    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
        });
    };

    const handleClick = () => {
        navigate(`/rental/${booking.id}/edit`);
    };

    return (
        <button
            onClick={handleClick}
            className="w-full bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-200 overflow-hidden text-left focus:outline-none focus:ring-2 focus:ring-emerald-500"
        >
            <div className={`${statusInfo.bg} ${statusInfo.border} border-b-2 p-4`}>
                <div className="flex items-center justify-between gap-3">
                    {/* Status Badge */}
                    <div className="flex items-center gap-2 flex-shrink-0">
                        <StatusIcon className={statusInfo.color} size={18} />
                        <span className={`font-bold text-xs uppercase tracking-wide ${statusInfo.color}`}>
                            {statusInfo.label}
                        </span>
                    </div>

                    {/* Customer Name */}
                    <div className="flex-1 min-w-0">
                        <span className="font-semibold text-slate-800 truncate block">
                            {booking.customer.name}
                        </span>
                    </div>

                    {/* Date - Hidden on mobile */}
                    <div className="hidden sm:flex items-center gap-1.5 flex-shrink-0 text-slate-600">
                        <Calendar size={14} />
                        <span className="text-sm">{formatDate(booking.rental_date)}</span>
                    </div>

                    {/* Total Amount */}
                    <div className="text-emerald-700 font-bold text-lg flex-shrink-0">
                        ₹{totalAmount}
                    </div>

                    {/* Chevron Icon */}
                    <ChevronRight className="text-slate-400 flex-shrink-0" size={20} />
                </div>

                {/* Mobile: Show date on second row */}
                <div className="sm:hidden flex items-center gap-1.5 mt-2 text-sm text-slate-600">
                    <Calendar size={12} />
                    <span>{formatDate(booking.rental_date)}</span>
                </div>
            </div>
        </button>
    );
}
