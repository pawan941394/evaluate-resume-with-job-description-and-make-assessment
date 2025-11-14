import os
import json
import tempfile
import streamlit as st
from llm_agent import main as run_agent

st.set_page_config(page_title="Resume Assessment & Interview Questions", page_icon="🧠", layout="centered")

st.title("Resume Assessment & Interview Questions")
st.caption("Upload your resume (PDF/Image/Text), paste the JD, and get an objective assessment + tailored interview questions.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", help="Will be set as OPENAI_API_KEY for this session.")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    st.markdown("---")
    st.info("Tip: For images, ensure Tesseract OCR is installed if your image handler is unavailable.")

source_type = st.selectbox("Resume source type", ["pdf", "image", "text"], index=0)

resume_input = None
if source_type == "text":
    resume_input = st.text_area("Paste resume text", height=200, placeholder="Paste your resume text here...")
elif source_type == "pdf":
    uploaded = st.file_uploader("Upload resume PDF", type=["pdf"])
    if uploaded:
        # Persist to a temp file and pass the path to the agent
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded.read())
            resume_input = tmp.name
else:  # image
    uploaded = st.file_uploader("Upload resume image", type=["png", "jpg", "jpeg", "bmp", "tif", "tiff"])
    if uploaded:
        ext = os.path.splitext(uploaded.name or "")[1].lower() or ".png"
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(uploaded.read())
            resume_input = tmp.name

jd_text = st.text_area("Paste Job Description", height=220, placeholder="Paste the job description here...")

col1, col2 = st.columns([1, 1])
with col1:
    run_btn = st.button("Generate Assessment + Questions", type="primary")
with col2:
    clear_btn = st.button("Clear")

if clear_btn:
    try:
        st.rerun()
    except AttributeError:
        # Fallback for older Streamlit versions
        st.experimental_rerun()

if run_btn:
    if not os.getenv("OPENAI_API_KEY"):
        st.error("Please provide your OpenAI API Key in the sidebar.")
    elif source_type in ("pdf", "image") and not resume_input:
        st.error("Please upload your resume file.")
    elif source_type == "text" and not (resume_input and resume_input.strip()):
        st.error("Please paste your resume text.")
    elif not (jd_text and jd_text.strip()):
        st.error("Please paste the job description.")
    else:
        with st.spinner("Generating assessment and objective MCQs..."):
            try:
                output_json = run_agent(
                    jd_text=jd_text.strip(),
                    resume=resume_input,
                    source_type=source_type,
                    api_key=api_key,
                )

                data = None
                try:
                    data = json.loads(output_json)
                except Exception:
                    st.warning("The model did not return strict JSON. Showing raw output below.")
                    st.markdown(output_json)
                    st.stop()

                assessment_md = data.get("assessment_markdown", "")
                mcqs = data.get("mcqs", []) or []

                # Display assessment
                st.subheader("Assessment")
                if assessment_md:
                    st.markdown(assessment_md)
                else:
                    st.info("No assessment text returned.")

                # Initialize session state for assessment & MCQs
                if "mcqs" not in st.session_state:
                    st.session_state["mcqs"] = mcqs
                else:
                    st.session_state["mcqs"] = mcqs

                st.session_state["assessment_md"] = assessment_md

                if "selections" not in st.session_state:
                    st.session_state["selections"] = {}
                if "checked" not in st.session_state:
                    st.session_state["checked"] = False

            except Exception as e:
                st.error(f"Error: {e}")

# Render MCQ section if available
if "mcqs" in st.session_state and st.session_state["mcqs"]:
    st.markdown("---")
    st.subheader("Objective MCQs")

    for idx, q in enumerate(st.session_state["mcqs"]):
        question = q.get("question", f"Question {idx+1}")
        options = q.get("options", [])
        if not options:
            st.warning(f"Q{idx+1} has no options returned by the model.")
            continue
        st.write(f"{idx+1}. {question}")
        default_index = st.session_state["selections"].get(idx, None)
        choice = st.radio(
            label=f"Choose an option for Q{idx+1}",
            options=list(range(len(options))),
            format_func=lambda i: options[i] if i is not None and i < len(options) else "",
            index=default_index if default_index is not None else 0,
            key=f"q_{idx}",
            horizontal=False,
        )
        st.session_state["selections"][idx] = choice
        st.markdown("")

    submitted = st.button("Submit Answers", type="primary")

    if submitted:
        st.session_state["checked"] = True

    if st.session_state.get("checked"):
        correct = 0
        total = len(st.session_state["mcqs"])
        st.markdown("---")
        st.subheader("Results")
        for idx, q in enumerate(st.session_state["mcqs"]):
            answer_index = q.get("answer_index", -1)
            explanation = q.get("explanation", "")
            user_pick = st.session_state["selections"].get(idx, -1)
            is_right = user_pick == answer_index
            if is_right:
                correct += 1
                st.success(f"Q{idx+1}: Correct ✅")
            else:
                st.error(f"Q{idx+1}: Incorrect ❌")
            # Show feedback
            opts = q.get("options", [])
            correct_text = opts[answer_index] if 0 <= answer_index < len(opts) else "(Invalid index)"
            picked_text = opts[user_pick] if 0 <= user_pick < len(opts) else "(No selection)"
            st.caption(f"Your answer: {picked_text}")
            st.caption(f"Correct answer: {correct_text}")
            if explanation:
                st.info(f"Why: {explanation}")
            st.markdown("")

        st.write(f"Score: {correct} / {total} ({(100*correct/total):.0f}%)")

        # Build a downloadable markdown summary
        def build_download_md() -> str:
            assess = st.session_state.get("assessment_md", "")
            lines = ["# Resume Assessment & MCQs", "", "## Assessment", "", assess or "(none)", "", "## MCQs"]
            for idx, q in enumerate(st.session_state["mcqs"]):
                opts = q.get("options", [])
                answer_index = q.get("answer_index", -1)
                explanation = q.get("explanation", "")
                lines.append("")
                lines.append(f"{idx+1}. {q.get('question','')}")
                for i, opt in enumerate(opts):
                    prefix = "*" if i == answer_index else "-"
                    lines.append(f"    {prefix} {opt}")
                if explanation:
                    lines.append(f"    _Why_: {explanation}")
            lines.append("")
            lines.append(f"Score: {correct}/{total} ({(100*correct/total):.0f}%)")
            return "\n".join(lines)

        dl_md = build_download_md()
        st.download_button(
            "Download Result",
            data=dl_md.encode("utf-8"),
            file_name="assessment_and_mcqs.md",
            mime="text/markdown",
        )
else:
    # If nothing generated yet, keep UI clean
    pass
