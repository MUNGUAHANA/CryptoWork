def shift_row(state, nb_bytes):
    for i in range(1, nb_bytes):
        state[i:] = state[i:] + state[:i]
        return state 
    # Exemple d'utilisation 
    state = [0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff] 
    #state = [64, 2E, 81, 6C, E7, C1, 3D, 86, 28, 8B, 41, 68, 87, C2, 24, DF]
    nb_bytes = 2
    state_shifted = shift_row(state, nb_bytes)
    print("State shifted: ", state_shifted)