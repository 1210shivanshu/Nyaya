# client.py — Final cleaned & complete version
import streamlit as st
import socket
import json
import threading
import time
from datetime import datetime
from nyayaFunction import modelRun
from langTranslator import MinimalIndianTranslator

# ============================================================================
# Configuration (change these if needed)
# ============================================================================
CHAT_SERVER_HOST = "127.0.0.1"   # change if your chat server runs elsewhere
CHAT_SERVER_PORT = 8051

# Maximum message history to keep in session (for performance)
MAX_HISTORY_ITEMS = 200
TRIM_TO_LAST = 100

# ============================================================================
# Chat client (for "Inbox" feature) — simple TCP client
# ============================================================================
class ChatClient:
    def __init__(self, host=CHAT_SERVER_HOST, port=CHAT_SERVER_PORT):
        self.host = host
        self.port = port
        self.client_socket = None
        self.connected = False
        self.messages = []  # list of dicts: {"sender": ..., "message": ..., "timestamp": ...}

    def connect(self, username):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.client_socket.send(json.dumps({"username": username}).encode("utf-8"))
            self.connected = True

            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()
            return True
        except Exception as e:
            st.sidebar.error(f"Connection failed: {e}")
            return False

    def send_message(self, message):
        if not self.connected:
            return False
        try:
            self.client_socket.send(json.dumps({"message": message}).encode("utf-8"))
            return True
        except Exception as e:
            st.sidebar.error(f"Send failed: {e}")
            self.connected = False
            return False

    def receive_messages(self):
        while self.connected:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    self.connected = False
                    break
                # Try decode and append
                try:
                    payload = data.decode("utf-8")
                    # The server may send multiple JSON objects concatenated; try parsing robustly
                    parts = payload.strip().split("\n")
                    for part in parts:
                        if not part:
                            continue
                        try:
                            msg = json.loads(part)
                            self.messages.append(msg)
                        except json.JSONDecodeError:
                            # attempt to salvage partial messages
                            continue
                except Exception:
                    continue
                time.sleep(0.1)
            except Exception:
                self.connected = False
                break


# ============================================================================
# Translation & formatting helpers
# ============================================================================
def format_legal_text(response, translator=None, target_lang="english"):
    """
    Convert structured response (dict) into a human readable markdown string.
    If translator is provided and target_lang != 'english', translate final text.
    """
    if isinstance(response, dict) and response.get("status") == "success":
        title = response.get("title", "Legal Information")
        section = response.get("section_number", "N/A")
        subsection = response.get("subsection_number", "N/A")
        explanation = response.get("explanation", response.get("original_explanation", "No explanation available."))
        punishment = response.get("punishment", "No punishment specified.")
        cross_refs = response.get("cross_references", "None specified.")

        text = f"""**{title}**

**Section:** {section}  |  **Subsection:** {subsection}

**Detailed Explanation:**  
{explanation}

**Punishment:**  
{punishment}

**Cross References:**  
{cross_refs}

---  
*Source: Bharatiya Nyaya Sanhita (BNS)*
"""
    elif isinstance(response, dict) and response.get("status") == "no_match":
        text = f"{response.get('message','No relevant legal information found.')}\n\n💡 {response.get('suggestion','Try rephrasing your query or use more specific legal terms.')}"
    elif isinstance(response, dict) and response.get("status") == "error":
        text = f"Error: {response.get('message', 'Unknown error')}"
    else:
        text = str(response)

    # Translate final formatted text if requested
    if translator and target_lang and target_lang.lower() != "english":
        try:
            return translator.translate(text, "english", target_lang)
        except Exception:
            # fallback to original English formatted text on translation error
            return text
    return text


def safe_translate(translator, text, src_lang, tgt_lang):
    """
    Wrapper for translator.translate with safe fallback.
    Translator is expected to expose translate(text, src, tgt).
    """
    try:
        if not text:
            return text
        if src_lang == tgt_lang:
            return text
        return translator.translate(text, src_lang, tgt_lang)
    except Exception:
        return text


def check_query_length(q, max_len=500):
    if len(q) > max_len:
        return False, f"Your query exceeds the maximum allowed length of {max_len} characters. Please shorten your query."
    return True, q


# ============================================================================
# Streamlit UI bootstrapping
# ============================================================================
st.set_page_config(page_title="Nyaya — AI Legal Assistant", layout="wide")

st.title("Nyaya — AI Legal Assistant")
st.write("---")

# initialize session state variables
if "client" not in st.session_state:
    st.session_state.client = ChatClient()
if "username" not in st.session_state:
    st.session_state.username = ""
if "connected" not in st.session_state:
    st.session_state.connected = False
if "translator" not in st.session_state:
    translator = MinimalIndianTranslator()
    translator.set_chunk_size(300)
    st.session_state.translator = translator
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "english"
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm **Nyaya**, your AI legal assistant. How can I help you today?", "timestamp": datetime.now().isoformat()}
    ]
if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False
if "max_query_length" not in st.session_state:
    st.session_state.max_query_length = 500   


# supported languages map (key: code used in translator calls; value: label)
languages = {
    "english": "English",
    "hindi": "Hindi",
    "tamil": "Tamil",
    "telugu": "Telugu",
    "bengali": "Bengali",
    "gujarati": "Gujarati",
    "kannada": "Kannada",
    "malayalam": "Malayalam",
    "marathi": "Marathi",
    "punjabi": "Punjabi",
    "urdu": "Urdu"
}

# ============================================================================
# Sidebar: Inbox & Document Intelligence
# ============================================================================
with st.sidebar:
    st.header("Tools")
    menu = st.selectbox("Choose a section:", ["Inbox", "Document Intelligence"])

    # Inbox UI
    if menu == "Inbox":
        st.session_state.auto_refresh = True

        if not st.session_state.connected:
            st.subheader("Login to Chat Server")
            with st.form("login_form"):
                username = st.text_input("Enter your username", key="login_username")
                submitted = st.form_submit_button("Connect")
                if submitted and username:
                    ok = st.session_state.client.connect(username)
                    if ok:
                        st.session_state.username = username
                        st.session_state.connected = True
                        st.success("Connected to chat server")
                        st.experimental_rerun()
                    else:
                        st.error("Connection failed. Check server or host/port settings.")

        else:
            st.subheader("Chat Room")
            st.success(f"Connected as: {st.session_state.username}")

            st.write("**Recent messages from server:**")
            for msg in st.session_state.client.messages[-10:]:
                sender = msg.get("sender", "Server")
                content = msg.get("message", "")
                t = msg.get("timestamp", datetime.now().strftime("%H:%M:%S"))
                if sender == "Server":
                    st.info(f"[{t}] {content}")
                elif sender == st.session_state.username:
                    st.success(f"[{t}] You: {content}")
                else:
                    st.warning(f"[{t}] {sender}: {content}")

            with st.form("send_inbox"):
                out_msg = st.text_input("Type a message to server", key="inbox_msg")
                send_ok = st.form_submit_button("Send")
                if send_ok and out_msg:
                    if st.session_state.client.send_message(out_msg):
                        st.success("Sent to server")
                    else:
                        st.error("Failed to send")

    # Document intelligence / Upload
    else:
        st.subheader("Document Intelligence")
        uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
        if uploaded_files:
            st.success(f"{len(uploaded_files)} file(s) uploaded.")
            extract_text = st.checkbox("Extract text", value=True)
            legal_analysis = st.checkbox("Legal analysis", value=True)
            if st.button("Analyze Documents"):
                with st.spinner("Processing documents..."):
                    time.sleep(1)
                    st.success("Documents processed (placeholder).")

# ============================================================================
# Main chat area
# ============================================================================

# language selector in main area
selected_lang = st.selectbox("Select your preferred language:", options=list(languages.keys()), format_func=lambda x: languages[x], index=list(languages.keys()).index(st.session_state.selected_language))
st.session_state.selected_language = selected_lang

# translate welcome message into selected language (only once)
if selected_lang != "english" and len(st.session_state.messages) == 1:
    try:
        st.session_state.messages[0]["content"] = safe_translate(st.session_state.translator, st.session_state.messages[0]["content"], "english", selected_lang)
    except Exception:
        pass

messages = st.session_state.messages

for i, msg in enumerate(messages):

    # RULE:
    # Hide last assistant message *only if user has already asked something*
    user_has_asked = any(m["role"] == "user" for m in messages)

    if user_has_asked:
        # Skip duplicate rendering of last assistant message
        if i == len(messages) - 1 and msg["role"] == "assistant":
            continue

    # Render normally
    with st.chat_message(msg["role"]):
        content = msg["content"]

        if isinstance(content, dict):
            st.markdown(
                format_legal_text(
                    content,
                    st.session_state.translator,
                    st.session_state.selected_language,
                )
            )
        else:
            st.markdown(str(content))


# always show the latest message immediately if messages exist and we have at least 1
if st.session_state.messages:
    last_msg = st.session_state.messages[-1]
    # We'll display last_msg only if it was not just added this run by immediate display logic (below)
    # But to keep behavior consistent we don't duplicate: latest will be handled by input pipeline (immediate)
    pass

# ============================================================================
# Chat input and pipeline
# ============================================================================
prompt = st.chat_input(f"Ask in {languages[selected_lang]}... (Max {st.session_state.max_query_length} chars)")
if prompt:
    # Validate length
    valid, info = check_query_length(prompt, st.session_state.max_query_length)
    if not valid:
        err_text = info
        if selected_lang != "english":
            err_text = safe_translate(st.session_state.translator, err_text, "english", selected_lang)
        with st.chat_message("assistant"):
            st.error(err_text)
        st.session_state.messages.append({"role": "assistant", "content": {"type": "error", "message": err_text}, "timestamp": datetime.now().isoformat()})
        st.experimental_rerun()

    # 1) Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2) Save user message to history
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": datetime.now().isoformat()})

    # 3) Translate user's prompt into English (backend language)
    if selected_lang != "english":
        english_query = safe_translate(st.session_state.translator, prompt, selected_lang, "english")
    else:
        english_query = prompt

    # 4) Query backend (modelRun) — runs in English
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                bot_response = modelRun(english_query)  # expected to be dict with keys like status, title, explanation...
            except Exception as e:
                err_msg = f"Error during modelRun: {e}"
                # translate error message if necessary
                display_err = safe_translate(st.session_state.translator, err_msg, "english", selected_lang) if selected_lang != "english" else err_msg
                st.error(display_err)
                st.session_state.messages.append({"role": "assistant", "content": {"type": "error", "message": display_err}, "timestamp": datetime.now().isoformat()})
                st.experimental_rerun()

            # 5) Format and translate final output to selected language
            try:
                final_rendered = format_legal_text(bot_response, st.session_state.translator, selected_lang)
            except Exception:
                # fallback to a safe str rendering
                final_rendered = str(bot_response)

            # 6) Display final rendered output immediately
            st.markdown(final_rendered)

    # 7) Save assistant response to history in a way that preserves both source data and rendered text
    # We store a dict with two keys: 'bot' = original response dict (if any), 'rendered' = final translated markdown string
    stored_content = bot_response if isinstance(bot_response, dict) else {"raw": bot_response}
    wrapped = {"bot": stored_content, "rendered": final_rendered}
    st.session_state.messages.append({"role": "assistant", "content": wrapped, "timestamp": datetime.now().isoformat()})

    # 8) Trim history for performance
    if len(st.session_state.messages) > MAX_HISTORY_ITEMS:
        st.session_state.messages = st.session_state.messages[-TRIM_TO_LAST:]

    # 9) Rerun to ensure UI updates (history will now include this turn)
    st.rerun()

# ============================================================================
# Auto-refresh / Inbox polling (only when Inbox selected)
# ============================================================================
if menu == "Inbox":
    st.session_state.auto_refresh = True
else:
    st.session_state.auto_refresh = False

if st.session_state.auto_refresh and menu == "Inbox":
    # small sleep so we don't lock the UI too aggressively
    time.sleep(1)
    st.rerun()

