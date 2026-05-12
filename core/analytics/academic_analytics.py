from collections import defaultdict
from collections import defaultdict


# -----------------------------------
# ANALYZE TOPIC FREQUENCY
# -----------------------------------

def analyze_topic_frequency(chunks):

    topic_frequency = defaultdict(int)

    for chunk in chunks:

        topic_clusters = chunk.get(
            "topic_clusters",
            {}
        )

        for cluster_name in topic_clusters:

            topic_frequency[
                cluster_name
            ] += 1

    return dict(
        sorted(

            topic_frequency.items(),

            key=lambda x: x[1],

            reverse=True
        )
    )


# -----------------------------------
# ANALYZE MARKS WEIGHTAGE
# -----------------------------------

def analyze_marks_weightage(chunks):

    marks_distribution = defaultdict(int)

    for chunk in chunks:

        marks = chunk.get("marks")

        topic_clusters = chunk.get(
            "topic_clusters",
            {}
        )

        if marks:

            try:

                numeric_marks = int(
                    ''.join(
                        filter(str.isdigit, str(marks))
                    ) or 0
                )

            except:

                numeric_marks = 0

        else:

            numeric_marks = 0

        for cluster_name in topic_clusters:

            marks_distribution[
                cluster_name
            ] += numeric_marks

    return dict(

        sorted(

            marks_distribution.items(),

            key=lambda x: x[1],

            reverse=True
        )
    )


# -----------------------------------
# GENERATE FINAL INSIGHTS
# -----------------------------------

def generate_academic_insights(chunks):

    topic_frequency = analyze_topic_frequency(
        chunks
    )

    marks_weightage = analyze_marks_weightage(
        chunks
    )

    insights = {

        "most_repeated_topics":
            topic_frequency,

        "highest_weightage_topics":
            marks_weightage
    }

    return insights

# -----------------------------------
# GENERATE ADVANCED ANALYTICS
# -----------------------------------

def generate_advanced_analytics(chunks):

    analytics = defaultdict(

        lambda: {

            "frequency": 0,

            "weightage": 0,

            "questions": [],

            "subtopics": set()
        }
    )

    # -----------------------------------
    # PROCESS CHUNKS
    # -----------------------------------

    for chunk in chunks:

        topic_clusters = chunk.get(
            "topic_clusters",
            {}
        )

        marks = chunk.get(
            "marks",
            0
        )

        chunk_text = chunk.get(
            "chunk_text",
            ""
        )

        try:

            numeric_marks = int(
                ''.join(
                    filter(str.isdigit, str(marks))
                ) or 0
            )

        except:

            numeric_marks = 0

        # -----------------------------------
        # UPDATE ANALYTICS
        # -----------------------------------

        for cluster_name, subtopics in topic_clusters.items():

            analytics[
                cluster_name
            ]["frequency"] += 1

            analytics[
                cluster_name
            ]["weightage"] += numeric_marks

            analytics[
                cluster_name
            ]["questions"].append(
                chunk_text[:250]
            )

            for subtopic in subtopics:

                analytics[
                    cluster_name
                ]["subtopics"].add(
                    subtopic
                )

    # -----------------------------------
    # PRIORITY SCORING
    # -----------------------------------

    final_analytics = {}

    for topic, data in analytics.items():

        score = (
            data["frequency"] * 2
            +
            data["weightage"]
        )

        if score >= 15:

            priority = "HIGH"

        elif score >= 7:

            priority = "MEDIUM"

        else:

            priority = "LOW"

        final_analytics[topic] = {

            "frequency":
                data["frequency"],

            "weightage":
                data["weightage"],

            "priority":
                priority,

            "likely_questions":
                data["questions"][:5],

            "subtopics":
                list(data["subtopics"])
        }

    return final_analytics