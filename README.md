# Baller Shot Caller

A web-app game that lets users visually examine the play dynamics of an NBA game—focusing on the Spurs. Observe the play until the moment the ball is shot, without seeing the ball itself. Challenge the model and try to determine who took the shot.

![bsc_screenshot](https://github.com/kizzen/Baller-Shot-Caller/assets/19916076/acf1f24f-6ad4-43ce-ade1-63473f0e4006)

To see the app in action: https://www.youtube.com/watch?v=p69Cib-ZyK0

### How to run the app

1. Clone the repository
- `git clone https://github.com/kizzen/Baller-Shot-Caller.git`
2. In the directory you just cloned, create and activate a new virtual environment
- `cd Baller-Shot-Caller`
- `conda create -n bsc_env`
- `conda activate bsc_env`
3. Install the necessary packages from requirements.txt into the newly create environment
- with pip: `pip install -r requirements.txt`
- or conda: `while read requirement; do conda install --yes $requirement; done < requirements.txt`
4. Launch the app from the terminal
- `python app.py`
5. Click the given URL to access the app.: http://127.0.0.1:80.