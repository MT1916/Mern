import { useState, useEffect } from 'react';
import { User, MapPin, Phone, Calendar, ArrowRight } from 'lucide-react';
import { supabase } from '../../lib/supabase';
import type { BookingData } from '../NewBookingForm';

interface CustomerInfoStepProps {
  initialData: BookingData;
  onNext: (data: Partial<BookingData>) => void;
  onCancel: () => void;
  modifiedFields?: Set<string>;
}

interface Customer {
  id: string;
  name: string;
  contact_number: string;
  address: string | null;
}

export function CustomerInfoStep({ initialData, onNext, onCancel, modifiedFields }: CustomerInfoStepProps) {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [isNewCustomer, setIsNewCustomer] = useState(true);
  const [selectedCustomerId, setSelectedCustomerId] = useState('');
  const [customerName, setCustomerName] = useState(initialData.customerName);
  const [contactNumber, setContactNumber] = useState(initialData.contactNumber);
  const [address, setAddress] = useState(initialData.address);
  const [rentalDate, setRentalDate] = useState(initialData.rentalDate);
  const [returnDate, setReturnDate] = useState(initialData.returnDate);
  const [notes, setNotes] = useState(initialData.notes);

  useEffect(() => {
    loadCustomers();
  }, []);

  async function loadCustomers() {
    try {
      const { data, error } = await supabase
        .from('customers')
        .select('*')
        .order('name');

      if (error) throw error;
      setCustomers(data || []);
    } catch (error) {
      console.error('Error loading customers:', error);
    }
  }

  function handleCustomerSelect(customerId: string) {
    setSelectedCustomerId(customerId);
    const customer = customers.find(c => c.id === customerId);
    if (customer) {
      setCustomerName(customer.name);
      setContactNumber(customer.contact_number);
      setAddress(customer.address || '');
    }
  }

  function handleNext() {
    if (isNewCustomer) {
      if (!customerName.trim() || !contactNumber.trim() || !address.trim()) {
        alert('Please fill in all required fields');
        return;
      }
      onNext({
        customerName,
        contactNumber,
        address,
        rentalDate,
        returnDate,
        notes,
      });
    } else {
      if (!selectedCustomerId) {
        alert('Please select a customer');
        return;
      }
      onNext({
        existingCustomerId: selectedCustomerId,
        customerName,
        contactNumber,
        address,
        rentalDate,
        returnDate,
        notes,
      });
    }
  }

  return (
    <div className="p-6 space-y-6">
      <div className="bg-slate-50 rounded-lg p-5 border-2 border-slate-200">
        <div className="flex items-center gap-2 mb-4">
          <User className="text-slate-700" size={20} />
          <h3 className="text-lg font-bold text-slate-800">Customer Details</h3>
        </div>

        <div className="flex gap-3 mb-4">
          <button
            type="button"
            onClick={() => {
              setIsNewCustomer(true);
              setSelectedCustomerId('');
              setCustomerName(initialData.customerName);
              setContactNumber(initialData.contactNumber);
              setAddress(initialData.address);
            }}
            className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${isNewCustomer
                ? 'bg-emerald-600 text-white'
                : 'bg-white text-slate-700 border border-slate-300 hover:bg-slate-50'
              }`}
          >
            New Customer
          </button>
          <button
            type="button"
            onClick={() => setIsNewCustomer(false)}
            className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${!isNewCustomer
                ? 'bg-emerald-600 text-white'
                : 'bg-white text-slate-700 border border-slate-300 hover:bg-slate-50'
              }`}
          >
            Existing Customer
          </button>
        </div>

        {!isNewCustomer && (
          <div className="mb-4">
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Select Customer *
            </label>
            <select
              value={selectedCustomerId}
              onChange={(e) => handleCustomerSelect(e.target.value)}
              className="w-full px-4 py-3 border-2 border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 bg-white"
            >
              <option value="">Choose a customer</option>
              {customers.map((customer) => (
                <option key={customer.id} value={customer.id}>
                  {customer.name} - {customer.contact_number}
                </option>
              ))}
            </select>
          </div>
        )}

        {(isNewCustomer || selectedCustomerId) && (
          <div className="space-y-4">
            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-slate-700 mb-2">
                <User size={16} />
                Customer Name *
              </label>
              <input
                type="text"
                value={customerName}
                onChange={(e) => setCustomerName(e.target.value)}
                disabled={!isNewCustomer}
                className={`w-full px-4 py-3 border-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 disabled:bg-slate-100 disabled:text-slate-600 ${modifiedFields?.has('customerName')
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-slate-300 focus:border-emerald-500'
                  }`}
                placeholder="Enter customer name"
              />
            </div>

            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-slate-700 mb-2">
                <Phone size={16} />
                Contact Number *
              </label>
              <input
                type="tel"
                value={contactNumber}
                onChange={(e) => setContactNumber(e.target.value)}
                disabled={!isNewCustomer}
                className={`w-full px-4 py-3 border-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 disabled:bg-slate-100 disabled:text-slate-600 ${modifiedFields?.has('contactNumber')
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-slate-300 focus:border-emerald-500'
                  }`}
                placeholder="Enter phone number"
              />
            </div>

            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-slate-700 mb-2">
                <MapPin size={16} />
                Delivery Address *
              </label>
              <textarea
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                disabled={!isNewCustomer}
                rows={3}
                className={`w-full px-4 py-3 border-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 disabled:bg-slate-100 disabled:text-slate-600 ${modifiedFields?.has('address')
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-slate-300 focus:border-emerald-500'
                  }`}
                placeholder="Enter complete delivery address"
              />
            </div>
          </div>
        )}
      </div>

      <div className="bg-slate-50 rounded-lg p-5 border-2 border-slate-200">
        <div className="flex items-center gap-2 mb-4">
          <Calendar className="text-slate-700" size={20} />
          <h3 className="text-lg font-bold text-slate-800">Booking Details</h3>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Rental Date *
            </label>
            <input
              type="date"
              value={rentalDate}
              onChange={(e) => setRentalDate(e.target.value)}
              className={`w-full px-4 py-3 border-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 ${modifiedFields?.has('rentalDate')
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-slate-300 focus:border-emerald-500'
                }`}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Return Date (Optional)
            </label>
            <input
              type="date"
              value={returnDate}
              onChange={(e) => setReturnDate(e.target.value)}
              className={`w-full px-4 py-3 border-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 ${modifiedFields?.has('returnDate')
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-slate-300 focus:border-emerald-500'
                }`}
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Notes (Optional)
          </label>
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            rows={2}
            className={`w-full px-4 py-3 border-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 ${modifiedFields?.has('notes')
                ? 'border-blue-500 bg-blue-50'
                : 'border-slate-300 focus:border-emerald-500'
              }`}
            placeholder="Add any special instructions or notes"
          />
        </div>
      </div>

      <div className="flex gap-3 pt-4 border-t">
        <button
          type="button"
          onClick={onCancel}
          className="flex-1 px-6 py-3 border-2 border-slate-300 text-slate-700 rounded-lg font-semibold hover:bg-slate-50 transition-colors"
        >
          Cancel
        </button>
        <button
          type="button"
          onClick={handleNext}
          className="flex-1 px-6 py-3 bg-emerald-600 text-white rounded-lg font-semibold hover:bg-emerald-700 transition-colors shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
        >
          Next: Select Items
          <ArrowRight size={20} />
        </button>
      </div>
    </div>
  );
}
