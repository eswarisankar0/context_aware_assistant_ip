from .intent import IntentDetector
from .llm_engine import LLMEngine
from .context_builder import ContextBuilder
from .action_router import ActionRouter

detector = IntentDetector()
llm = LLMEngine()
context = ContextBuilder()
router = ActionRouter()

# ⭐ simple conversation memory
chat_history = []


def run_assistant(msg: str):
    intent = detector.detect_intent(msg)

    # 🔥 If it's a reminder → handle in backend FIRST
    if intent == "set_reminder":
        action = router.handle_action(intent, msg)

        if action:
             reply = action["reply"]
        else:
             reply = "Sorry, I couldn't process that reminder."

    else:
        ctx = context.get_context(msg, intent)

        history_text = "\n".join(chat_history[-4:])
        full_context = f"{history_text}\n{ctx}" if ctx else history_text

        reply = llm.generate_response(msg, intent, full_context)
        action = None

    # Store conversation
    chat_history.append(f"User: {msg}")
    chat_history.append(f"Assistant: {reply}")

    return {
        "reply": reply,
        "system": action
    }

    print("Detected intent:", intent)