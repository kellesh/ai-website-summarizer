import gradio as gr
from summarizer import summarize

# =============================================================================
# HISTORY
# =============================================================================

history_data = []
MAX_HISTORY = 100


# =============================================================================
# HELPERS
# =============================================================================

def get_history_choices():
    return [
        f"{idx + 1:03d}. {item['url']}"
        for idx, item in enumerate(history_data)
    ]


# =============================================================================
# SUMMARIZE
# =============================================================================

def summarize_url(url):

    if not url.strip():
        yield (
            "⚠️ Please enter a URL",
            """
### 🤖 AI Summary

Please enter a valid URL.
""",
            gr.update()
        )
        return

    yield (
        "⏳ Processing website content...",
        """
### 🤖 AI Summary

Analyzing website content...
""",
        gr.update()
    )

    try:
        result = summarize(url)

        history_data.insert(
            0,
            {
                "url": url,
                "summary": result
            }
        )

        history_data[:] = history_data[:MAX_HISTORY]

        history_choices = get_history_choices()

        formatted_response = f"""
        ## 🤖 AI Summary

        {result}
        """

        yield (
            "✅ Summary generated successfully",
            formatted_response,
            gr.update(
                choices=history_choices,
                value=history_choices[0]
            )
        )

    except Exception as ex:

        yield (
            f"❌ Error: {str(ex)}",
            f"""
### ❌ Error

{str(ex)}
""",
            gr.update()
        )


# =============================================================================
# LOAD HISTORY
# =============================================================================

def load_history(selection):

    if not selection:
        return "", ""

    try:
        index = int(selection.split(".")[0]) - 1

        if index >= len(history_data):
            return "", ""

        item = history_data[index]

        return (
            item["url"],
            f"""
### 🤖 AI Summary

{item['summary']}
"""
        )

    except Exception:
        return "", ""


# =============================================================================
# CLEAR
# =============================================================================

def clear_view():
    return (
        "",
        "",
        """
### 🤖 AI Summary

Summary will appear here.
"""
    )


# =============================================================================
# CSS
# =============================================================================

CUSTOM_CSS = """
.gradio-container {
    max-width: 100% !important;
}

/* --------------------------------------------------
   HISTORY SIDEBAR
-------------------------------------------------- */

.history-panel {
    height: 92vh;
    overflow-y: auto;
    resize: horizontal;

    min-width: 280px;

    border-right: 1px solid #e5e7eb;

    padding-right: 12px;
}

.history-list {
    height: 82vh;
    overflow-y: auto !important;
}

/* --------------------------------------------------
   MAIN PANEL
-------------------------------------------------- */

.main-panel {
    padding-left: 18px;
}

/* --------------------------------------------------
   STATUS
-------------------------------------------------- */

.status-box {
    min-height: 35px;

    margin-top: 10px;
    margin-bottom: 14px;

    font-weight: 600;
}

/* --------------------------------------------------
   AI RESPONSE PANEL
-------------------------------------------------- */

/* ==========================================
   AI RESPONSE PANEL
========================================== */

#summary_output {
    background: #ffffff;

    border: 1px solid #e5e7eb;

    border-radius: 14px;

    padding: 24px;

    min-height: 550px;

    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

    overflow-y: auto;

    line-height: 1.8;
}

/* Force ALL text to remain visible */

#summary_output,
#summary_output *,
#summary_output p,
#summary_output span,
#summary_output div,
#summary_output li,
#summary_output ul,
#summary_output ol,
#summary_output strong,
#summary_output b,
#summary_output em,
#summary_output i,
#summary_output h1,
#summary_output h2,
#summary_output h3,
#summary_output h4,
#summary_output h5,
#summary_output h6 {

    color: #111827 !important;
}

/* Bullet lists */

#summary_output ul,
#summary_output ol {
    margin-left: 24px;
    padding-left: 12px;
}

#summary_output li {
    margin-bottom: 6px;
}

/* Headings */

#summary_output h1,
#summary_output h2,
#summary_output h3,
#summary_output h4 {
    margin-top: 18px;
    margin-bottom: 10px;
    font-weight: 700;
}

/* Bold text */

#summary_output strong,
#summary_output b {
    color: #000000 !important;
    font-weight: 700;
}

/* Code blocks */

#summary_output code {
    background: #f3f4f6;

    color: #111827 !important;

    padding: 2px 6px;

    border-radius: 4px;
}

#summary_output pre {
    background: #f8fafc;

    color: #111827 !important;

    border: 1px solid #e5e7eb;

    border-radius: 8px;

    padding: 12px;

    overflow-x: auto;
}

/* Blockquotes */

#summary_output blockquote {

    border-left: 4px solid #3b82f6;

    background: #f8fbff;

    color: #111827 !important;

    padding: 10px 15px;

    margin: 10px 0;
}

/* Links */

#summary_output a {
    color: #2563eb !important;
    text-decoration: underline;
}

/* --------------------------------------------------
   BUTTON SPACING
-------------------------------------------------- */

.action-row {
    margin-top: 10px;
    margin-bottom: 10px;
}
"""


# =============================================================================
# UI
# =============================================================================

with gr.Blocks(
    title="AI Website Summarizer",
    theme=gr.themes.Soft(),
    css=CUSTOM_CSS
) as demo:

    gr.Markdown("# 🔎 AI Website Summarizer")

    with gr.Row():

        # ==============================================================
        # LEFT SIDEBAR
        # ==============================================================

        with gr.Column(
            scale=3,
            elem_classes=["history-panel"]
        ):

            gr.Markdown("## 📜 History")

            history_list = gr.Radio(
                choices=[],
                show_label=False,
                elem_classes=["history-list"]
            )

        # ==============================================================
        # RIGHT PANEL
        # ==============================================================

        with gr.Column(
            scale=7,
            elem_classes=["main-panel"]
        ):

            url_input = gr.Textbox(
                label="Website URL",
                placeholder="https://example.com"
            )

            with gr.Row(
                elem_classes=["action-row"]
            ):

                summarize_btn = gr.Button(
                    "🚀 Summarize",
                    variant="primary"
                )

                clear_btn = gr.Button(
                    "🧹 Clear"
                )

            status_output = gr.Markdown(
                value="",
                elem_classes=["status-box"]
            )

            gr.Markdown("### Summary")

            summary_output = gr.Markdown(
                value="""
### 🤖 AI Summary

Summary will appear here.
""",
                elem_id="summary_output"
            )

    # ==============================================================
    # EVENTS
    # ==============================================================

    summarize_btn.click(
        fn=summarize_url,
        inputs=url_input,
        outputs=[
            status_output,
            summary_output,
            history_list
        ]
    )

    history_list.change(
        fn=load_history,
        inputs=history_list,
        outputs=[
            url_input,
            summary_output
        ]
    )

    clear_btn.click(
        fn=clear_view,
        outputs=[
            url_input,
            status_output,
            summary_output
        ]
    )

# =============================================================================
# START
# =============================================================================

demo.launch(
    share=True
)