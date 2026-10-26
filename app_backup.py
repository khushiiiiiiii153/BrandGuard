
import streamlit as st
import sqlite3
import json
import re
from datetime import datetime

DB_NAME = "brandguard.db"

st.set_page_config(
    page_title="BrandGuard",
    page_icon="🛡️",
    layout="wide"
)


def get_connection():
    return sqlite3.connect(DB_NAME)


def setup_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                findings TEXT NOT NULL,
                decision TEXT DEFAULT 'Pending review',
                comments TEXT DEFAULT '',
                created_at TEXT NOT NULL
            )
        """)


def check_content(content, banned_words):
    findings = []

    for word in banned_words:
        word = word.strip()

        if not word:
            continue

        pattern = r"(?<!\w)" + re.escape(word) + r"(?!\w)"

        if re.search(pattern, content, flags=re.IGNORECASE):
            findings.append({
                "term": word,
                "reason": (
                    "This term is listed in the "
                    "sample brand's banned terms."
                ),
                "severity": "Review required",
                "source": "Brand Library - Banned terms"
            })

    return findings


def save_review(content, findings):
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO reviews
            (content, findings, created_at)
            VALUES (?, ?, ?)
        """, (
            content,
            json.dumps(findings),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        return cursor.lastrowid


def update_decision(review_id, decision, comments):
    with get_connection() as conn:
        conn.execute("""
            UPDATE reviews
            SET decision = ?, comments = ?
            WHERE id = ?
        """, (decision, comments, review_id))


def get_reviews():
    with get_connection() as conn:
        return conn.execute("""
            SELECT id, content, findings, decision, comments, created_at
            FROM reviews
            ORDER BY id DESC
        """).fetchall()


setup_database()

st.title("🛡️ BrandGuard")
st.caption("Explainable, Evidence-Checked Brand Governance")

st.info(
    "Check content against brand rules before publication. "
    "The final decision belongs to a human reviewer."
)

with st.sidebar:
    st.header("Brand Library")

    banned_text = st.text_area(
        "Banned terms (comma-separated)",
        value="guaranteed, best in India, 100% effective"
    )

    st.caption(
        "This prototype uses editable sample rules. "
        "Advanced brand-library management is not yet implemented."
    )

tab_check, tab_history = st.tabs(
    ["Content Checker", "Review History"]
)

with tab_check:
    st.subheader("1. Submit content")

    content = st.text_area(
        "Marketing content",
        height=160,
        placeholder="Paste your advertisement or social media caption..."
    )

    if st.button("Check Brand Compliance", type="primary"):
        if not content.strip():
            st.warning("Please enter content first.")
        else:
            banned_words = banned_text.split(",")
            findings = check_content(content, banned_words)
            review_id = save_review(content, findings)

            st.session_state["current_review_id"] = review_id
            st.success(f"Review #{review_id} saved successfully.")

    review_id = st.session_state.get("current_review_id")

    if review_id is not None:
        reviews = get_reviews()
        current = next(
            (r for r in reviews if r[0] == review_id),
            None
        )

        if current:
            st.subheader("2. Review Findings")
            findings = json.loads(current[2])

            if findings:
                st.error(
                    f"{len(findings)} potential issue(s) found."
                )

                for item in findings:
                    st.markdown(f"**Flagged term:** {item['term']}")
                    st.write(f"Reason: {item['reason']}")
                    st.write(f"Severity: {item['severity']}")
                    st.write(f"Source: {item['source']}")
                    st.divider()
            else:
                st.success("No banned terms detected.")
                st.caption(
                    "This basic check does not guarantee full compliance."
                )

            st.subheader("3. Human Review")

            with st.form("review_decision_form"):
                decision = st.selectbox(
                    "Reviewer decision",
                    [
                        "Pending review",
                        "Approve",
                        "Request changes",
                        "Reject"
                    ],
                    index=[
                        "Pending review",
                        "Approve",
                        "Request changes",
                        "Reject"
                    ].index(current[3])
                )

                comments = st.text_area(
                    "Comments or reason",
                    value=current[4]
                )

                submitted = st.form_submit_button(
                    "Save Review Decision"
                )

                if submitted:
                    if (
                        decision in ["Request changes", "Reject"]
                        and not comments.strip()
                    ):
                        st.warning(
                            "Please add a reason for this decision."
                        )
                    elif decision == "Pending review":
                        st.warning(
                            "Select a final decision before saving."
                        )
                    else:
                        update_decision(
                            review_id, decision, comments
                        )
                        st.success(
                            "Decision saved! Open Review History to verify."
                        )
                        st.rerun()

with tab_history:
    st.subheader("Saved Review History")
    reviews = get_reviews()

    if not reviews:
        st.info("No reviews saved yet.")
    else:
        st.write(f"Total saved reviews: {len(reviews)}")

        for row in reviews:
            (
                rid, saved_content, saved_findings,
                decision, comments, created_at
            ) = row

            with st.expander(
                f"Review #{rid} | {decision} | {created_at}"
            ):
                st.write("**Content:**")
                st.write(saved_content)

                items = json.loads(saved_findings)
                st.write(f"**Issues detected:** {len(items)}")

                for item in items:
                    st.write(
                        f"- {item['term']}: {item['reason']}"
                    )

                st.write("**Decision:**", decision)
                st.write("**Comments:**", comments or "None")

st.divider()
st.caption(
    "Prototype: rule-based checking only. "
    "AI review and advanced access controls are not implemented yet."
)
