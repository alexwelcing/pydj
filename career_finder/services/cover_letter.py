from textwrap import dedent
from typing import Iterable, Optional


def _join_sentences(*sentences: str) -> str:
    cleaned = [sentence.strip() for sentence in sentences if sentence and sentence.strip()]
    return " ".join(cleaned)


def _format_skills(skills: Iterable[str]) -> str:
    items = [skill.strip() for skill in skills if skill and skill.strip()]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + f" and {items[-1]}"


def generate_cover_letter(
    role_name: str,
    applicant_name: str,
    company_name: str,
    hook_sentence_one: str,
    hook_sentence_two: str,
    current_company: str,
    product_or_team: Optional[str] = None,
    portfolio_link: Optional[str] = None,
    skills: Optional[Iterable[str]] = None,
) -> str:
    """Create a cover letter following the high-signal transition template.

    The template frames leadership changes as a natural transition point while
    highlighting hands-on engineering impact. Provide two custom hook sentences
    to tie your background to the target role.
    """

    custom_hook = _join_sentences(hook_sentence_one, hook_sentence_two)
    skills_text = _format_skills(skills or [])

    product_sentence = (
        f" This role on the {product_or_team} is the logical next step for my trajectory."
        if product_or_team
        else ""
    )

    skills_sentence = (
        f"My core stack includes {skills_text}, enabling me to ship production-ready AI experiences end to end. "
        if skills_text
        else ""
    )

    close_link = f"\n{portfolio_link}" if portfolio_link else ""

    letter_body = dedent(
        f"""
        Subject: Application for {role_name} - {applicant_name}

        {custom_hook}{product_sentence}

        Currently, I am driving technical strategy at {current_company}. Following our recent acquisition, my direct leadership chain (manager and director) has exited as part of the post-merger integration. While I remain a core contributor ensuring continuity, this restructuring has created a natural transition point for me. I am proactively exploring opportunities where I can commit my long-term focus, with the goal of aligning with a new team by Q1.

        I specialize in the intersection of software engineering and enterprise AI implementation—bridging the gap between theoretical models and production-grade software. I don’t just build features; I architect systems that scale. {skills_sentence}My background allows me to operate autonomously as a high-impact Individual Contributor, delivering complex technical solutions while maintaining the strategic awareness usually reserved for management.

        I am ready to bring this blend of hands-on coding and strategic implementation to {company_name} immediately. I would welcome a brief conversation to discuss how my background fits your roadmap for 2025.

        Best,
        {applicant_name}{close_link}
        """
    ).strip()

    return letter_body
