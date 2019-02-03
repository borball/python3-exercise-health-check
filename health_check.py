import datetime
import json
import config


class Status:

    def __init__(self, healthy, message):
        self.healthy = healthy
        self.message = message


class Events:

    def __init__(self, ok, error):
        self.ok = ok
        self.error = error

    def total(self):
        return self.ok + self.error

    def error_rate(self):
        return self.error / self.total()

    def add_on(self, another_event):
        self.ok += another_event.ok
        self.error += another_event.error


class HealthCheck:

    def __init__(self, service_id, status, events):
        self.service_id = service_id
        self.status = status
        self.events = events

    def is_healthy(self):
        return self.status.healthy

    def total_events(self):
        return self.events.total()


def dct_to_health_check_hook(dct):
    if "healthy" in dct and "message" in dct:
        return Status(dct["healthy"], dct["message"])

    if "ok" in dct and "error" in dct:
        return Events(dct["ok"], dct["error"])

    if "service_id" in dct and "status" in dct and "events" in dct:
        return HealthCheck(dct["service_id"], dct["status"], dct["events"])


def persist_events(all_service_event_reports):
    print("Total events reach to {}, start persistence of service event reports.".format(config.EVENT_ROLLING_INTERVAL))
    time = datetime.datetime.now().strftime("%Y%m%d-%H%M00")
    title = "SERVICE_ID,TOTAL,OK,ERROR,ERROR_RATE\n"
    filename = "service-events-" + time + ".csv"
    with open(filename, 'w', newline='') as f:
        f.write(title)
        for service_id, service_events in all_service_event_reports.items():
            f.write(service_id + "," + str(service_events.total()) + "," + str(service_events.ok) + "," +
                    str(service_events.error) + "," + str(service_events.error_rate()) + "\n")


# send tcp trap
def send_tcp(service_id, service_events):
    tcp_payload = "TCP report: Service '{}' error rate {} is bigger than {}."
    print(tcp_payload.format(service_id, service_events.error_rate(), config.MAX_ALLOWED_ERROR_RATE))
    # TODO: use tcp lib to open a TCP socket send the message


# send email alert if service is not healthy
def send_alert(service_health_check):
    email = "Service '{}' is not healthy, error message: '{}'"
    print(email.format(service_health_check.service_id, service_health_check.status.message))
    # TODO: use mail lib to send the email based on a pre-defined template


def main():
    total_events = 0
    service_events_store = {}

    while True:
        message = input(config.PROMPT)
        if "quit" == message:
            exit(0)

        else:
            try:
                health_check = json.loads(message, object_hook=dct_to_health_check_hook)
            except ValueError:
                print("[WARN]: The input is not a valid health check report or quit command.")
                continue

            if not health_check.is_healthy():
                send_alert(health_check)

            if health_check.service_id not in service_events_store.keys():
                service_events_store[health_check.service_id] = health_check.events
            else:
                service_events = service_events_store[health_check.service_id]
                service_events.add_on(health_check.events)
                service_events_store[health_check.service_id] = service_events

            total_events += health_check.total_events()
            if total_events >= config.EVENT_ROLLING_INTERVAL:
                for service_id, service_events in service_events_store.items():
                    if service_events.error_rate() >= config.MAX_ALLOWED_ERROR_RATE:
                        send_tcp(service_id, service_events)

                # persist the last 1000 service event
                persist_events(service_events_store)

                # reset to generate rolling report
                total_events = 0
                service_events_store = {}

            else:
                continue


main()
