# email_reminders

The main idea is to search for things that need to remember, and send an email.

Below there is a config that search in a DB to send a remember about a payment that is an open state.

```
# boleto_reminder.ini

[db]
host: xxx.yyy.rds.amazonaws.com
name: dbname
user: username
password: password
port: 3306

[mandrill]
api_key: apikey
google_analytics_campaign: xxx@yyy.com
google_analytics_domains:  www.example.com
reply_to: reply@example.com
website: www.example.com

[reminder]
action_name: Payment in open state
reminder_template_name: doc-reminder
summary_template_name: doc-reminder-summary
tables: orders o
fields: transaction_id, name, email, doc, guid as order_id
filter: (o.status = 'waiting_payment') and (datediff(now(),o.dt_created) >= 3) and (o.reminders <= 2) and (o.transaction_id <> 0)
attachment_url: https://www.example.com/preorder/pdfgenerator.php?doc=${doc}
send_resume_to: team@example.com
update: update orders set reminders=reminders+1 where guid='${order_id}'
```
