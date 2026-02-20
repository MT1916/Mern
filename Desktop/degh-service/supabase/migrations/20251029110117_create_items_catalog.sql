/*
  # Create Items Catalog

  ## Overview
  This migration creates a catalog of all rental items with their names and prices.
  It replaces the hardcoded item types with a flexible database-driven catalog.

  ## New Tables
  
  ### `items`
  Stores the catalog of available rental items
  - `id` (uuid, primary key) - Unique identifier for each item
  - `name` (text, required) - Name of the item (e.g., "Deg 14/16 payali wali")
  - `price` (numeric, required) - Rental price per item
  - `category` (text, optional) - Item category for grouping
  - `is_active` (boolean) - Whether item is currently available for rent
  - `created_at` (timestamptz) - Record creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ## Changes to Existing Tables
  
  ### `rental_items`
  - Drop the old `item_type` column and constraint
  - Add `item_id` foreign key to reference items table
  - Add `price_at_booking` to store the price when booking was made

  ## Security
  - Enable Row Level Security (RLS) on items table
  - Add policies for public access (consistent with other tables)
  
  ## Important Notes
  1. Items can be easily added, updated, or deactivated without code changes
  2. Historical pricing is preserved via `price_at_booking` column
  3. Categories help organize items in the UI
*/

-- Create items table
CREATE TABLE IF NOT EXISTS items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  price numeric NOT NULL DEFAULT 0,
  category text,
  is_active boolean DEFAULT true,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Insert all items with their prices
INSERT INTO items (name, price, category) VALUES
  ('Deg 14/16 payali wali', 320, 'Cooking'),
  ('Deg 12 payali wali', 150, 'Cooking'),
  ('Deg 10 payali wali', 150, 'Cooking'),
  ('Deg 8 payali wali', 150, 'Cooking'),
  ('Deg 6/7 payali wali', 100, 'Cooking'),
  ('Deg 4/5 payali wali', 100, 'Cooking'),
  ('Bhagona 3 payali wali deg', 50, 'Cooking'),
  ('Chulha', 20, 'Cooking'),
  ('Dhakkan', 20, 'Cooking'),
  ('Kafgir', 20, 'Utensils'),
  ('Rakaabi (plate)', 2, 'Serving'),
  ('Jug', 10, 'Serving'),
  ('Steel tokri tanga', 10, 'Storage'),
  ('Chawal ka chhacha', 5, 'Utensils'),
  ('Sini', 3, 'Serving'),
  ('Balti steel', 10, 'Storage'),
  ('Drum', 20, 'Storage'),
  ('Half drum', 20, 'Storage'),
  ('Stand (haath dhone wala)', 150, 'Facilities'),
  ('Kursi, faayada kursi', 5, 'Seating'),
  ('Mat chatai', 30, 'Seating'),
  ('Badi mat', 150, 'Seating'),
  ('Dastar khwan', 10, 'Serving'),
  ('Lamba table', 30, 'Furniture'),
  ('Balli', 20, 'Furniture'),
  ('Site parda', 100, 'Decoration'),
  ('Focus', 200, 'Equipment'),
  ('DJ speaker', 400, 'Equipment'),
  ('Dabbu (bada)', 10, 'Utensils'),
  ('Daalcha korma chammach', 10, 'Utensils'),
  ('Daal ghotna', 50, 'Utensils'),
  ('Donga', 10, 'Utensils'),
  ('Tare (aata gondhne wala)', 200, 'Equipment'),
  ('Gaadi', 30, 'Equipment'),
  ('Kambal', 10, 'Comfort'),
  ('Takiya', 10, 'Comfort'),
  ('Pani jar', 100, 'Storage'),
  ('Gas chulha', 100, 'Cooking'),
  ('Kadhaai jharna', 100, 'Cooking')
ON CONFLICT DO NOTHING;

-- Update rental_items table structure
DO $$
BEGIN
  -- Add item_id column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'rental_items' AND column_name = 'item_id'
  ) THEN
    ALTER TABLE rental_items ADD COLUMN item_id uuid REFERENCES items(id);
  END IF;

  -- Add price_at_booking column if it doesn't exist
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'rental_items' AND column_name = 'price_at_booking'
  ) THEN
    ALTER TABLE rental_items ADD COLUMN price_at_booking numeric DEFAULT 0;
  END IF;
END $$;

-- Enable Row Level Security on items
ALTER TABLE items ENABLE ROW LEVEL SECURITY;

-- RLS Policies for items table
DROP POLICY IF EXISTS "Public can view items" ON items;
CREATE POLICY "Public can view items"
  ON items FOR SELECT
  TO anon, authenticated
  USING (true);

DROP POLICY IF EXISTS "Public can insert items" ON items;
CREATE POLICY "Public can insert items"
  ON items FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

DROP POLICY IF EXISTS "Public can update items" ON items;
CREATE POLICY "Public can update items"
  ON items FOR UPDATE
  TO anon, authenticated
  USING (true)
  WITH CHECK (true);

DROP POLICY IF EXISTS "Public can delete items" ON items;
CREATE POLICY "Public can delete items"
  ON items FOR DELETE
  TO anon, authenticated
  USING (true);

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_items_category ON items(category);
CREATE INDEX IF NOT EXISTS idx_items_is_active ON items(is_active);
CREATE INDEX IF NOT EXISTS idx_rental_items_item_id ON rental_items(item_id);
