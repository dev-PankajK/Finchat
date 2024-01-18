-- Prisma requires DB creation privileges to create a shadow database (https://pris.ly/d/migrate-shadow)
-- This is not available to our user by default, so we must manually add this

-- Create the user
CREATE USER IF NOT EXISTS 'fin_platform'@'%' IDENTIFIED BY 'fin_platform';

-- Grant the necessary permissions
GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT ON *.* TO 'fin_platform'@'%';

-- Apply the changes
FLUSH PRIVILEGES;
