import numpy as np

def bayes_filter(belief, action, measurement):
    # Transition model definition
    transition_model_push = np.array([[1.0, 0.0],
                                 [0.8, 0.2]])
    transition_model_noth = np.array([[1.0, 0.0],
                                 [0.0, 1.0]])
    
    transition_model= { 0 : transition_model_noth, 1 : transition_model_push}

    # Measurement model definition
    measurement_model = np.array([[0.6, 0.4],
                                 [0.2, 0.8]])

    # Update belief based on action
    # print("model",transition_model[action].T)
    belief = np.dot(transition_model[action].T, belief)
    print("after prediction",belief)

    # Update belief based on measurement
    belief = np.multiply(measurement_model[:, measurement], belief)
    belief /= np.sum(belief)

    return belief

def main():
    # Initialize belief of door is open or closed
    belief = np.array([0.5, 0.5])

    # List of [action, measurement] pairs, 
    # actions : 0 = do_nothing , 1 = push
    # measuremnt : 0 = is_open , 1 = is_closed
    action_measurement_pairs = [
        {"action": 0, "measurement": 1},
        {"action": 0, "measurement": 1},
        {"action": 1, "measurement": 1},
        {"action": 1, "measurement": 0},
        {"action": 0, "measurement": 0},
    ]

    # Iterate through action_measurement_pairs and update belief
    for pair in action_measurement_pairs:
        belief = bayes_filter(belief, pair["action"], pair["measurement"])
        print("Belief after [Action: {}, Measurement: {}]: {}".format(pair["action"], pair["measurement"], belief))

if __name__ == "__main__":
    main()
