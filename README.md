# facial-morse

A computer vision project to translate Morse code, generated by opening/closing of the eyes and mouth, into plain English.

### How are blinks detected?

This project detects opening and closing of facial features (eyes and mouth) by calculating aspect ratios (AR) using coordinates (landmarks) provided by the dlib pose estimator and shape_predictor_68_face_landmarks model.
When open, the AR is fairly constant, however, when closed it approximates 0. Thus we can define a threshold and register a blink when the AR dips below the threshold.\
There are other ways to do this, such as calculating the area of the eye's whites and timing it's presence, however,
this method is more computationally expensive than the former (Cech & Soukupova, 2016). Because this project is intended to run on a embedded system (such as a raspberry pi),
the aspect-ratio method is preferred.

## The facial-morse system

- Short blink = dot
- Long blink = dash
- Open mouth = end morse sequence/backspace

## Features

- Freestyle mode: Test your morse knowledge in freestly mode
- Practice mode: Practice your skills by playing with a randomly generated word
- Match logging: View your past attempts and learn from your mistakes

## How to run locally from CLI

1. Ensure python3, pip, OpenCV4 (and its dependencies) are installed on your system
2. Clone the repo onto your system
3. Create a virtual environment:

```commandline
# for example, using python venv:
cd /path/to/repo
python -m venv venv_name
```

4. Activate virtual environment and install the project dependencies

```commandline
# for example, using python venv:
source /venv_name/bin/activate
sudo pip install -r requirements.txt
```

5. Run the program:

```commandline
python3 main.py --shape-predictor shape_predictor_68_face_landmarks.dat
```

NOTE: This project uses the "shape_predictor_68_face_landmarks" for facial landmark detection.
It should be included when you clone the repo. If not, just google it and download the .dat
file into the root of the project.

---

## References

Cech, J., Soukupova, T., (2016). Real-Time Eye Blink Detection using Facial Landmarks. https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf
