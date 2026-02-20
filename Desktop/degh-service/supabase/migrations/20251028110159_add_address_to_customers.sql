/*
  # Add Address Field to Customers

  ## Changes
  - Add `address` column to customers table to track delivery/service location
  
  ## Details
  The address field will store the location where rental items need to be delivered
  or where the catering service will take place.
*/

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'customers' AND column_name = 'address'
  ) THEN
    ALTER TABLE customers ADD COLUMN address text;
  END IF;
END $$;
