SELECT
    billboard.bill_id, price, size, install_address, quality
FROM
    billboard
LEFT JOIN
    billboard.schedule s ON billboard.bill_id = s.bill_id
WHERE
        ((start_of_lease < '$start' AND end_of_lease < '$start')
        OR
        (start_of_lease > '$end' AND end_of_lease > '$end'))
        OR s.bill_id IS NULL
