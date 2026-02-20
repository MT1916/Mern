import { useEffect, useState, useCallback } from 'react';
import { supabase } from '../lib/supabase';
import { Plus, Calendar, Filter } from 'lucide-react';
import { CompactRentalCard } from './CompactRentalCard';
import { NewBookingForm } from './NewBookingForm';
import { StatsOverview } from './StatsOverview';

export interface Customer {
  id: string;
  name: string;
  contact_number: string;
  address: string | null;
  created_at: string;
  updated_at: string;
}

export interface Booking {
  id: string;
  customer_id: string;
  rental_date: string;
  return_date: string | null;
  status: 'active' | 'returned' | 'overdue';
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface BookingItem {
  id: string;
  rental_id: string;
  item_id: string;
  quantity: number;
  price_at_booking: number;
  item_name?: string;
  created_at: string;
}

export interface BookingWithDetails extends Booking {
  customer: Customer;
  items: BookingItem[];
}

export function Dashboard() {
  const [bookings, setBookings] = useState<BookingWithDetails[]>([]);
  const [filteredBookings, setFilteredBookings] = useState<BookingWithDetails[]>([]);
  const [loading, setLoading] = useState(true);
  const [showNewBookingForm, setShowNewBookingForm] = useState(false);
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'returned' | 'overdue'>('all');

  useEffect(() => {
    loadBookings();
  }, []);

  const filterBookings = useCallback(() => {
    if (statusFilter === 'all') {
      setFilteredBookings(bookings);
    } else {
      setFilteredBookings(bookings.filter(b => b.status === statusFilter));
    }
  }, [bookings, statusFilter]);

  useEffect(() => {
    filterBookings();
  }, [filterBookings]);

  async function loadBookings() {
    try {
      // Fetch all rentals first
      const { data: rentalsData, error: rentalsError } = await supabase
        .from('rentals')
        .select('*')
        .order('rental_date', { ascending: false });

      if (rentalsError) throw rentalsError;
      if (!rentalsData || rentalsData.length === 0) {
        setBookings([]);
        setLoading(false);
        return;
      }

      // Get unique customer IDs and rental IDs
      const customerIds = [...new Set(rentalsData.map(r => r.customer_id))];
      const rentalIds = rentalsData.map(r => r.id);

      // Fetch ALL customers and items in parallel (batch queries)
      const [customersResponse, itemsResponse] = await Promise.all([
        supabase.from('customers').select('*').in('id', customerIds),
        supabase.from('rental_items').select(`
          id,
          rental_id,
          item_id,
          quantity,
          price_at_booking,
          created_at,
          items (name)
        `).in('rental_id', rentalIds)
      ]);

      const { data: customersData, error: customersError } = customersResponse;
      const { data: itemsData, error: itemsError } = itemsResponse;

      if (customersError) throw customersError;
      if (itemsError) throw itemsError;

      // Create lookup maps for O(1) access
      const customersMap = new Map(
        (customersData || []).map(customer => [customer.id, customer])
      );

      const itemsMap = new Map<string, any[]>();
      (itemsData || []).forEach(item => {
        const rentalId = item.rental_id;
        if (!itemsMap.has(rentalId)) {
          itemsMap.set(rentalId, []);
        }
        itemsMap.get(rentalId)?.push({
          ...item,
          item_name: (item as { items?: { name: string } }).items?.name,
        });
      });

      // Combine data efficiently
      const bookingsWithDetails: BookingWithDetails[] = rentalsData
        .map(rental => {
          const customer = customersMap.get(rental.customer_id);
          const items = itemsMap.get(rental.id) || [];

          if (!customer) return null;

          return {
            ...rental,
            customer,
            items,
          };
        })
        .filter((booking): booking is BookingWithDetails => booking !== null);

      setBookings(bookingsWithDetails);
    } catch (error) {
      console.error('Error loading bookings:', error);
    } finally {
      setLoading(false);
    }
  }

  function handleNewBooking() {
    setShowNewBookingForm(true);
  }

  function handleCloseForm() {
    setShowNewBookingForm(false);
    loadBookings();
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center">
        <div className="text-slate-600 text-lg">Loading bookings...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 className="text-4xl font-bold text-slate-800 mb-2">Booking Manager</h1>
              <p className="text-slate-600">Track and manage all your catering rental bookings</p>
            </div>
            <button
              onClick={handleNewBooking}
              className="flex items-center justify-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-lg font-medium transition-colors shadow-lg hover:shadow-xl"
            >
              <Plus size={20} />
              New Booking
            </button>
          </div>
        </div>

        <StatsOverview bookings={bookings} />

        <div className="mb-6 bg-white rounded-lg shadow-md p-4">
          <div className="flex items-center gap-4 flex-wrap">
            <div className="flex items-center gap-2 text-slate-700">
              <Filter size={20} />
              <span className="font-medium">Filter by Status:</span>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setStatusFilter('all')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${statusFilter === 'all'
                  ? 'bg-slate-700 text-white'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  }`}
              >
                All ({bookings.length})
              </button>
              <button
                onClick={() => setStatusFilter('active')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${statusFilter === 'active'
                  ? 'bg-blue-600 text-white'
                  : 'bg-blue-50 text-blue-700 hover:bg-blue-100'
                  }`}
              >
                Active ({bookings.filter(b => b.status === 'active').length})
              </button>
              <button
                onClick={() => setStatusFilter('overdue')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${statusFilter === 'overdue'
                  ? 'bg-red-600 text-white'
                  : 'bg-red-50 text-red-700 hover:bg-red-100'
                  }`}
              >
                Overdue ({bookings.filter(b => b.status === 'overdue').length})
              </button>
              <button
                onClick={() => setStatusFilter('returned')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${statusFilter === 'returned'
                  ? 'bg-emerald-600 text-white'
                  : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100'
                  }`}
              >
                Returned ({bookings.filter(b => b.status === 'returned').length})
              </button>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredBookings.length === 0 ? (
            <div className="col-span-full bg-white rounded-xl shadow-lg p-12 text-center">
              <Calendar size={64} className="mx-auto text-slate-300 mb-4" />
              <h3 className="text-xl font-semibold text-slate-700 mb-2">
                {statusFilter === 'all' ? 'No Bookings Yet' : `No ${statusFilter} Bookings`}
              </h3>
              <p className="text-slate-500 mb-6">
                {statusFilter === 'all'
                  ? 'Create your first booking to get started'
                  : 'Try selecting a different filter'}
              </p>
              {statusFilter === 'all' && (
                <button
                  onClick={handleNewBooking}
                  className="inline-flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                >
                  <Plus size={20} />
                  Create First Booking
                </button>
              )}
            </div>
          ) : (
            filteredBookings.map((booking) => (
              <CompactRentalCard
                key={booking.id}
                booking={booking}
              />
            ))
          )}
        </div>
      </div>

      {showNewBookingForm && (
        <NewBookingForm
          onClose={handleCloseForm}
        />
      )}
    </div>
  );
}
