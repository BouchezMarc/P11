from fastapi import FastAPI
from stable_baselines3 import DQN
import gymnasium as gym
from gymnasium.wrappers import RecordVideo
import numpy as np
import os
import time


MODEL_PATH = "./model/dqn_lunarlander_final_3"

VIDEO_DIR = "videos"


app = FastAPI(
    title="Fast API Eagle-1 Autopilot API"
)


print("Chargement du modèle...")

model = DQN.load(MODEL_PATH)

print("Modèle chargé.")


@app.get("/")
def home():
    return {
        "status": "Eagle-1 online"
    }


# ---------------------------------
# Jouer une partie complète
# ---------------------------------

@app.get("/play_episode")
def play_episode():


    os.makedirs(
        VIDEO_DIR,
        exist_ok=True
    )


    env = gym.make(
        "LunarLander-v3",
        render_mode="rgb_array"
    )


    env = RecordVideo(
        env,
        video_folder=VIDEO_DIR,
        name_prefix="eagle1"
    )


    obs, info = env.reset()


    done = False

    total_reward = 0
    steps = 0


    while not done:


        action, _ = model.predict(
            obs,
            deterministic=True
        )


        obs, reward, terminated, truncated, info = env.step(
            action
        )


        total_reward += reward

        steps += 1


        done = terminated or truncated



    env.close()


    return {
        "reward": round(float(total_reward),2),
        "steps": steps,
        "video": "videos/eagle1*.mp4"
    }



# ---------------------------------
# Evaluation 100 épisodes
# ---------------------------------

@app.get("/evaluate")
def evaluate():


    env = gym.make(
        "LunarLander-v3"
    )


    rewards = []

    lengths = []


    for episode in range(100):


        obs, info = env.reset()


        done = False

        reward_total = 0

        steps = 0


        while not done:


            action, _ = model.predict(
                obs,
                deterministic=True
            )


            obs, reward, terminated, truncated, info = env.step(
                action
            )


            reward_total += reward

            steps += 1


            done = terminated or truncated



        rewards.append(
            reward_total
        )

        lengths.append(
            steps
        )



    env.close()


    return {

        "mean_reward":
            float(np.mean(rewards)),

        "std_reward":
            float(np.std(rewards)),

        "max_reward":
            float(np.max(rewards)),

        "success":
            int(sum(r > 200 for r in rewards)),

        "rewards":
            rewards,

        "lengths":
            lengths
    }