class ContextManager:

    def __init__(self,token_manager,context_limit: int,output_reserve: int,safety_margin: int):
        self.token_manager = token_manager
        self.context_limit = context_limit
        self.output_reserve = output_reserve
        self.safety_margin = safety_margin

    def get_input_budget(self):
        return (
            self.context_limit - self.output_reserve - self.safety_margin
        )

    def fits_context_window(self, messages: list) -> bool:

        total_tokens = self.token_manager.count_messages_tokens(messages)
        return total_tokens <= self.get_input_budget()
    
    def trim_msg(self,message:list)->list:
        system_msg = message[0]
        remaining_msgs = message[1:]
        while not self.fits_context_window([system_msg]+remaining_msgs):
            if(len(remaining_msgs)<=1):
                raise ValueError("mesage length exceeds context window")
            del remaining_msgs[:2]
        return [system_msg]+remaining_msgs