from hugchat import hugchat
from hugchat.login import Login


class HuggingChat:
    """
    API for accessing HuggingChat
    List of models: https://huggingface.co/chat
    Requires email and password from https://huggingface.co to use
    """

    def __init__(
        self,
        email: str,
        password: str,
        system_prompt: str = "",
        cookie_path_dir: str = "./cookies_snapshot",
        model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1",
    ):
        self.sign = Login(email, password)
        cookies = self.sign.login()
        self.sign.saveCookiesToDir(cookie_path_dir)
        self.chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        # Check actual list of models on https://huggingface.co/chat/settings
        self.models = {
            "mistralai/Mixtral-8x7B-Instruct-v0.1": 0,
            "meta-llama/Llama-2-70b-chat-hf": 1,
            "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO": 2,
            "codellama/CodeLlama-34b-Instruct-hf": 3,
            "mistralai/Mistral-7B-Instruct-v0.2": 4,
            "openchat/openchat-3.5-1210": 5,
        }
        self.system_prompt = system_prompt
        self.model = self.models[model]
        self.chatbot = hugchat.ChatBot(cookies=cookies.get_dict(), system_prompt=self.system_prompt)
        self.chatbot.switch_llm(self.model)
        self.chatbot.new_conversation(switch_to=True, system_prompt=self.system_prompt)

    def prompt(self, prompt: str) -> str:
        return str(self.chatbot.query(prompt))

    def delete_conversations(self) -> None:
        """
        Deletes all conversations in a user's profile
        """
        self.chatbot.delete_all_conversations()

    def switch_model(self, model: str) -> None:
        self.model = self.models[model]
        self.chatbot.switch_llm(self.model)
        self.chatbot.new_conversation(switch_to=True, system_prompt=self.system_prompt)

    def switch_system_prompt(self, system_prompt: str) -> None:
        self.system_prompt = system_prompt
        self.chatbot.new_conversation(switch_to=True, system_prompt=self.system_prompt)

    def get_conversation_info(self):
        """
        Returns information about the current conversation
        """
        return self.chatbot.get_conversation_info()

    def delete_conversation(self, conversation_id: str) -> None:
        """
        Deletes a specific conversation identified by conversation_id
        """
        self.chatbot.delete_conversation(conversation_id)
