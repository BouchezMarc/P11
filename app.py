import streamlit as st
import requests
import os
import glob


API = "http://127.0.0.1:8000"


st.title("🚀 GUI Eagle-1 Autopilot")


st.write(
    "Démonstration du pilote automatique LunarLander-v3"
)


if st.button("▶️ Lancer une partie"):

    try:

        response = requests.get(
            f"{API}/play_episode",
            timeout=120
        )

        data = response.json()


        st.success(
            "Partie terminée"
        )


        # ---------------------
        # Métriques
        # ---------------------

        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Reward obtenu",
                f"{data['reward']:.2f}"
            )


        with col2:

            st.metric(
                "Nombre d'actions",
                data["steps"]
            )


        # ---------------------
        # Recherche vidéo
        # ---------------------

        videos = glob.glob(
            "videos/*.mp4"
        )


        if videos:

            # dernière vidéo créée
            video_path = max(
                videos,
                key=os.path.getctime
            )


            st.subheader(
                "🎥 Partie jouée par l'agent"
            )


            st.video(
                video_path
            )


        else:

            st.warning(
                "Vidéo non trouvée dans le dossier videos/"
            )


    except Exception as e:

        st.error(
            f"Erreur : {e}"
        )