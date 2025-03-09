-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create country table
CREATE TABLE country (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    code CHAR(2) NOT NULL UNIQUE
);

-- Create locations table
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    population INT CHECK (population >= 0),
    elevation FLOAT,
    geom GEOMETRY(Point, 4326),
    country_id INT REFERENCES country(id) ON DELETE CASCADE
);

-- Insert sample countries
INSERT INTO country (name, code) VALUES
    ('United States', 'US'),
    ('United Kingdom', 'GB'),
    ('France', 'FR');

-- Insert sample locations
INSERT INTO locations (name, population, elevation, geom, country_id) VALUES 
    ('New York', 8419600, 10, ST_GeomFromText('POINT(-74.006 40.7128)', 4326), 
        (SELECT id FROM country WHERE code = 'US')),
    ('San Francisco', 873965, 16, ST_GeomFromText('POINT(-122.4194 37.7749)', 4326), 
        (SELECT id FROM country WHERE code = 'US')),
    ('London', 8982000, 11, ST_GeomFromText('POINT(-0.1276 51.5074)', 4326), 
        (SELECT id FROM country WHERE code = 'GB')),
    ('Paris', 2161000, 35, ST_GeomFromText('POINT(2.3522 48.8566)', 4326), 
        (SELECT id FROM country WHERE code = 'FR'));
