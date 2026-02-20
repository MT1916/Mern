/*
  # Catering Rental Management System Schema

  ## Overview
  This migration creates the database structure for managing catering rental items
  and customer information for a rental business.

  ## New Tables
  
  ### `customers`
  Stores customer information for rental tracking
  - `id` (uuid, primary key) - Unique identifier for each customer
  - `name` (text, required) - Customer's full name
  - `contact_number` (text, required) - Customer's phone number
  - `created_at` (timestamptz) - Record creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ### `rentals`
  Tracks individual rental transactions
  - `id` (uuid, primary key) - Unique identifier for each rental
  - `customer_id` (uuid, foreign key) - References customers table
  - `rental_date` (date, required) - Date when items were rented
  - `return_date` (date, optional) - Expected/actual return date
  - `status` (text, required) - Rental status: 'active', 'returned', 'overdue'
  - `notes` (text, optional) - Additional notes about the rental
  - `created_at` (timestamptz) - Record creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ### `rental_items`
  Stores individual items included in each rental
  - `id` (uuid, primary key) - Unique identifier for each rental item
  - `rental_id` (uuid, foreign key) - References rentals table
  - `item_type` (text, required) - Type of item: 'degh', 'chair', 'table', 'tangna', 'plate'
  - `quantity` (integer, required) - Number of items rented
  - `created_at` (timestamptz) - Record creation timestamp

  ## Security
  - Enable Row Level Security (RLS) on all tables
  - Add policies for authenticated users to manage rental data
  
  ## Important Notes
  1. All tables use UUID primary keys for better scalability
  2. Rental status defaults to 'active' for new rentals
  3. Foreign key constraints ensure data integrity
  4. RLS policies restrict access to authenticated users only
*/

-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  contact_number text NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create rentals table
CREATE TABLE IF NOT EXISTS rentals (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id uuid NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
  rental_date date NOT NULL DEFAULT CURRENT_DATE,
  return_date date,
  status text NOT NULL DEFAULT 'active',
  notes text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  CONSTRAINT valid_status CHECK (status IN ('active', 'returned', 'overdue'))
);

-- Create rental_items table
CREATE TABLE IF NOT EXISTS rental_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  rental_id uuid NOT NULL REFERENCES rentals(id) ON DELETE CASCADE,
  item_type text NOT NULL,
  quantity integer NOT NULL DEFAULT 1,
  created_at timestamptz DEFAULT now(),
  CONSTRAINT valid_item_type CHECK (item_type IN ('degh', 'chair', 'table', 'tangna', 'plate')),
  CONSTRAINT positive_quantity CHECK (quantity > 0)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_rentals_customer_id ON rentals(customer_id);
CREATE INDEX IF NOT EXISTS idx_rentals_status ON rentals(status);
CREATE INDEX IF NOT EXISTS idx_rental_items_rental_id ON rental_items(rental_id);

-- Enable Row Level Security
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE rentals ENABLE ROW LEVEL SECURITY;
ALTER TABLE rental_items ENABLE ROW LEVEL SECURITY;

-- RLS Policies for customers table
CREATE POLICY "Authenticated users can view all customers"
  ON customers FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Authenticated users can insert customers"
  ON customers FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Authenticated users can update customers"
  ON customers FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Authenticated users can delete customers"
  ON customers FOR DELETE
  TO authenticated
  USING (true);

-- RLS Policies for rentals table
CREATE POLICY "Authenticated users can view all rentals"
  ON rentals FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Authenticated users can insert rentals"
  ON rentals FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Authenticated users can update rentals"
  ON rentals FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Authenticated users can delete rentals"
  ON rentals FOR DELETE
  TO authenticated
  USING (true);

-- RLS Policies for rental_items table
CREATE POLICY "Authenticated users can view all rental items"
  ON rental_items FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Authenticated users can insert rental items"
  ON rental_items FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Authenticated users can update rental items"
  ON rental_items FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Authenticated users can delete rental items"
  ON rental_items FOR DELETE
  TO authenticated
  USING (true);