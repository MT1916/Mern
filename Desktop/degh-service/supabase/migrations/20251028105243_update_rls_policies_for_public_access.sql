/*
  # Update RLS Policies for Public Access

  ## Changes
  This migration updates the Row Level Security policies to allow public access
  since authentication is not yet implemented in the application.

  ## Security Note
  These policies allow anyone with the anon key to access the data.
  This is suitable for development and single-user applications.
  For production multi-user scenarios, implement authentication first.
*/

-- Drop existing policies
DROP POLICY IF EXISTS "Authenticated users can view all customers" ON customers;
DROP POLICY IF EXISTS "Authenticated users can insert customers" ON customers;
DROP POLICY IF EXISTS "Authenticated users can update customers" ON customers;
DROP POLICY IF EXISTS "Authenticated users can delete customers" ON customers;

DROP POLICY IF EXISTS "Authenticated users can view all rentals" ON rentals;
DROP POLICY IF EXISTS "Authenticated users can insert rentals" ON rentals;
DROP POLICY IF EXISTS "Authenticated users can update rentals" ON rentals;
DROP POLICY IF EXISTS "Authenticated users can delete rentals" ON rentals;

DROP POLICY IF EXISTS "Authenticated users can view all rental items" ON rental_items;
DROP POLICY IF EXISTS "Authenticated users can insert rental items" ON rental_items;
DROP POLICY IF EXISTS "Authenticated users can update rental items" ON rental_items;
DROP POLICY IF EXISTS "Authenticated users can delete rental items" ON rental_items;

-- Create new policies allowing public access via anon role

-- Customers policies
CREATE POLICY "Public can view customers"
  ON customers FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Public can insert customers"
  ON customers FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "Public can update customers"
  ON customers FOR UPDATE
  TO anon, authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Public can delete customers"
  ON customers FOR DELETE
  TO anon, authenticated
  USING (true);

-- Rentals policies
CREATE POLICY "Public can view rentals"
  ON rentals FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Public can insert rentals"
  ON rentals FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "Public can update rentals"
  ON rentals FOR UPDATE
  TO anon, authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Public can delete rentals"
  ON rentals FOR DELETE
  TO anon, authenticated
  USING (true);

-- Rental items policies
CREATE POLICY "Public can view rental items"
  ON rental_items FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Public can insert rental items"
  ON rental_items FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "Public can update rental items"
  ON rental_items FOR UPDATE
  TO anon, authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Public can delete rental items"
  ON rental_items FOR DELETE
  TO anon, authenticated
  USING (true);
