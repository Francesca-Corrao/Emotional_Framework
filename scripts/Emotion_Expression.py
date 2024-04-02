"""
Emotion Expression Component: get the emotion the robot feel in EPA space and perform one of the 5 it's able to feel.
From EPA found the closest one among the 5 he can display [Happy, Neutral, Sad, Anger and Fear].
Send the clue for the Expression to the Agent. 
It takes into account the time decay of emotions and the fact that the transition should be smooth. 
"""