import json
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from resume_handling.image_user_resume import  main as image_Resume
from resume_handling.pdf_user_resume import  main as pdf_Resume
from resume_handling.text_user_resume import  main as text_Resume

from agno.agent import Agent, RunOutput


def build_system_prompt() -> str:
    return (
        "Role: Objective resume assessment agent.\n"
        "Task: Evaluate the candidate resume against the provided job description AND generate objective MCQs.\n"
        "Always respond with strict JSON only (no markdown, no code fences).\n"
        "Schema: {\n"
        "  \"assessment_markdown\": string,  # Markdown section with headings and bullets, rationale included, objective\n"
        "  \"mcqs\": [\n"
        "    {\n"
        "      \"question\": string,\n"
        "      \"options\": [string, string, string, string],\n"
        "      \"answer_index\": integer,  # 0-based index of correct option\n"
        "      \"explanation\": string    # Short rationale for the correct answer\n"
        "    }\n"
        "  ]\n"
        "}\n"
        "Constraints:\n"
        "- Use only the provided texts; be specific, evidence-based, no speculation.\n"
        "- Each MCQ must be unambiguous, single best answer, and grounded in JD/resume.\n"
        "- Prefer skills, responsibilities, tools, and experience alignment for MCQs.\n"
    )


def build_user_prompt(jd_text: str, resume_text: str, num_mcqs: int = 5) -> str:
    return (
        "You are given a job description (JD) and a candidate resume.\n"
        "1) Produce an objective resume assessment (as markdown) with:\n"
        "   - Overall match score (0-100) with a short rationale.\n"
        "   - Strengths mapped to JD requirements (bulleted).\n"
        "   - Gaps/missing skills and potential risks (bulleted).\n"
        "   - Actionable recommendations to tailor the resume for this JD.\n"
        "2) Generate exactly {num} multiple-choice questions (MCQs) with 4 options each,\n"
        "   centered on alignment of resume to JD (skills/tools/experience). Provide the correct\n"
        "   option index and a brief explanation.\n\n"
        f"JD:\n{jd_text}\n\n"
        f"RESUME:\n{resume_text}\n\n"
        "Respond ONLY with valid JSON as per the schema above."
    ).format(num=num_mcqs)


def main(jd_text: str, resume: str, source_type: str, api_key: str, num_mcqs: int = 5) -> str:
    if source_type == "pdf":
        resume_text = pdf_Resume(resume)
    elif source_type == "image":
        resume_text = image_Resume(resume)
    elif source_type == "text":
        resume_text = text_Resume(resume)
    else:
        raise ValueError(f"Unsupported source_type: {source_type}")

    agent = Agent(
        model=OpenAIChat(id='gpt-4o', api_key=api_key),
        description=build_system_prompt(),
        markdown=False,
        session_id='fixed_id_for_demo',
        db=SqliteDb(db_file='user_memories/data.db'),
        add_history_to_context=True,
        num_history_runs=10,
    )

    user_prompt = build_user_prompt(jd_text=jd_text, resume_text=resume_text, num_mcqs=num_mcqs)

    response: RunOutput = agent.run(user_prompt)

    # Ensure we return a plain JSON string that Streamlit can parse.
    text = str(response.content)
    # Best-effort: validate JSON and re-dump to normalize formatting.
    try:
        data = json.loads(text)
        return json.dumps(data, ensure_ascii=False)
    except Exception:
        # If the model included extra text, attempt to extract JSON segment.
        try:
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1 and end > start:
                data = json.loads(text[start:end+1])
                return json.dumps(data, ensure_ascii=False)
        except Exception:
            pass
    return text
