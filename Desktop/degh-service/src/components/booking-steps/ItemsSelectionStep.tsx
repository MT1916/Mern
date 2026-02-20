import { useState, useEffect, useRef } from 'react';
import { Package, ArrowLeft, Check, Search, X, Plus, Minus, Edit2 } from 'lucide-react';
import { supabase } from '../../lib/supabase';

interface ItemsSelectionStepProps {
  onBack: () => void;
  onSubmit: (items: SelectedItem[]) => void;
  submitting: boolean;
  initialItems?: SelectedItem[];
  isEditMode?: boolean;
}

interface Item {
  id: string;
  name: string;
  price: number;
  category: string | null;
  is_active: boolean;
}

export interface SelectedItem {
  itemId: string;
  name: string;
  price: number;
  quantity: number;
}

const categoryIcons: Record<string, string> = {
  'Cooking': '🍲',
  'Utensils': '🍴',
  'Serving': '🍽️',
  'Storage': '📦',
  'Facilities': '🚿',
  'Seating': '🪑',
  'Furniture': '🪑',
  'Decoration': '🎨',
  'Equipment': '🔧',
  'Comfort': '🛏️',
};

export function ItemsSelectionStep({ onBack, onSubmit, submitting, initialItems, isEditMode }: ItemsSelectionStepProps) {
  const [items, setItems] = useState<Item[]>([]);
  const [selectedItems, setSelectedItems] = useState<Map<string, SelectedItem>>(new Map());
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [activeItemId, setActiveItemId] = useState<string | null>(null);
  const [inputValue, setInputValue] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);
  const [filteredItemsList, setFilteredItemsList] = useState<Item[]>([]);

  useEffect(() => {
    loadItems();
  }, []);

  // Initialize with existing items in edit mode
  useEffect(() => {
    if (initialItems && initialItems.length > 0) {
      const itemsMap = new Map<string, SelectedItem>();
      initialItems.forEach(item => {
        itemsMap.set(item.itemId, item);
      });
      setSelectedItems(itemsMap);
    }
  }, [initialItems]);

  useEffect(() => {
    if (activeItemId && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [activeItemId]);

  async function loadItems() {
    try {
      const { data, error } = await supabase
        .from('items')
        .select('*')
        .eq('is_active', true)
        .order('category', { ascending: true })
        .order('price', { ascending: false });

      if (error) throw error;
      setItems(data || []);
    } catch (error) {
      console.error('Error loading items:', error);
    } finally {
      setLoading(false);
    }
  }

  function handleAddClick(item: Item) {
    const selectedItem = selectedItems.get(item.id);
    const currentQuantity = selectedItem?.quantity || 0;
    setActiveItemId(item.id);
    setInputValue(currentQuantity.toString());
  }

  function handleIncrease() {
    const current = parseInt(inputValue) || 0;
    setInputValue((current + 1).toString());
  }

  function handleDecrease() {
    const current = parseInt(inputValue) || 0;
    if (current > 0) {
      setInputValue((current - 1).toString());
    }
  }

  function handleConfirm() {
    if (!activeItemId) return;

    const quantity = parseInt(inputValue) || 0;

    if (quantity === 0) {
      setSelectedItems(prev => {
        const newMap = new Map(prev);
        newMap.delete(activeItemId);
        return newMap;
      });
    } else {
      const item = items.find(i => i.id === activeItemId);
      if (item) {
        setSelectedItems(prev => {
          const newMap = new Map(prev);
          newMap.set(activeItemId, {
            itemId: item.id,
            name: item.name,
            price: item.price,
            quantity,
          });
          return newMap;
        });
      }
    }

    openNextItem();
  }

  function openNextItem() {
    if (!activeItemId) return;

    const currentIndex = filteredItemsList.findIndex(item => item.id === activeItemId);

    if (currentIndex !== -1 && currentIndex < filteredItemsList.length - 1) {
      const nextItem = filteredItemsList[currentIndex + 1];
      const selectedItem = selectedItems.get(nextItem.id);
      const currentQuantity = selectedItem?.quantity || 0;
      setActiveItemId(nextItem.id);
      setInputValue(currentQuantity.toString());
    } else {
      setInputValue('');
      setActiveItemId(null);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleConfirm();
    }
  }

  function handleDelete() {
    if (activeItemId) {
      setSelectedItems(prev => {
        const newMap = new Map(prev);
        newMap.delete(activeItemId);
        return newMap;
      });
      setInputValue('');
      setActiveItemId(null);
    }
  }

  function handleSubmit() {
    const itemsArray = Array.from(selectedItems.values());
    if (itemsArray.length === 0) {
      alert('Please select at least one item');
      return;
    }
    onSubmit(itemsArray);
  }

  const categories = ['all', ...new Set(items.map(item => item.category).filter(Boolean))];

  const filteredItems = items.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  useEffect(() => {
    setFilteredItemsList(filteredItems);
  }, [filteredItems]);

  const groupedItems = filteredItems.reduce((acc, item) => {
    const category = item.category || 'Other';
    if (!acc[category]) acc[category] = [];
    acc[category].push(item);
    return acc;
  }, {} as Record<string, Item[]>);

  const totalQuantity = Array.from(selectedItems.values()).reduce((sum, item) => sum + item.quantity, 0);
  const totalPrice = Array.from(selectedItems.values()).reduce((sum, item) => sum + (item.quantity * item.price), 0);

  if (loading) {
    return (
      <div className="p-6 flex items-center justify-center">
        <div className="text-slate-600">Loading items...</div>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-6 space-y-4 md:space-y-6">
      <div className="bg-gradient-to-r from-emerald-50 to-teal-50 rounded-lg p-4 md:p-5 border-2 border-emerald-200">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 md:gap-4">
          <div className="flex items-center gap-2 md:gap-3">
            <Package className="text-emerald-700" size={20} />
            <div>
              <h3 className="text-base md:text-lg font-bold text-slate-800">Select Rental Items</h3>
              <p className="text-xs md:text-sm text-slate-600">Click Add to select quantity</p>
            </div>
          </div>
          <div className="flex gap-2 md:gap-3">
            {totalQuantity > 0 && (
              <>
                <div className="bg-white px-3 md:px-4 py-2 rounded-lg border-2 border-emerald-300">
                  <div className="text-xs text-slate-600">Items</div>
                  <div className="font-bold text-emerald-700 text-lg">{totalQuantity}</div>
                </div>
                <div className="bg-emerald-600 text-white px-3 md:px-4 py-2 rounded-lg font-bold">
                  <div className="text-xs opacity-90">Total</div>
                  <div className="text-lg">₹{totalPrice}</div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-2 md:gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={18} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search items..."
            className="w-full pl-9 md:pl-10 pr-4 py-2 md:py-2.5 border-2 border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
          />
        </div>
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="px-3 md:px-4 py-2 md:py-2.5 border-2 border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 bg-white"
        >
          {categories.map(cat => (
            <option key={cat || 'all'} value={cat || ''}>
              {cat === 'all' ? 'All Categories' : cat}
            </option>
          ))}
        </select>
      </div>

      <div className="space-y-5 md:space-y-6 max-h-[500px] md:max-h-[600px] overflow-y-auto pr-2">
        {Object.entries(groupedItems).map(([category, categoryItems]) => (
          <div key={category}>
            <div className="flex items-center gap-2 mb-2 md:mb-3 sticky top-0 bg-white py-2 z-10">
              <span className="text-xl md:text-2xl">{categoryIcons[category] || '📦'}</span>
              <h4 className="text-base md:text-lg font-bold text-slate-800">{category}</h4>
              <div className="flex-1 h-px bg-slate-200"></div>
            </div>

            <div className="space-y-2">
              {categoryItems.map((item) => {
                const selectedItem = selectedItems.get(item.id);
                const quantity = selectedItem?.quantity || 0;

                return (
                  <div
                    key={item.id}
                    className="bg-white rounded-lg border-2 border-slate-200 hover:border-emerald-300 p-3 md:p-4 transition-all"
                  >
                    <div className="grid grid-cols-12 gap-2 md:gap-3 items-center">
                      <div className="col-span-5 md:col-span-6 text-left">
                        <div className="font-semibold text-slate-800 text-sm md:text-base line-clamp-2">
                          {item.name}
                        </div>
                      </div>

                      <div className="col-span-4 md:col-span-3 text-center">
                        <div className="text-xs md:text-sm text-slate-600 mb-0.5">Price</div>
                        <div className="font-bold text-emerald-700 text-base md:text-lg">
                          ₹{item.price}
                        </div>
                      </div>

                      <div className="col-span-3 flex gap-1">
                        <button
                          onClick={() => handleAddClick(item)}
                          className={`flex-1 py-2 md:py-2.5 px-2 rounded-lg font-bold transition-all text-center text-sm md:text-base ${quantity > 0
                            ? 'bg-emerald-600 text-white hover:bg-emerald-700'
                            : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                            }`}
                        >
                          {quantity === 0 ? 'Add' : quantity}
                        </button>
                        {quantity > 0 && (
                          <button
                            onClick={() => handleAddClick(item)}
                            className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 md:py-2.5 px-2 rounded-lg transition-all"
                            title="Edit quantity"
                          >
                            <Edit2 size={16} />
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {filteredItems.length === 0 && (
        <div className="text-center py-8 md:py-12">
          <Package size={40} className="mx-auto text-slate-300 mb-2 md:mb-3" />
          <p className="text-slate-600 text-sm md:text-base">No items found</p>
        </div>
      )}

      {activeItemId && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-md">
            <div className="bg-emerald-600 text-white p-4 flex items-center justify-between">
              <div className="flex-1">
                <div className="text-sm opacity-90">Selected Item</div>
                <div className="text-lg font-bold line-clamp-2">
                  {items.find(i => i.id === activeItemId)?.name}
                </div>
              </div>
              <button
                onClick={() => {
                  setActiveItemId(null);
                  setInputValue('');
                }}
                className="p-2 hover:bg-emerald-700 rounded-lg transition-colors flex-shrink-0 ml-2"
              >
                <X size={20} />
              </button>
            </div>

            <div className="p-6 space-y-4">
              <div className="bg-slate-100 rounded-lg p-6 text-center border-2 border-slate-300">
                <div className="text-xs text-slate-600 mb-2 font-semibold">QUANTITY</div>
                <div className="text-7xl font-bold text-emerald-700 mb-4">
                  {inputValue || '0'}
                </div>

                <div className="flex gap-3 justify-center">
                  <button
                    onClick={handleDecrease}
                    className="bg-red-500 hover:bg-red-600 text-white font-bold p-3 rounded-lg transition-colors active:bg-red-700"
                  >
                    <Minus size={24} />
                  </button>
                  <button
                    onClick={handleIncrease}
                    className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold p-3 rounded-lg transition-colors active:bg-emerald-800"
                  >
                    <Plus size={24} />
                  </button>
                </div>
              </div>

              <input
                ref={inputRef}
                type="number"
                min="0"
                value={inputValue}
                onChange={(e) => {
                  let value = e.target.value;
                  if (value.startsWith('0') && value.length > 1) {
                    value = value.replace(/^0+/, '');
                  }
                  setInputValue(value);
                }}
                onKeyDown={handleKeyDown}
                placeholder="Enter quantity"
                className="w-full px-4 py-3 border-2 border-emerald-300 rounded-lg text-center text-2xl font-bold text-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                inputMode="numeric"
              />

              <div className="grid grid-cols-2 gap-2 pt-2">
                <button
                  onClick={handleDelete}
                  className="bg-red-600 hover:bg-red-700 text-white font-bold py-3 rounded-lg transition-colors active:bg-red-800"
                >
                  Delete
                </button>
                <button
                  onClick={handleConfirm}
                  className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 rounded-lg transition-colors active:bg-emerald-800"
                >
                  Confirm
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="flex gap-2 md:gap-3 pt-4 md:pt-6 border-t-2 sticky bottom-0 bg-white">
        <button
          type="button"
          onClick={onBack}
          className="px-4 md:px-6 py-2 md:py-3 border-2 border-slate-300 text-slate-700 rounded-lg font-semibold hover:bg-slate-50 transition-colors flex items-center justify-center gap-2 text-sm md:text-base"
        >
          <ArrowLeft size={18} />
          <span className="hidden md:inline">Back</span>
        </button>
        <button
          type="button"
          onClick={handleSubmit}
          disabled={submitting || totalQuantity === 0}
          className="flex-1 px-4 md:px-6 py-2 md:py-3 bg-emerald-600 text-white rounded-lg font-semibold hover:bg-emerald-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl flex items-center justify-center gap-2 text-sm md:text-base whitespace-nowrap"
        >
          {submitting ? (
            <>{isEditMode ? 'Updating Order...' : 'Creating Order...'}</>
          ) : (
            <>
              <Check size={18} />
              <span>{isEditMode ? 'Update Order' : 'Create Order'}</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
