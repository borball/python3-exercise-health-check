## Requirement

Write a Python script that reads JSON encoded strings from stdin and alerts on service health failure and/or high error rate. Example input:

	{
	  "service_id": "myservice",
	  "status": {
	    "healthy": true,
	    "message": "Everything is OK"
	  },
	  "events": {
	    "ok": 23,
	    "error": 2
	  }
	}

The "events" dict contains the count of "ok" events and "error" events that have happened since the last report from this particular service. 

If a service is unhealthy, send an email via smtplib, boto3(AWS SES or SNS), or another python library of your choice to alerts@example.com. If you use boto3, you may assume that you have an initialized, authorized client object. 

When we reach 1000 events, sum up events for each service. If errors are more than 10% of the event total for any service, send a TCP message to 127.0.0.1:5005 containing the service_id and error percentage.

**Bonus:** Keep a rolling event tally and alert on statistics from the last 1000 events.

**Boto 3 SES documentation**: [link](http://boto3.readthedocs.io/en/latest/reference/services/ses.html#SES.Client.send_email)



## Implementation

Major requirement have been implemented except:

- Send email with any email lib
- Send TCP message

<font color = 'red'>Instead a log printed in the console to simulate the email or TCP sending. </font>
 

## Usage

On any laptop or server where **python3** installed, run the health check script with command below:

    python health_check.py
    
Input a Json string to simulate the health check report for a particular service, for example:

    {"service_id": "service1", "status": {"healthy": true, "message": "Everything is OK"}, "events": {"ok": 24, "error": 1}}
     
Either continue to input more report or exit the application by typing 'quit'.

## Configuration

	EVENT_ROLLING_INTERVAL： 1000
	MAX_ALLOWED_ERROR_RATE:  0.10

