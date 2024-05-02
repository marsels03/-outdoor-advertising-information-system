SELECT DISTINCT
    b.bill_id, b.price, b.size, b.install_address, b.quality
FROM
    billboard b
LEFT JOIN
    billboard.schedule s ON b.bill_id = s.bill_id
WHERE
    (s.bill_id IS NULL) OR
    (
        (s.start_of_lease > '$end' OR s.end_of_lease < '$start')
        OR
        (s.bill_id IS NULL)
    );
