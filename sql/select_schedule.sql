SELECT
    bill_id, start_of_lease,end_of_lease, surname, phone_number
FROM
    schedule
JOIN billboard.tenant t on schedule.contract_id = t.contract_id