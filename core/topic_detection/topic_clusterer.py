from collections import defaultdict


# -----------------------------------
# SEMANTIC CLUSTER DEFINITIONS
# -----------------------------------

TOPIC_CLUSTERS = {

    "Synchronization": [

        "clock",
        "lamport",
        "vector clock",
        "mutual exclusion",
        "dme",
        "meakawa",
        "synchronization"
    ],

    "Communication": [

        "rpc",
        "message passing",
        "communication",
        "protocol"
    ],

    "Distributed Systems": [

        "distributed",
        "transparency",
        "network os",
        "distributed os"
    ],

    "Process Management": [

        "deadlock",
        "process",
        "thread",
        "scheduling"
    ]
}


def cluster_topics(stabilized_topics):

    clustered_topics = defaultdict(list)

    unclustered_topics = []

    for item in stabilized_topics:

        topic = item["topic"].lower()

        matched = False

        # -----------------------------------
        # CHECK CLUSTER MATCH
        # -----------------------------------

        for cluster_name, keywords in TOPIC_CLUSTERS.items():

            for keyword in keywords:

                if keyword in topic:

                    clustered_topics[
                        cluster_name
                    ].append(
                        item["topic"]
                    )

                    matched = True

                    break

            if matched:
                break

        # -----------------------------------
        # UNCLUSTERED TOPICS
        # -----------------------------------

        if not matched:

            unclustered_topics.append(
                item["topic"]
            )

    return {

        "clusters": dict(clustered_topics),

        "unclustered": unclustered_topics
    }