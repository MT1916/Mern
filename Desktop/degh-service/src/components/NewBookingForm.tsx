import { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { CustomerInfoStep } from './booking-steps/CustomerInfoStep';
import { ItemsSelectionStep, SelectedItem } from './booking-steps/ItemsSelectionStep';
import { supabase } from '../lib/supabase';
import type { BookingWithDetails } from './Dashboard';
import { Toast, ToastType } from './Toast';

interface NewBookingFormProps {
  onClose: () => void;
  editingBooking?: BookingWithDetails | null;
}

export interface ItemQuantity {
  degh: number;
  chair: number;
  table: number;
  tangna: number;
  plate: number;
}

export interface BookingData {
  customerName: string;
  contactNumber: string;
  address: string;
  rentalDate: string;
  returnDate: string;
  notes: string;
  items: ItemQuantity;
  existingCustomerId?: string;
}

export function NewBookingForm({ onClose, editingBooking }: NewBookingFormProps) {
  const [currentStep, setCurrentStep] = useState<'customer' | 'items'>('customer');
  const [bookingData, setBookingData] = useState<BookingData>({
    customerName: '',
    contactNumber: '',
    address: '',
    rentalDate: new Date().toISOString().split('T')[0],
    returnDate: '',
    notes: '',
    items: {
      degh: 0,
      chair: 0,
      table: 0,
      tangna: 0,
      plate: 0,
    },
  });
  const [submitting, setSubmitting] = useState(false);
  const [initialData, setInitialData] = useState<BookingData | null>(null);
  const [modifiedFields, setModifiedFields] = useState<Set<string>>(new Set());
  const [initialItems, setInitialItems] = useState<SelectedItem[]>([]);
  const [toast, setToast] = useState<{ message: string; type: ToastType } | null>(null);

  // Initialize form with editing data
  useEffect(() => {
    if (editingBooking) {
      const initialBookingData = {
        customerName: editingBooking.customer.name,
        contactNumber: editingBooking.customer.contact_number,
        address: editingBooking.customer.address || '',
        rentalDate: editingBooking.rental_date.split('T')[0],
        returnDate: editingBooking.return_date ? editingBooking.return_date.split('T')[0] : '',
        notes: editingBooking.notes || '',
        items: {
          degh: 0,
          chair: 0,
          table: 0,
          tangna: 0,
          plate: 0,
        },
        existingCustomerId: editingBooking.customer_id,
      };
      setBookingData(initialBookingData);
      setInitialData(initialBookingData);

      // Convert booking items to SelectedItem format
      const selectedItems: SelectedItem[] = editingBooking.items.map(item => ({
        itemId: item.item_id,
        name: item.item_name || 'Unknown Item',
        price: item.price_at_booking,
        quantity: item.quantity,
      }));
      setInitialItems(selectedItems);
    }
  }, [editingBooking]);

  // Track changes
  useEffect(() => {
    if (editingBooking && initialData) {
      const changes = new Set<string>();

      if (bookingData.customerName !== initialData.customerName) changes.add('customerName');
      if (bookingData.contactNumber !== initialData.contactNumber) changes.add('contactNumber');
      if (bookingData.address !== initialData.address) changes.add('address');
      if (bookingData.rentalDate !== initialData.rentalDate) changes.add('rentalDate');
      if (bookingData.returnDate !== initialData.returnDate) changes.add('returnDate');
      if (bookingData.notes !== initialData.notes) changes.add('notes');

      setModifiedFields(changes);
    }
  }, [bookingData, initialData, editingBooking]);

  function handleCustomerInfoNext(data: Partial<BookingData>) {
    setBookingData({ ...bookingData, ...data });
    setCurrentStep('items');
  }

  function handleItemsBack() {
    setCurrentStep('customer');
  }

  async function handleItemsSubmit(items: SelectedItem[]) {
    setSubmitting(true);

    try {
      // If editing, update existing booking
      if (editingBooking) {
        // Update customer info
        const { error: customerError } = await supabase
          .from('customers')
          .update({
            name: bookingData.customerName.trim(),
            contact_number: bookingData.contactNumber.trim(),
            address: bookingData.address.trim() || null,
          })
          .eq('id', editingBooking.customer_id);

        if (customerError) throw customerError;

        // Update rental info
        const { error: rentalError } = await supabase
          .from('rentals')
          .update({
            rental_date: bookingData.rentalDate,
            return_date: bookingData.returnDate || null,
            notes: bookingData.notes || null,
            updated_at: new Date().toISOString(),
          })
          .eq('id', editingBooking.id);

        if (rentalError) throw rentalError;

        // Delete existing rental items
        const { error: deleteError } = await supabase
          .from('rental_items')
          .delete()
          .eq('rental_id', editingBooking.id);

        if (deleteError) throw deleteError;

        // Insert new rental items
        const itemsToInsert = items.map(item => ({
          rental_id: editingBooking.id,
          item_id: item.itemId,
          quantity: item.quantity,
          price_at_booking: item.price,
        }));

        const { error: itemsError } = await supabase
          .from('rental_items')
          .insert(itemsToInsert);

        if (itemsError) throw itemsError;

        setToast({ message: 'Booking updated successfully! 🎉', type: 'success' });
        setTimeout(() => onClose(), 1500);
        return;
      }

      // Otherwise, create new booking
      let customerId = bookingData.existingCustomerId;

      if (!customerId) {
        const { data: customerData, error: customerError } = await supabase
          .from('customers')
          .insert({
            name: bookingData.customerName.trim(),
            contact_number: bookingData.contactNumber.trim(),
            address: bookingData.address.trim() || null,
          })
          .select()
          .maybeSingle();

        if (customerError) {
          console.error('Customer error:', customerError);
          throw customerError;
        }
        if (!customerData) throw new Error('Failed to create customer');
        customerId = customerData.id;
      }

      const { data: rentalData, error: rentalError } = await supabase
        .from('rentals')
        .insert({
          customer_id: customerId,
          rental_date: bookingData.rentalDate,
          return_date: bookingData.returnDate || null,
          status: 'active',
          notes: bookingData.notes || null,
        })
        .select()
        .maybeSingle();

      if (rentalError) {
        console.error('Rental error:', rentalError);
        throw rentalError;
      }
      if (!rentalData) throw new Error('Failed to create rental');

      const itemsToInsert = items.map(item => ({
        rental_id: rentalData.id,
        item_id: item.itemId,
        quantity: item.quantity,
        price_at_booking: item.price,
      }));

      const { error: itemsError } = await supabase
        .from('rental_items')
        .insert(itemsToInsert);

      if (itemsError) {
        console.error('Items error:', itemsError);
        throw itemsError;
      }

      setToast({ message: 'Order successfully placed! 🎉', type: 'success' });
      setTimeout(() => onClose(), 1500);
    } catch (error) {
      console.error('Error creating booking:', error);
      const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
      setToast({
        message: `Failed to ${editingBooking ? 'update' : 'create'} booking: ${errorMessage}`,
        type: 'error'
      });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <>
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          <div className="bg-gradient-to-r from-emerald-600 to-emerald-700 p-6 flex items-center justify-between sticky top-0 z-10">
            <div>
              <h2 className="text-2xl font-bold text-white">
                {editingBooking ? 'Edit Booking' : 'Create New Booking'}
              </h2>
              <p className="text-emerald-100 text-sm mt-1">
                {currentStep === 'customer' ? 'Step 1: Customer Information' : 'Step 2: Select Items'}
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-emerald-800 p-2 rounded-lg transition-colors"
            >
              <X size={24} />
            </button>
          </div>

          {currentStep === 'customer' ? (
            <CustomerInfoStep
              initialData={bookingData}
              onNext={handleCustomerInfoNext}
              onCancel={onClose}
              modifiedFields={modifiedFields}
            />
          ) : (
            <ItemsSelectionStep
              onBack={handleItemsBack}
              onSubmit={handleItemsSubmit}
              submitting={submitting}
              initialItems={initialItems}
              isEditMode={!!editingBooking}
            />
          )}
        </div>
      </div>

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </>
  );
}
