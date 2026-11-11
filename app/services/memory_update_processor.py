

class MemoryUpdateProcessor:

    def __init__(self, summary_manager):
        self.summary_manager = summary_manager

    def apply_updates(self, extraction_response):
        for update in extraction_response.updates:
            category = update.category
            key = update.key
            value = update.value

            if category not in self.summary_manager.summary:
                raise ValueError(f"Invalid summary category: {category}")

            if key in self.summary_manager.summary[category]:
                self.summary_manager.update_information(category, key, value)
            else:
                self.summary_manager.add_information(category, key, value)
        return self.summary_manager.get_summary()