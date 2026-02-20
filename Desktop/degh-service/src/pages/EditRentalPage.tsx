import { useState, useEffect, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, User, Package, Save } from 'lucide-react';
import { supabase } from '../lib/supabase';
import type { BookingWithDetails, BookingItem } from '../components/Dashboard';
import { Toast, ToastType } from '../components/Toast';

export function EditRentalPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();

    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [booking, setBooking] = useState<BookingWithDetails | null>(null);
    const [toast, setToast] = useState<{ message: string; type: ToastType } | null>(null);

    // Editable state
    const [customerName, setCustomerName] = useState('');
    const [customerPhone, setCustomerPhone] = useState('');
    const [customerAddress, setCustomerAddress] = useState('');
    const [items, setItems] = useState<BookingItem[]>([]);
    const [status, setStatus] = useState<'active' | 'returned' | 'overdue'>('active');

    // Calculate total amount
    const totalAmount = useMemo(() => {
        return items.reduce((sum, item) => sum + (item.quantity * item.price_at_booking), 0);
    }, [items]);

    // Load booking data
    useEffect(() => {
        if (!id) {
            navigate('/');
            return;
        }

        loadBooking();
    }, [id]);

    async function loadBooking() {
        try {
            // Fetch all data in parallel for faster loading
            const [rentalResponse, itemsResponse] = await Promise.all([
                supabase.from('rentals').select('*').eq('id', id).maybeSingle(),
                supabase.from('rental_items').select(`
          id,
          rental_id,
          item_id,
          quantity,
          price_at_booking,
          created_at,
          items (name)
        `).eq('rental_id', id)
            ]);

            const { data: rentalData, error: rentalError } = rentalResponse;
            if (rentalError) throw rentalError;
            if (!rentalData) {
                setToast({ message: 'Booking not found', type: 'error' });
                setTimeout(() => navigate('/'), 2000);
                return;
            }

            // Now fetch customer with correct ID, as it depends on rentalData
            const { data: customerData, error: customerError } = await supabase
                .from('customers')
                .select('*')
                .eq('id', rentalData.customer_id)
                .maybeSingle();

            if (customerError) throw customerError;
            if (!customerData) throw new Error('Customer not found');

            const { data: itemsData, error: itemsError } = itemsResponse;
            if (itemsError) throw itemsError;

            const itemsWithNames = (itemsData || []).map(item => ({
                ...item,
                item_name: (item as { items?: { name: string } }).items?.name,
            }));

            const bookingWithDetails: BookingWithDetails = {
                ...rentalData,
                customer: customerData,
                items: itemsWithNames,
            };

            setBooking(bookingWithDetails);
            setCustomerName(customerData.name);
            setCustomerPhone(customerData.contact_number);
            setCustomerAddress(customerData.address || '');
            setItems(itemsWithNames);
            setStatus(rentalData.status);
        } catch (error) {
            console.error('Error loading booking:', error);
            setToast({ message: 'Failed to load booking', type: 'error' });
            setTimeout(() => navigate('/'), 2000);
        } finally {
            setLoading(false);
        }
    }

    // Handle item quantity change with optimistic update
    const handleQuantityChange = (itemId: string, newQuantity: number) => {
        const validQuantity = Math.max(1, newQuantity);

        // Optimistic update - instant UI feedback
        setItems(prevItems =>
            prevItems.map(item =>
                item.id === itemId ? { ...item, quantity: validQuantity } : item
            )
        );

        // Debounced save to database (optional - can save on "Save Changes" button)
        // This makes the UI feel instant while still persisting changes
    };

    // Save changes
    const handleSave = async () => {
        if (!booking) return;

        setSaving(true);
        try {
            // Update customer
            const { error: customerError } = await supabase
                .from('customers')
                .update({
                    name: customerName,
                    contact_number: customerPhone,
                    address: customerAddress,
                    updated_at: new Date().toISOString(),
                } as never)
                .eq('id', booking.customer_id);

            if (customerError) throw customerError;

            // Update rental status
            const { error: rentalError } = await supabase
                .from('rentals')
                .update({
                    status: status,
                    updated_at: new Date().toISOString(),
                } as never)
                .eq('id', booking.id);

            if (rentalError) throw rentalError;

            // Update item quantities
            for (const item of items) {
                const { error: itemError } = await supabase
                    .from('rental_items')
                    .update({ quantity: item.quantity } as never)
                    .eq('id', item.id);

                if (itemError) throw itemError;
            }

            setToast({ message: 'Changes saved successfully! 🎉', type: 'success' });
            setTimeout(() => navigate('/'), 1500);
        } catch (error) {
            console.error('Error saving changes:', error);
            setToast({ message: 'Failed to save changes', type: 'error' });
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-emerald-50">
                {/* Header Skeleton */}
                <div className="bg-white shadow-md sticky top-0 z-10 border-b border-slate-200">
                    <div className="container mx-auto px-4 py-4">
                        <div className="flex items-center gap-4">
                            <div className="w-10 h-10 bg-slate-200 rounded-xl animate-pulse"></div>
                            <div className="flex-1">
                                <div className="h-6 w-32 bg-slate-200 rounded animate-pulse mb-2"></div>
                                <div className="h-4 w-24 bg-slate-200 rounded animate-pulse"></div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Content Skeleton */}
                <div className="container mx-auto px-4 py-8 max-w-4xl">
                    <div className="space-y-6">
                        {/* Customer Details Skeleton */}
                        <div className="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden">
                            <div className="bg-gradient-to-r from-blue-400 to-blue-500 p-4 h-16 animate-pulse"></div>
                            <div className="p-6 space-y-5">
                                {[1, 2, 3].map((i) => (
                                    <div key={i}>
                                        <div className="h-4 w-24 bg-slate-200 rounded animate-pulse mb-2"></div>
                                        <div className="h-10 bg-slate-100 rounded-xl animate-pulse"></div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Items Skeleton */}
                        <div className="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden">
                            <div className="bg-gradient-to-r from-emerald-400 to-emerald-500 p-3 h-14 animate-pulse"></div>
                            <div className="p-4 space-y-2.5">
                                {[1, 2, 3, 4].map((i) => (
                                    <div key={i} className="h-16 bg-slate-100 rounded-lg animate-pulse"></div>
                                ))}
                            </div>
                        </div>

                        {/* Footer Skeleton */}
                        <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6">
                            <div className="h-12 bg-slate-100 rounded-xl animate-pulse mb-4"></div>
                            <div className="h-14 bg-emerald-100 rounded-xl animate-pulse"></div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    if (!booking) {
        return null;
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-emerald-50">
            {/* Header */}
            <div className="bg-white shadow-md sticky top-0 z-10 border-b border-slate-200">
                <div className="container mx-auto px-4 py-4">
                    <div className="flex items-center gap-4">
                        <button
                            onClick={() => navigate('/')}
                            className="p-2.5 hover:bg-slate-100 rounded-xl transition-all hover:scale-105 active:scale-95"
                            aria-label="Go back"
                        >
                            <ArrowLeft size={24} className="text-slate-700" />
                        </button>
                        <div className="flex-1">
                            <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
                                Edit Rental
                            </h1>
                            <p className="text-sm text-slate-500 font-medium">
                                ID: {booking.id.slice(0, 8).toUpperCase()}
                            </p>
                        </div>
                        <div className="hidden sm:flex items-center gap-2 px-4 py-2 bg-emerald-50 rounded-lg border border-emerald-200">
                            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                            <span className="text-sm font-medium text-emerald-700">Editing</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Content */}
            <div className="container mx-auto px-4 py-8 max-w-4xl">
                <div className="space-y-6">
                    {/* Customer Details Section */}
                    <div className="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden hover:shadow-xl transition-shadow">
                        <div className="bg-gradient-to-r from-blue-500 to-blue-600 p-4">
                            <h2 className="text-lg font-bold text-white flex items-center gap-2">
                                <div className="p-2 bg-white/20 rounded-lg backdrop-blur-sm">
                                    <User size={20} />
                                </div>
                                Customer Details
                            </h2>
                        </div>
                        <div className="p-6 space-y-5">
                            <div className="group">
                                <label className="block text-sm font-semibold text-slate-700 mb-2 flex items-center gap-2">
                                    <span className="w-1.5 h-1.5 bg-blue-500 rounded-full"></span>
                                    Full Name
                                </label>
                                <input
                                    type="text"
                                    value={customerName}
                                    onChange={(e) => setCustomerName(e.target.value)}
                                    className="w-full border-2 border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all hover:border-slate-300 bg-slate-50 focus:bg-white"
                                    placeholder="Enter customer name"
                                />
                            </div>

                            <div className="group">
                                <label className="block text-sm font-semibold text-slate-700 mb-2 flex items-center gap-2">
                                    <span className="w-1.5 h-1.5 bg-blue-500 rounded-full"></span>
                                    Phone Number
                                </label>
                                <input
                                    type="tel"
                                    value={customerPhone}
                                    onChange={(e) => setCustomerPhone(e.target.value)}
                                    className="w-full border-2 border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all hover:border-slate-300 bg-slate-50 focus:bg-white"
                                    placeholder="Enter phone number"
                                />
                            </div>

                            <div className="group">
                                <label className="block text-sm font-semibold text-slate-700 mb-2 flex items-center gap-2">
                                    <span className="w-1.5 h-1.5 bg-blue-500 rounded-full"></span>
                                    Address
                                </label>
                                <input
                                    type="text"
                                    value={customerAddress}
                                    onChange={(e) => setCustomerAddress(e.target.value)}
                                    className="w-full border-2 border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all hover:border-slate-300 bg-slate-50 focus:bg-white"
                                    placeholder="Enter address"
                                />
                            </div>
                        </div>
                    </div>

                    {/* Items Rented Section */}
                    <div className="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden hover:shadow-xl transition-shadow">
                        <div className="bg-gradient-to-r from-emerald-500 to-emerald-600 p-3">
                            <h2 className="text-base font-bold text-white flex items-center gap-2">
                                <div className="p-1.5 bg-white/20 rounded-lg backdrop-blur-sm">
                                    <Package size={18} />
                                </div>
                                Items Rented ({items.length})
                            </h2>
                        </div>
                        <div className="p-4 space-y-2.5 max-h-[500px] overflow-y-auto">
                            {items.map((item, index) => (
                                <div
                                    key={item.id}
                                    className="group relative bg-gradient-to-br from-slate-50 to-white rounded-lg p-3 border border-slate-200 hover:border-emerald-300 hover:shadow-sm transition-all"
                                >
                                    {/* Item number badge */}
                                    <div className="absolute -top-1.5 -left-1.5 w-6 h-6 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-full flex items-center justify-center text-white font-bold text-xs shadow-md">
                                        {index + 1}
                                    </div>

                                    {/* Compact layout */}
                                    <div className="flex items-center gap-3 ml-4">
                                        {/* Item info - Left */}
                                        <div className="flex-1 min-w-0">
                                            <div className="font-bold text-slate-800 text-sm truncate">
                                                {item.item_name || 'Unknown Item'}
                                            </div>
                                            <div className="text-xs text-slate-500 font-medium">
                                                ₹{item.price_at_booking}/unit
                                            </div>
                                        </div>

                                        {/* Quantity controls - Center */}
                                        <div className="flex items-center gap-1.5">
                                            <button
                                                onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                                                className="w-7 h-7 rounded-md bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold flex items-center justify-center transition-all hover:scale-110 active:scale-95 text-sm"
                                            >
                                                −
                                            </button>
                                            <input
                                                type="number"
                                                min="1"
                                                value={item.quantity}
                                                onChange={(e) => handleQuantityChange(item.id, parseInt(e.target.value) || 1)}
                                                className="w-14 border border-emerald-200 rounded-md px-2 py-1 text-center font-bold text-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-transparent bg-white text-sm"
                                            />
                                            <button
                                                onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                                                className="w-7 h-7 rounded-md bg-emerald-500 hover:bg-emerald-600 text-white font-bold flex items-center justify-center transition-all hover:scale-110 active:scale-95 text-sm"
                                            >
                                                +
                                            </button>
                                        </div>

                                        {/* Total - Right */}
                                        <div className="text-right w-20">
                                            <div className="text-xs text-slate-400 font-medium">Total</div>
                                            <div className="text-lg font-bold bg-gradient-to-r from-emerald-600 to-emerald-500 bg-clip-text text-transparent">
                                                ₹{item.quantity * item.price_at_booking}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Footer Section */}
                    <div className="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden hover:shadow-xl transition-shadow">
                        <div className="p-6 space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                {/* Status */}
                                <div>
                                    <label className="block text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
                                        <span className="w-1.5 h-1.5 bg-amber-500 rounded-full"></span>
                                        Rental Status
                                    </label>
                                    <select
                                        value={status}
                                        onChange={(e) => setStatus(e.target.value as 'active' | 'returned' | 'overdue')}
                                        className="w-full border-2 border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent bg-slate-50 hover:border-slate-300 transition-all font-medium text-slate-700"
                                    >
                                        <option value="active">🔵 Active</option>
                                        <option value="returned">✅ Returned</option>
                                        <option value="overdue">🔴 Overdue</option>
                                    </select>
                                </div>

                                {/* Total Amount */}
                                <div className="bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-xl p-5 border-2 border-emerald-200">
                                    <div className="text-sm font-semibold text-emerald-700 mb-2 flex items-center gap-2">
                                        <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                                        Grand Total
                                    </div>
                                    <div className="text-4xl font-bold bg-gradient-to-r from-emerald-600 to-emerald-500 bg-clip-text text-transparent">
                                        ₹{totalAmount}
                                    </div>
                                    <div className="text-xs text-emerald-600 mt-1 font-medium">
                                        {items.length} item{items.length !== 1 ? 's' : ''} • {items.reduce((sum, item) => sum + item.quantity, 0)} units
                                    </div>
                                </div>
                            </div>

                            {/* Save Button */}
                            <button
                                onClick={handleSave}
                                disabled={saving}
                                className="w-full bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 disabled:from-slate-400 disabled:to-slate-500 text-white font-bold py-4 px-6 rounded-xl transition-all focus:outline-none focus:ring-4 focus:ring-emerald-300 flex items-center justify-center gap-3 shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] disabled:hover:scale-100"
                            >
                                <Save size={22} />
                                <span className="text-lg">{saving ? 'Saving Changes...' : 'Save Changes'}</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {toast && (
                <Toast
                    message={toast.message}
                    type={toast.type}
                    onClose={() => setToast(null)}
                />
            )}
        </div>
    );
}
