import streamlit as st

from core.retrieval.pageindex_client import (

    upload_document,

    wait_for_processing
)

from core.llm.rag_pipeline import (
    academic_rag_pipeline
)

from core.preprocessing.hybrid_loader import (
    load_pdf_hybrid
)

from core.chunking.semantic_chunker import (
    generate_semantic_chunks
)

from core.analytics.academic_analytics import (
    generate_academic_insights
)


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(

    page_title="Academic Intelligence System",

    layout="wide"
)


# -----------------------------------
# TITLE
# -----------------------------------

st.title(
    "AI-Powered Academic Intelligence System"
)

st.markdown(
    "Upload academic PDFs and interact with them intelligently."
)


# -----------------------------------
# SESSION STATE
# -----------------------------------

if "doc_id" not in st.session_state:

    st.session_state.doc_id = None


if "documents_loaded" not in st.session_state:

    st.session_state.documents_loaded = False


if "analytics" not in st.session_state:

    st.session_state.analytics = None


# -----------------------------------
# FILE UPLOAD
# -----------------------------------

uploaded_files = st.file_uploader(

    "Upload PDFs",

    type=["pdf"],

    accept_multiple_files=True
)


# -----------------------------------
# PROCESS DOCUMENTS
# -----------------------------------

if uploaded_files:

    if st.button("Process Documents"):

        with st.spinner(
            "Processing documents..."
        ):

            all_chunks = []

            # -----------------------------------
            # SAVE FILES TEMPORARILY
            # -----------------------------------

            for uploaded_file in uploaded_files:

                file_path = f"temp_{uploaded_file.name}"

                with open(file_path, "wb") as f:

                    f.write(
                        uploaded_file.read()
                    )

                # -----------------------------------
                # PAGEINDEX UPLOAD
                # -----------------------------------

                doc_id = upload_document(
                    file_path
                )

                wait_for_processing(
                    doc_id
                )

                st.session_state.doc_id = doc_id

                # -----------------------------------
                # LOCAL ANALYTICS
                # -----------------------------------

                documents = load_pdf_hybrid(
                    file_path
                )

                for document in documents:

                    chunks = generate_semantic_chunks(
                        document
                    )

                    all_chunks.extend(chunks)

            # -----------------------------------
            # GENERATE ANALYTICS
            # -----------------------------------

            analytics = generate_academic_insights(
                all_chunks
            )

            st.session_state.analytics = analytics

            st.session_state.documents_loaded = True

        st.success(
            "Documents processed successfully!"
        )


# -----------------------------------
# MAIN MVP FEATURES
# -----------------------------------

if st.session_state.documents_loaded:

    tab1, tab2, tab3 = st.tabs([

        "Ask Questions",

        "Academic Insights",

        "Summaries"
    ])


    # -----------------------------------
    # TAB 1 — QA
    # -----------------------------------

    with tab1:

        st.subheader(
            "Ask Questions"
        )

        user_question = st.text_input(
            "Enter your question"
        )

        if st.button("Get Answer"):

            with st.spinner(
                "Generating answer..."
            ):

                response = academic_rag_pipeline(

                    st.session_state.doc_id,

                    user_question
                )

                st.markdown(
                    response
                )


    # -----------------------------------
    # TAB 2 — ANALYTICS
    # -----------------------------------

    with tab2:

        st.subheader(
            "Academic Insights"
        )

        analytics = st.session_state.analytics

        # -----------------------------------
        # MOST REPEATED TOPICS
        # -----------------------------------

        st.markdown(
            "### Most Repeated Topics"
        )

        repeated_topics = analytics[
            "most_repeated_topics"
        ]

        if repeated_topics:

            for topic, count in repeated_topics.items():

                st.write(
                    f"• {topic} → {count}"
                )

        else:

            st.info(
                "No topic analytics available."
            )


        # -----------------------------------
        # HIGHEST WEIGHTAGE
        # -----------------------------------

        st.markdown(
            "### Highest Weightage Topics"
        )

        weightage_topics = analytics[
            "highest_weightage_topics"
        ]

        if weightage_topics:

            for topic, marks in weightage_topics.items():

                st.write(
                    f"• {topic} → {marks} marks"
                )

        else:

            st.info(
                "No marks analytics available."
            )


    # -----------------------------------
    # TAB 3 — SUMMARIES
    # -----------------------------------

    with tab3:

        st.subheader(
            "Chapter Summaries"
        )

        st.info(
            "Summary generation will be added in the next phase."
        )