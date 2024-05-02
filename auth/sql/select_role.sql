SELECT
    role
FROM
    internal_users
WHERE
        login = '$login' AND password = '$password'

UNION

SELECT
    role
FROM
    tenant
WHERE
    login = '$login' AND password = '$password'
UNION
SELECT
    role
FROM
    bill_owner
WHERE
    login = '$login' AND password = '$password'