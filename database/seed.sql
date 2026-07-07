-- Trajectoire - Donnees de seed (circuits et evenements francais)

-- ============================================================
-- CIRCUITS
-- ============================================================
INSERT INTO circuits (id, name, slug, description, city, postal_code, location, length_km, layout_type, runoff_areas, has_electricity, has_compressor, has_fuel_station, noise_limit_db, has_noise_restriction, allowed_categories, image_url, website_url)
VALUES
  (
    'a0000001-0000-0000-0000-000000000001',
    'Circuit Paul Ricard',
    'paul-ricard',
    'Circuit emblematique du Castellet, celebre pour ses degagements en asphalte bleu et rouge.',
    'Le Castellet',
    '83330',
    ST_SetSRID(ST_MakePoint(5.7869, 43.2508), 4326),
    5.842, 'permanent', 'asphalte',
    true, true, true,
    102, true,
    '{auto,moto}',
    NULL,
    'https://www.circuitpaulricard.com'
  ),
  (
    'a0000001-0000-0000-0000-000000000002',
    'Circuit de Nevers Magny-Cours',
    'magny-cours',
    'Circuit technique accueillant le GP de France F1. Tracé exigeant avec courbes rapides.',
    'Magny-Cours',
    '58470',
    ST_SetSRID(ST_MakePoint(3.1400, 46.8700), 4326),
    4.411, 'permanent', 'asphalte',
    true, true, true,
    98, true,
    '{auto}',
    NULL,
    'https://www.magny-cours.com'
  ),
  (
    'a0000001-0000-0000-0000-000000000003',
    'Circuit de Spa-Francorchamps',
    'spa-francorchamps',
    'Plus beau circuit du monde selon de nombreux pilotes. Secteur de l''Eau Rouge mythique.',
    'Spa',
    '4900',
    ST_SetSRID(ST_MakePoint(5.9720, 50.4370), 4326),
    7.004, 'permanent', 'asphalte',
    true, true, true,
    105, true,
    '{auto,moto}',
    NULL,
    'https://www.spa-francorchamps.be'
  ),
  (
    'a0000001-0000-0000-0000-000000000004',
    'Circuit de Bresse',
    'bresse',
    'Circuit technique avec degagements en herbe. Populaire pour les trackdays moto.',
    'Frontenaud',
    '71580',
    ST_SetSRID(ST_MakePoint(5.3470, 46.6020), 4326),
    3.050, 'permanent', 'graviers',
    true, false, false,
    95, true,
    '{auto,moto}',
    NULL,
    'https://www.circuitdebresse.com'
  ),
  (
    'a0000001-0000-0000-0000-000000000005',
    'Circuit de l''Anneau du Rhin',
    'anneau-du-rhin',
    'Circuit situe sur une ile du Rhin, tracé roulant et securise.',
    'Biltzheim',
    '68127',
    ST_SetSRID(ST_MakePoint(7.4820, 47.9600), 4326),
    3.350, 'permanent', 'asphalte',
    true, true, false,
    98, true,
    '{auto,moto}',
    NULL,
    'https://www.anneau-du-rhin.com'
  ),
  (
    'a0000001-0000-0000-0000-000000000006',
    'Circuit du Mas du Clos',
    'mas-du-clos',
    'Circuit dans la campagne aveyronnaise. Ambiance conviviale et tracé technique.',
    'Saint-Geniez-d-Olt',
    '12130',
    ST_SetSRID(ST_MakePoint(2.9680, 44.4600), 4326),
    2.150, 'permanent', 'mixte',
    true, true, false,
    100, true,
    '{moto}',
    NULL,
    'https://www.masduclos.com'
  ),
  (
    'a0000001-0000-0000-0000-000000000007',
    'Circuit du Val de Vienne',
    'val-de-vienne',
    'Circuit moderne avec de grandes zones de degagement. Ideal pour debuter.',
    'Le Vigeant',
    '86150',
    ST_SetSRID(ST_MakePoint(0.6390, 46.2220), 4326),
    3.757, 'permanent', 'asphalte',
    true, true, true,
    102, true,
    '{auto,moto}',
    NULL,
    'https://www.valdevienne.com'
  ),
  (
    'a0000001-0000-0000-0000-000000000008',
    'Circuit Carole',
    'carole',
    'Circuit teaching situe en Seine-Saint-Denis. Tres populaire pour les journées pistes.',
    'Tremblay-en-France',
    '93290',
    ST_SetSRID(ST_MakePoint(2.5690, 48.9560), 4326),
    1.350, 'permanent', 'graviers',
    true, false, false,
    95, true,
    '{moto}',
    NULL,
    'https://www.circuitcarole.com'
  ),
  (
    'a0000001-0000-0000-0000-000000000009',
    'Circuit de Nogaro (Paul Armagnac)',
    'nogaro',
    'Circuit historique du Gers. Tracé rapide avec de belles courbes.',
    'Nogaro',
    '32110',
    ST_SetSRID(ST_MakePoint(-0.0340, 43.7580), 4326),
    3.636, 'permanent', 'mixte',
    true, true, true,
    102, true,
    '{auto,moto}',
    NULL,
    'https://www.circuit-nogaro.com'
  ),
  (
    'a0000001-0000-0000-0000-00000000000a',
    'Pole Mecanique d''Alès',
    'ales',
    'Complexe motor sport complet avec circuit automobile et tout-terrain.',
    'Saint-Martin-de-Valgalgues',
    '30520',
    ST_SetSRID(ST_MakePoint(4.0810, 44.1190), 4326),
    3.250, 'permanent', 'mixte',
    true, true, true,
    100, false,
    '{auto,moto}',
    NULL,
    'https://www.pole-mecanique-ales.fr'
  ),
  (
    'a0000001-0000-0000-0000-00000000000b',
    'Circuit de Croix-en-Ternois',
    'croix-en-ternois',
    'Circuit familial du Pas-de-Calais avec plusieurs configurations.',
    'Croix-en-Ternois',
    '62130',
    ST_SetSRID(ST_MakePoint(2.4880, 50.3910), 4326),
    1.900, 'permanent', 'graviers',
    true, true, true,
    96, true,
    '{moto}',
    NULL,
    'https://www.circuitdecroix.fr'
  ),
  (
    'a0000001-0000-0000-0000-00000000000c',
    'Circuit de Charade',
    'charade',
    'Circuit de montagne pres de Clermont-Ferrand. Tracé technique en elevation.',
    'Saint-Genes-Champanelle',
    '63830',
    ST_SetSRID(ST_MakePoint(3.0330, 45.7330), 4326),
    3.975, 'permanent', 'asphalte',
    true, false, false,
    102, true,
    '{auto}',
    NULL,
    'https://www.circuit-charade.com'
  )
ON CONFLICT (slug) DO NOTHING;

-- ============================================================
-- EVENEMENTS (Trackdays)
-- ============================================================
INSERT INTO events (circuit_id, organizer_name, organizer_url, start_date, end_date, has_debutant, has_intermediaire, has_confirme, price_base, price_license, booking_url, spots_available, is_active)
SELECT c.id, 'M2R Trackdays', 'https://m2r-trackdays.fr', '2026-08-15', '2026-08-15', true, true, true, 299.00, 259.00, 'https://m2r-trackdays.fr/booking/paul-ricard-aout', 25, true
FROM circuits c WHERE c.slug = 'paul-ricard';

INSERT INTO events (circuit_id, organizer_name, organizer_url, start_date, end_date, has_debutant, has_intermediaire, has_confirme, price_base, price_license, booking_url, spots_available, is_active)
SELECT c.id, 'RS Trackdays', 'https://rs-trackdays.fr', '2026-09-10', '2026-09-11', false, true, true, 349.00, 299.00, 'https://rs-trackdays.fr/booking/paul-ricard-sept', 15, true
FROM circuits c WHERE c.slug = 'paul-ricard';

INSERT INTO events (circuit_id, organizer_name, organizer_url, start_date, end_date, has_debutant, has_intermediaire, has_confirme, price_base, price_license, booking_url, spots_available, is_active)
SELECT c.id, 'MotoE Sport', 'https://motoe-sport.fr', '2026-07-20', '2026-07-21', true, true, false, 199.00, 179.00, 'https://motoe-sport.fr/booking/magny-cours-juillet', 30, true
FROM circuits c WHERE c.slug = 'magny-cours';

INSERT INTO events (circuit_id, organizer_name, organizer_url, start_date, end_date, has_debutant, has_intermediaire, has_confirme, price_base, price_license, booking_url, spots_available, is_active)
SELECT c.id, 'Trackday France', 'https://trackday-france.fr', '2026-08-28', '2026-08-29', true, true, true, 259.00, 229.00, 'https://trackday-france.fr/booking/spa-aout', 20, true
FROM circuits c WHERE c.slug = 'spa-francorchamps';

INSERT INTO events (circuit_id, organizer_name, organizer_url, start_date, end_date, has_debutant, has_intermediaire, has_confirme, price_base, price_license, booking_url, spots_available, is_active)
SELECT c.id, 'Moto Passion Track', 'https://motopassion-track.fr', '2026-09-05', '2026-09-05', true, true, false, 129.00, 99.00, 'https://motopassion-track.fr/booking/bresse-sept', 5, true
FROM circuits c WHERE c.slug = 'bresse';

INSERT INTO events (circuit_id, organizer_name, organizer_url, start_date, end_date, has_debutant, has_intermediaire, has_confirme, price_base, price_license, booking_url, spots_available, is_active)
SELECT c.id, 'RS Trackdays', 'https://rs-trackdays.fr', '2026-08-08', '2026-08-08', false, true, true, 189.00, 159.00, 'https://rs-trackdays.fr/booking/anneau-rhin-aout', 18, true
FROM circuits c WHERE c.slug = 'anneau-du-rhin';

INSERT INTO events (circuit_id, organizer_name, organizer_url, start_date, end_date, has_debutant, has_intermediaire, has_confirme, price_base, price_license, booking_url, spots_available, is_active)
SELECT c.id, 'M2R Trackdays', 'https://m2r-trackdays.fr', '2026-07-26', '2026-07-26', true, true, true, 99.00, 79.00, 'https://m2r-trackdays.fr/booking/val-de-vienne-juillet', 12, true
FROM circuits c WHERE c.slug = 'val-de-vienne';

INSERT INTO events (circuit_id, organizer_name, organizer_url, start_date, end_date, has_debutant, has_intermediaire, has_confirme, price_base, price_license, booking_url, spots_available, is_active)
SELECT c.id, 'Bike Track Days', 'https://biketrackdays.fr', '2026-08-16', '2026-08-16', true, false, false, 89.00, 69.00, 'https://biketrackdays.fr/booking/carole-aout', 8, true
FROM circuits c WHERE c.slug = 'carole';

INSERT INTO events (circuit_id, organizer_name, organizer_url, start_date, end_date, has_debutant, has_intermediaire, has_confirme, price_base, price_license, booking_url, spots_available, is_active)
SELECT c.id, 'Trackday France', 'https://trackday-france.fr', '2026-09-19', '2026-09-20', true, true, true, 199.00, 169.00, 'https://trackday-france.fr/booking/ales-sept', 22, true
FROM circuits c WHERE c.slug = 'ales';

INSERT INTO events (circuit_id, organizer_name, organizer_url, start_date, end_date, has_debutant, has_intermediaire, has_confirme, price_base, price_license, booking_url, spots_available, is_active)
SELECT c.id, 'MotoE Sport', 'https://motoe-sport.fr', '2026-07-13', '2026-07-13', true, true, false, 119.00, 99.00, 'https://motoe-sport.fr/booking/nogaro-juillet', 3, true
FROM circuits c WHERE c.slug = 'nogaro';

INSERT INTO events (circuit_id, organizer_name, organizer_url, start_date, end_date, has_debutant, has_intermediaire, has_confirme, price_base, price_license, booking_url, spots_available, is_active)
SELECT c.id, 'M2R Trackdays', 'https://m2r-trackdays.fr', '2026-10-03', '2026-10-04', false, true, true, 279.00, 239.00, 'https://m2r-trackdays.fr/booking/spa-octobre', 10, true
FROM circuits c WHERE c.slug = 'spa-francorchamps';

INSERT INTO events (circuit_id, organizer_name, organizer_url, start_date, end_date, has_debutant, has_intermediaire, has_confirme, price_base, price_license, booking_url, spots_available, is_active)
SELECT c.id, 'Moto Passion Track', 'https://motopassion-track.fr', '2026-09-12', '2026-09-12', true, true, true, 109.00, 89.00, 'https://motopassion-track.fr/booking/mas-du-clos-sept', 14, true
FROM circuits c WHERE c.slug = 'mas-du-clos';
