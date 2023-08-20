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
   

CREATE VIEW Informacion_tablas_view AS
SELECT
    t.table_name AS Tabla,
    c.column_name AS Columna,
    c.data_type AS Tipo,
    IFNULL(kcu.constraint_name, 'No') AS Es_Index,
    kcu.ordinal_position AS Orden_Index,
    GROUP_CONCAT(DISTINCT kcu2.referenced_table_name) AS Tablas_Vinculadas
FROM
    information_schema.tables t
    INNER JOIN information_schema.columns c ON t.table_name = c.table_name
    LEFT JOIN information_schema.key_column_usage kcu ON t.table_name = kcu.table_name AND c.column_name = kcu.column_name
    LEFT JOIN information_schema.key_column_usage kcu2 ON kcu.referenced_table_name = kcu2.table_name
WHERE
    t.table_schema = 'qxm_dump'
GROUP BY
    t.table_name, c.column_name, c.data_type, Es_Index, Orden_Index;
  
	
	
