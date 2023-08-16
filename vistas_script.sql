-- USE qxm_dump;

DROP VIEW IF EXISTS profesionals_data;
CREATE VIEW profesionals_data  AS
SELECT
    prof.id,
    prof.bill,
    prof.created_at,
    cat.title AS category_title,
    poll.insurance,
    poll.bank_account,
    addr.city
FROM
    professionals AS prof
JOIN
    professional_categories AS prof_cat ON prof.id = prof_cat.professional_id
JOIN
    categories AS cat ON prof_cat.category_id = cat.id
JOIN
    professional_polls AS poll ON prof.id = poll.professional_id
JOIN
    users AS usr ON prof.user_id = usr.id
JOIN
    user_addresses AS addr ON usr.id = addr.user_id;

DROP VIEW IF EXISTS presupuestos_contratados;
CREATE VIEW presupuestos_contratados AS
SELECT
    projects.id,
    MAX(contracts.price) AS price,
    MAX(contracts.created_at) AS created_at,
    MAX(categories.title) AS title,
    MAX(prof.id) AS professional_id,
    MAX(prof.qualification) AS qualification,
    MAX(prof.bill) AS bill,
    MAX(poll.insurance) AS insurance,
    MAX(poll.bank_account) AS bank_account,
    MAX(addr.city) AS city
FROM
    contracts
JOIN
    projects ON projects.id = contracts.project_id
JOIN
    professionals AS prof ON prof.id = contracts.professional_id
JOIN
    categories ON categories.id = projects.category_id
JOIN
    professional_polls AS poll ON prof.id = poll.professional_id
JOIN
    users AS usr ON projects.user_id = usr.id
JOIN
    user_addresses AS addr ON usr.id = addr.user_id
GROUP BY
    projects.id;

DROP VIEW IF EXISTS projects_view;
CREATE VIEW projects_view AS
SELECT
    p.id AS project_id,
    c.title AS category_title,
    CASE WHEN c2.project_id IS NULL THEN 'No' ELSE 'Si' END AS has_contract
FROM projects p
JOIN categories c ON p.category_id = c.id
LEFT JOIN contracts c2 ON p.id = c2.project_id;
   
   
  
	
	
