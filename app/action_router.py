from .time_parser import parse_time

class ActionRouter:
    def __init__(self):
        self.reminders = []

    def handle_action(self, intent, msg):

        if intent == "set_reminder":
            time = parse_time(msg)

            reminder = {
                "task": msg,
                "time": str(time)
            }

            self.reminders.append(reminder)

            return {
                "reply": f"Reminder set for {time}",
                "task": msg,
                "time": str(time)
            }

        return None