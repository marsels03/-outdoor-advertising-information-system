SELECT
    login
FROM
    tenant
WHERE
    login = '$login'

UNION
SELECT
    login
FROM
    bill_owner
WHERE
    login = '$login'
UNION
SELECT
    login
FROM
    internal_users
WHERE
    login = '$login'

