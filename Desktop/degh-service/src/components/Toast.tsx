import { useEffect } from 'react';
import { CheckCircle, XCircle, AlertCircle, X } from 'lucide-react';

export type ToastType = 'success' | 'error' | 'warning';

interface ToastProps {
    message: string;
    type: ToastType;
    onClose: () => void;
    duration?: number;
}

export function Toast({ message, type, onClose, duration = 3000 }: ToastProps) {
    useEffect(() => {
        const timer = setTimeout(() => {
            onClose();
        }, duration);

        return () => clearTimeout(timer);
    }, [duration, onClose]);

    const config = {
        success: {
            icon: CheckCircle,
            bgColor: 'bg-emerald-50',
            borderColor: 'border-emerald-500',
            iconColor: 'text-emerald-600',
            textColor: 'text-emerald-800',
        },
        error: {
            icon: XCircle,
            bgColor: 'bg-red-50',
            borderColor: 'border-red-500',
            iconColor: 'text-red-600',
            textColor: 'text-red-800',
        },
        warning: {
            icon: AlertCircle,
            bgColor: 'bg-amber-50',
            borderColor: 'border-amber-500',
            iconColor: 'text-amber-600',
            textColor: 'text-amber-800',
        },
    };

    const { icon: Icon, bgColor, borderColor, iconColor, textColor } = config[type];

    return (
        <div className="fixed top-4 right-4 z-[100] animate-slideIn">
            <div
                className={`${bgColor} ${borderColor} border-l-4 rounded-lg shadow-lg p-4 pr-12 min-w-[320px] max-w-md`}
            >
                <div className="flex items-start gap-3">
                    <Icon className={`${iconColor} flex-shrink-0 mt-0.5`} size={20} />
                    <p className={`${textColor} font-medium text-sm flex-1`}>{message}</p>
                    <button
                        onClick={onClose}
                        className={`${textColor} hover:opacity-70 transition-opacity absolute top-4 right-4`}
                        aria-label="Close notification"
                    >
                        <X size={16} />
                    </button>
                </div>
            </div>
        </div>
    );
}
