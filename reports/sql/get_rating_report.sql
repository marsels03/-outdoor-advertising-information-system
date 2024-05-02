select
    *
from
    rating_report_strs
join
        rating_reports
ON
     rating_report_strs.rrs_report = rating_reports.rating_reports_id
where
    rating_report_year='$year' and rating_report_month= '$month'