import json

import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go


# Page settings
st.set_page_config(
    page_title="SkillGraph AI",
    layout="wide"
)


# Basic styling
st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0;
}

.subtitle {
    color: #9ca3af;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background: #161b22;
    border: 1px solid #30363d;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# Load skill and role data
@st.cache_data
def load_data():

    with open("skills.json", "r", encoding="utf-8") as file:
        skills = json.load(file)

    with open("roles.json", "r", encoding="utf-8") as file:
        roles = json.load(file)

    return skills, roles


skills, roles = load_data()


# Application header
st.markdown(
    '<div class="title">SkillGraph AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze your skills, discover gaps and generate a learning path.'
    '</div>',
    unsafe_allow_html=True
)


# Sidebar inputs
st.sidebar.title("Skill Analysis")

role = st.sidebar.selectbox(
    "Target Role",
    list(roles.keys())
)

st.sidebar.markdown("---")

st.sidebar.subheader("Your Skills")

all_skills = list(skills.keys())

selected_skills = st.sidebar.multiselect(
    "Select skills you already know",
    all_skills
)

st.sidebar.markdown("---")

analyze = st.sidebar.button(
    "Analyze Skill Gap",
    use_container_width=True
)


# Show the landing page before analysis
if not analyze:

    st.info(
        "Select your target role and the skills you already know, "
        "then click Analyze Skill Gap."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Career Roles", len(roles))

    with col2:
        st.metric("Skills", len(skills))

    with col3:
        st.metric(
            "Skill Dependencies",
            sum(
                len(value["prerequisites"])
                for value in skills.values()
            )
        )

    st.markdown("---")

    st.subheader("How it works")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("### 01")
        st.write("Choose a career role.")

    with col2:
        st.markdown("### 02")
        st.write("Select your existing skills.")

    with col3:
        st.markdown("### 03")
        st.write("Analyze your skill gaps.")

    with col4:
        st.markdown("### 04")
        st.write("Get a dependency-based learning path.")

    st.stop()


# Get the skills required for the selected role
required_skills = roles[role]

known = set(selected_skills)

missing = [
    skill
    for skill in required_skills
    if skill not in known
]


# Calculate how many required skills the user already has
coverage = (
    len(known.intersection(required_skills))
    / len(required_skills)
) * 100


# Display the main metrics
st.subheader(f"{role} Analysis")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Skill Coverage",
        f"{coverage:.1f}%"
    )

with col2:
    st.metric(
        "Required Skills",
        len(required_skills)
    )

with col3:
    st.metric(
        "Skills You Have",
        len(known.intersection(required_skills))
    )

with col4:
    st.metric(
        "Skill Gaps",
        len(missing)
    )


st.progress(
    int(coverage),
    text=f"Skill coverage for {role}"
)

st.markdown("---")


# Show the status of every skill required by the role
st.subheader("Skill Gap")

status_data = []

for skill in required_skills:

    if skill in known:
        status = "Known"
    else:
        status = "Missing"

    status_data.append({
        "Skill": skill,
        "Category": skills[skill]["category"],
        "Status": status
    })


df = pd.DataFrame(status_data)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# Find all prerequisites for a particular skill
def find_dependencies(skill, result=None):

    if result is None:
        result = []

    prerequisites = skills.get(
        skill,
        {}
    ).get(
        "prerequisites",
        []
    )

    for prerequisite in prerequisites:

        if prerequisite not in result:

            result.append(prerequisite)

            find_dependencies(
                prerequisite,
                result
            )

    return result


# Build the learning path using the skill dependencies
learning_path = []

for skill in missing:

    dependencies = find_dependencies(skill)

    for dependency in dependencies:

        if (
            dependency not in known
            and dependency not in learning_path
        ):
            learning_path.append(dependency)

    if skill not in learning_path:
        learning_path.append(skill)


st.subheader("Recommended Learning Path")

if learning_path:

    for index, skill in enumerate(learning_path, 1):

        category = skills[skill]["category"]

        st.markdown(
            f"""
            <div class="card">

            <b>STEP {index}</b>

            <h3>{skill}</h3>

            <span>{category}</span>

            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.success(
        "You already have all the required skills for this role."
    )


# Create the dependency graph for the selected role
st.subheader("Skill Dependency Graph")

graph = nx.DiGraph()

for skill in required_skills:

    graph.add_node(skill)

    prerequisites = skills[skill]["prerequisites"]

    for prerequisite in prerequisites:

        if prerequisite in required_skills:

            graph.add_edge(
                prerequisite,
                skill
            )


# Calculate positions for the graph nodes
try:

    positions = nx.spring_layout(
        graph,
        seed=42,
        k=1.5
    )

except Exception:

    positions = nx.circular_layout(graph)


# Create graph edges
edge_x = []
edge_y = []

for source, target in graph.edges():

    x0, y0 = positions[source]
    x1, y1 = positions[target]

    edge_x.extend([
        x0,
        x1,
        None
    ])

    edge_y.extend([
        y0,
        y1,
        None
    ])


edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=1),
    hoverinfo="none",
    mode="lines"
)


# Create graph nodes
node_x = []
node_y = []
node_text = []
node_colors = []

for node in graph.nodes():

    x, y = positions[node]

    node_x.append(x)
    node_y.append(y)
    node_text.append(node)

    if node in known:
        node_colors.append(1)
    else:
        node_colors.append(0)


node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers+text",
    text=node_text,
    textposition="top center",
    hoverinfo="text",
    marker=dict(
        size=25,
        color=node_colors,
        colorscale=[
            [0, "#ef4444"],
            [1, "#22c55e"]
        ],
        showscale=False,
        line=dict(width=1)
    )
)


# Display the graph
fig = go.Figure(
    data=[
        edge_trace,
        node_trace
    ]
)

fig.update_layout(
    height=650,
    showlegend=False,
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# Show a short summary of the analysis
st.subheader("Analysis Summary")

if coverage >= 80:

    st.success(
        f"You currently cover {coverage:.1f}% of the skills "
        f"required for {role}."
    )

elif coverage >= 50:

    st.warning(
        f"You currently cover {coverage:.1f}% of the skills "
        f"required for {role}. Focus on the missing dependencies."
    )

else:

    st.error(
        f"You currently cover {coverage:.1f}% of the skills "
        f"required for {role}. Build the fundamentals first."
    )