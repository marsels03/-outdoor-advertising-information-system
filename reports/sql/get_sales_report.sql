select
    *
from
    sales_report_strs
join
        sales_reports
ON
    sales_report_strs.srs_report = sales_reports.sales_reports_id
where
    sales_report_year='$year' and sales_reports_month='$month'