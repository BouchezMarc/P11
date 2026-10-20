import streamlit as st
import requests
import pandas as pd


API = "http://127.0.0.1:8000"


st.title(
    "📊 Dashboard Eagle-1 RL Dashboard"
)


if st.button("Evaluer le modèle"):


    response = requests.get(
        f"{API}/evaluate"
    )


    st.session_state.result = response.json()



if "result" in st.session_state:


    data = st.session_state.result


    st.metric(
        "Reward moyen",
        round(data["mean_reward"],2)
    )


    st.metric(
        "Ecart type",
        round(data["std_reward"],2)
    )


    st.metric(
        "Meilleur score",
        round(data["max_reward"],2)
    )


    st.metric(
        "Réussites > 200",
        f"{data['success']} / 100"
    )


    df = pd.DataFrame(
        {
            "Episode": range(1,101),
            "Reward": data["rewards"],
            "Length": data["lengths"]
        }
    )


    st.subheader(
        "Récompenses"
    )


    st.line_chart(
        df.set_index("Episode")["Reward"]
    )


    st.subheader(
        "Durée des épisodes"
    )


    st.line_chart(
        df.set_index("Episode")["Length"]
    )