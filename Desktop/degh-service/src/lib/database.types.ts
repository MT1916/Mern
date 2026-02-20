export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Database {
  public: {
    Tables: {
      customers: {
        Row: {
          id: string
          name: string
          contact_number: string
          address: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          name: string
          contact_number: string
          address?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          name?: string
          contact_number?: string
          address?: string | null
          created_at?: string
          updated_at?: string
        }
      }
      items: {
        Row: {
          id: string
          name: string
          category: string | null
          price: number
          is_active: boolean
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          name: string
          category?: string | null
          price: number
          is_active?: boolean
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          name?: string
          category?: string | null
          price?: number
          is_active?: boolean
          created_at?: string
          updated_at?: string
        }
      }
      rentals: {
        Row: {
          id: string
          customer_id: string
          rental_date: string
          return_date: string | null
          status: 'active' | 'returned' | 'overdue'
          notes: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          customer_id: string
          rental_date: string
          return_date?: string | null
          status?: 'active' | 'returned' | 'overdue'
          notes?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          customer_id?: string
          rental_date?: string
          return_date?: string | null
          status?: 'active' | 'returned' | 'overdue'
          notes?: string | null
          created_at?: string
          updated_at?: string
        }
      }
      rental_items: {
        Row: {
          id: string
          rental_id: string
          item_id: string
          quantity: number
          price_at_booking: number
          created_at: string
        }
        Insert: {
          id?: string
          rental_id: string
          item_id: string
          quantity: number
          price_at_booking: number
          created_at?: string
        }
        Update: {
          id?: string
          rental_id?: string
          item_id?: string
          quantity?: number
          price_at_booking?: number
          created_at?: string
        }
      }
    }
  }
}
