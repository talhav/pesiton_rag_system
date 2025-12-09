from .rag_response_prompt import (
    MAIN_INSTRUCTION,
    CONTEXT_USAGE_INSTRUCTION,
    AMBIGUITY_HANDLING_INSTRUCTION,
)


class PromptManager:
    def get_llm_response_prompt(self) -> str:
        return (
            MAIN_INSTRUCTION
            + CONTEXT_USAGE_INSTRUCTION
            + AMBIGUITY_HANDLING_INSTRUCTION
        )
