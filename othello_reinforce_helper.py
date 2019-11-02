import numpy as np

def display_results(player_1_wins, player_2_wins, ties, margins, steps_array, pieces):
    print('player_1 wins:', str(int(100*player_1_wins/episodes + 0.5)) + '%')
    print('player_2 wins:', str(int(100*player_2_wins/episodes + 0.5)) +'%')
    print('ties:', str(int(100*ties/episodes + 0.5))+ '%')
    print('Max, Mean, Min margins: ', end ='')
    print(np.max(margins), np.mean(margins), np.min(margins))
    print('Max, Mean, Min steps: ', end ='')
    print(np.max(steps_array), np.mean(steps_array), np.min(steps_array))
    print('Max, Mean, Min pieces: ', end ='')
    print(np.max(pieces), np.mean(pieces), np.min(pieces))
    
def play_with_model(model, game, board,  exploit = False, epsilon=1e-12, conv=False, return_predictions=False):
    # Recibe el modelo con el que se hace la movida
    n_square = game.n**2
    if conv:
        predictions = model.predict(board.reshape(-1, *board.shape, 1))
    else:
        predictions = model.predict(board.reshape(-1, n_square))
    valid_moves = game.getValidMoves(board, 1)
    predictions_ = predictions[0].copy()
    if valid_moves[-1] == 1:
        # No hay movidas válidas
        if return_predictions:
            return n_square, predictions_
        else:
            return n_square
    predictions = (predictions + epsilon) * valid_moves[:-1] 
    
    predictions = predictions/predictions.sum()
    if exploit:
        action = np.argmax(predictions)
    else:
        action = np.random.choice(n_square, p=predictions[0])
    if return_predictions:
        return action, predictions_
    else:
        return action
    
def play_with_full_model(model, game, board,  exploit = False, epsilon=1e-12, conv=False, return_predictions=False):
    # Recibe el modelo con el que se hace la movida
    n_square = game.n**2
    if conv:
        value, predictions = model.predict(board.reshape(-1, *board.shape, 1))
    else:
        value, predictions = model.predict(board.reshape(-1, n_square))
    value = value[0]
    valid_moves = game.getValidMoves(board, 1)
    predictions_ = predictions[0].copy()
    if valid_moves[-1] == 1:
        # No hay movidas válidas
        if return_predictions:
            return n_square, value, predictions_
        else:
            return n_square, value
    predictions = (predictions + epsilon) * valid_moves[:-1] 
    
    predictions = predictions/predictions.sum()
    if exploit:
        action = np.argmax(predictions)
    else:
        action = np.random.choice(n_square, p=predictions[0])
    if return_predictions:
        return action, value, predictions_
    else:
        return action, value
    
def play_episode(players, game, board, return_actions=False, append_last=False, return_predictions=True):
    # No necesita el jugador que comienza por que se resuelve en su forma canonica. 
    # Se ve el juego en la perspectiva de blanco siempre
    # board = game.getCanonicalForm(board, 1)
    states = []
    actions = []
    rewards = []
    predictions = []
    player_turn = 0
    ended = game.getGameEnded(board, 1) 
    while ended == 0:
        states.append(board)
        if return_predictions:
            action, prediction = players[player_turn](game, board, return_predictions=True)
            predictions.append(prediction)
        else:
            action = players[player_turn](game, board)
        actions.append(action)
        board, _ = game.getNextState(board, 1, action)
        board = game.getCanonicalForm(board, -1)
        player_turn = (player_turn + 1) % len(players)
        ended = game.getGameEnded(board, 1) 
        if ended==0:
            rewards.append(0)
        else:
            rewards.append(-np.sign(board.sum()))
    if append_last:
        states.append(board)
    states = np.array(states)
    actions = np.array(actions)
    rewards = np.array(rewards)
    if return_actions and return_predictions:
        predictions = np.array(predictions)
        return states, actions, rewards, predictions
    elif return_actions:
        return states, actions, rewards
    else:
        return states

def play_episode_with_value(players, game, board, return_actions=False, append_last=False, return_predictions=True):
    # No necesita el jugador que comienza por que se resuelve en su forma canonica. 
    # Se ve el juego en la perspectiva de blanco siempre
    # board = game.getCanonicalForm(board, 1)
    states = []
    actions = []
    rewards = []
    values = []
    predictions = []
    player_turn = 0
    ended = game.getGameEnded(board, 1) 
    while ended == 0:
        states.append(board)
        if return_predictions:
            action, value, prediction = players[player_turn](game, board, return_predictions=True)
            predictions.append(prediction)
        else:
            action, value = players[player_turn](game, board)
        actions.append(action)
        values.append(value)
        board, _ = game.getNextState(board, 1, action)
        board = game.getCanonicalForm(board, -1)
        player_turn = (player_turn + 1) % len(players)
        ended = game.getGameEnded(board, 1) 
        if ended==0:
            rewards.append(0)
        else:
            rewards.append(-np.sign(board.sum()))
    if append_last:
        states.append(board)
    states = np.array(states)
    actions = np.array(actions)
    rewards = np.array(rewards)
    values = np.array(values)
    if return_actions and return_predictions:
        predictions = np.array(predictions)
        return states, actions, rewards, values, predictions
    elif return_actions:
        return states, actions, rewards, values
    else:
        return states
    
def play_episodes(model, game, board, episodes=1, conv=True, return_predictions=True, player=1):
    states_ = []
    actions_ = []
    rewards_ = []
    predictions_ = []
    for i in range(episodes):
        states, actions, rewards, predictions = play_episode([lambda game, board, return_predictions: 
                                                              play_with_model(model, game, board, conv=conv, return_predictions=return_predictions), 
                                             lambda game, board, return_predictions: 
                                                              play_with_model(model, game, board, conv=conv, return_predictions=return_predictions)], 
                                            game, board*player, return_actions=True, return_predictions=True)
        states_.append(states)
        actions_.append(actions.reshape(-1, 1))
        rewards_.append(rewards.reshape(-1, 1))
        predictions_.append(predictions)
    return np.vstack(states_), np.vstack(actions_), np.vstack(rewards_), np.vstack(predictions_)
    
def get_discounted_rewards(rewards, gamma=0.99):
    accumulated_rewards = []
    rew = rewards[-1]
    accumulated_rewards.append(rew)
    for i in range(len(rewards)-1):
        rew = rew*-gamma
        accumulated_rewards.append(rew)
    accumulated_rewards=np.array(accumulated_rewards)[::-1]
    return accumulated_rewards
    
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Input, Concatenate, BatchNormalization, Activation, Dropout
from keras.models import Model, Sequential
from keras.optimizers import Adam
import keras.backend as K
from keras.initializers import glorot_uniform
from keras.losses import categorical_crossentropy, binary_crossentropy

def get_policy_model_softmax(lr=0.001, hidden_layer_neurons = 256, input_shape=[16], output_shape=16):
    model = Sequential()
    model.add(Dense(hidden_layer_neurons, input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dense(output_shape, activation='softmax'))
    model.compile(Adam(lr), loss=['categorical_crossentropy'])
    return model

def get_policy_model_softmax_cnn(lr=0.001, filters = 16, filter_size=3, input_shape=[4, 4, 1], output_shape=16):
    model = Sequential()
    model.add(Conv2D(filters, filter_size, input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dense(output_shape, activation='softmax'))
    model.compile(Adam(lr), loss=['categorical_crossentropy'])
    return model

def get_policy_model_softmax_cnn_deep(lr=0.001, do=0.25, input_shape=[4, 4, 1], output_shape=16):
    model = Sequential()
    model.add(Conv2D(16, 2, input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
#     model.add(Dropout(do))
    model.add(Conv2D(32, 2, input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
#     model.add(Dropout(do))
    model.add(Conv2D(64, 2, input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dropout(do))
    model.add(Dense(output_shape, activation='softmax'))
    model.compile(Adam(lr), loss=['categorical_crossentropy'])
    return model

def get_value_model_cnn_deep(lr=0.001, do=0.25, input_shape=[4, 4, 1], output_shape=1):
    model = Sequential()
    model.add(Conv2D(16, 2, input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
#     model.add(Dropout(do))
    model.add(Conv2D(32, 2, input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
#     model.add(Dropout(do))
    model.add(Conv2D(64, 2, input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dropout(do))
    model.add(Dense(output_shape))
    model.compile(Adam(lr), loss=['mse'])
    return model

def get_policy_concat_cnns(lr=0.001, filters = 128, input_shape=[4, 4, 1], output_shape=16):
    x = Input(shape=input_shape)
    x1 = Flatten()(Conv2D(filters, 2, activation='relu')(x))
    x2 = Flatten()(Conv2D(filters, 3, activation='relu')(x))
    x3 = Flatten()(Conv2D(filters, 4, activation='relu')(x))
    concat = Concatenate()([x1, x2, x3])
    out = Dense(output_shape, activation='softmax')(concat)
    model = Model(x, out)
    model.compile(Adam(lr), loss=['categorical_crossentropy'])
    return model

def one_cnn(lr = 0.001, ce_w=1, mse_w=1, input_shape = [4, 4, 1], do = 0.25, output_shape = 16):
    model = Sequential()
    model.add(Conv2D(16, 2))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Conv2D(32, 2))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Conv2D(64, 2))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dropout(do))

    inp = Input(input_shape)
    x = model(inp)
    x_value = Dense(1, name='value')(x)
    x_policy = Dense(output_shape, activation='softmax', name='policy')(x)
    full_model = Model(inp, [x_value, x_policy])

    full_model.compile(Adam(lr), loss={'policy': 'categorical_crossentropy', 'value': 'mse'}, 
                       loss_weights={'policy': ce_w, 'value': mse_w})
    return full_model