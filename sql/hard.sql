SELECT
    surname,
    phone_number
FROM
    tenant
LEFT JOIN
    (SELECT * FROM orders
            WHERE YEAR(date_of_issue) = '$year' AND MONTH(date_of_issue) = '$month') AS ord
ON
    tenant.contract_id= ord.contract_id
WHERE
    ord.contract_id IS NULL;