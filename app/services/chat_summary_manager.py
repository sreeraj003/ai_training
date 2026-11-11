class SummaryManager:
    def __init__(self):
        self.summary = {
            "user_facts": {},
            "preferences": {},
            "decisions": {},
            "ongoing_tasks": {},
            "unresolved_tasks": {},
            "learning_journey": {}
        }

    def add_information(self, category: str, key: str, info: object):
        if category not in self.summary:
            raise ValueError(f"Invalid summary category: {category}")

        if key in self.summary[category]:
            raise ValueError(f"Information with key '{key}' already exists.")

        self.summary[category][key] = info

    def update_information(self, category: str, key: str, info: object):
        if category not in self.summary:
            raise ValueError(f"Invalid summary category: {category}")

        self.summary[category][key] = info

    def get_summary(self):
        return {
            category: information.copy()
            for category, information in self.summary.items()
        }