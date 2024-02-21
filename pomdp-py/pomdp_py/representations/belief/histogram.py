from pomdp_py.representations.distribution.histogram import Histogram
import maps
from pomdp_py.problems.multi_object_search.domain.state import ObjectState

def abstraction_over_histogram(current_histogram, state_mapper):
    state_mappings = {s: state_mapper(s) for s in current_histogram}
    hist = {}
    for s in current_histogram:
        a_s = state_mapper(s)
        if a_s not in hist[a_s]:
            hist[a_s] = 0
        hist[a_s] += current_histogram[s]
    return hist

def count_times(pos, obj):
    count = 0
    for dispid in range(len(maps.dispositions)):
        analyze_pos = maps.dispositions[dispid][obj]
        #print(analyze_pos)
        if pos == (analyze_pos[0], analyze_pos[1]):
            count += 1
    return count

def update_histogram_belief(
    beliefs,
    objid,
    real_action,
    real_observation,
    observation_model,
    transition_model,
    oargs={},
    targs={},
    normalize=True,
    static_transition=False,
    next_state_space=None
):
    """
    update_histogram_belief(current_histogram, real_action, real_observation,
                            observation_model, transition_model, oargs={},
                            targs={}, normalize=True, deterministic=False)
    This update is based on the equation:
    :math:`B_{new}(s') = n O(z|s',a) \sum_s T(s'|s,a)B(s)`.

    Args:
        current_histogram (~pomdp_py.representations.distribution.Histogram)
            is the Histogram that represents current belief.
        real_action (~pomdp_py.framework.basics.Action)
        real_observation (~pomdp_py.framework.basics.Observation)
        observation_model (~pomdp_py.framework.basics.ObservationModel)
        transition_model (~pomdp_py.framework.basics.TransitionModel)
        oargs (dict) Additional parameters for observation_model (default {})
        targs (dict) Additional parameters for transition_model (default {})
        normalize (bool) True if the updated belief should be normalized
        static_transition (bool) True if the transition_model is treated as static;
            This basically means Pr(s'|s,a) = Indicator(s' == s). This then means
            that sum_s Pr(s'|s,a)*B(s) = B(s'), since s' and s have the same state space.
            This thus helps reduce the computation cost by avoiding the nested iteration
            over the state space; But still, updating histogram belief requires
            iteration of the state space, which may already be prohibitive.
        next_state_space (set) the state space of the updated belief. By default,
            this parameter is None and the state space given by current_histogram
            will be directly considered as the state space of the updated belief.
            This is useful for space and time efficiency in problems where the state
            space contains parts that the agent knows will deterministically update,
            and thus not keeping track of the belief over these states.

    Returns:
        Histogram: the histogram distribution as a result of the update
    """
    probabilities_mul = []
    if next_state_space is None:
        next_state_space = beliefs[objid]
    for next_state in next_state_space:
        observation_prob = observation_model.probability(
            real_observation, next_state, real_action, **oargs
        )
        probabilities_mul.append(observation_prob)

    """
    for obj in beliefs:
        print("DEBUGX", beliefs[obj], obj)
        new_histogram = {}  # state space still the same.
        total_prob = 0
        for x, next_state in enumerate(beliefs[obj]):
            new_histogram[next_state] = beliefs[obj][next_state] * probabilities_mul[x]
            total_prob += new_histogram[next_state]
        print("DEBUG1", new_histogram)
    """
    # print("DEBUG",beliefs)
    for x, next_state in enumerate(beliefs[objid]):
        # print("DEBUG", next_state) # ObjectState(target,(6, 0))
        disp_involved = []
        for disp in range(len(maps.dispositions)):
            # print(next_state.pose, next_state.objid)
            pos = maps.dispositions[disp][next_state.objid]
            if next_state.pose == (pos[1], pos[0]):
                disp_involved.append(disp)
        # print("DEBUG", disp_involved) # ci stampa l'indice delle disposizioni di cui dobbiamo modificare le probabilità
        
       
        for obj in range(len(maps.dispositions[0])):
            #print(obj)
            new_histogram = {}
            for obj_bel in beliefs[obj]:
                new_histogram[obj_bel] = beliefs[obj][obj_bel]
            #print(new_histogram)
            """
            for disp in range(len(maps.dispositions)):
                new_histogram =  {} # state space still the same.
                total_prob = 0
                state = ObjectState(, "target", (pos[1], pos[0]))
                new_histogram[state] = beliefs[obj]
            """

            #1 2 3 1 4 1 5
            #1 2 3 4 5

            change = [False] * len(maps.dispositions)
            for dispid in disp_involved:
                pos = maps.dispositions[dispid][obj]
                state = ObjectState(obj, "target", (pos[1], pos[0]))
                if probabilities_mul[x] != 1e-100:
                    change[disp] = True
                if count_times(pos, obj) > 1 and probabilities_mul[x] == 1e-100:
                    pass
                else:
                    new_histogram[state] = beliefs[obj][state] * probabilities_mul[x]
                #if maps.disposition[disp][]
                #new_histogram[next_state] = beliefs[obj][next_state] * probabilities_mul[x]
                #total_prob += new_histogram[state]
                # print("DEBUG1", new_histogram)
            #for ele in range(len(change)):
            #    if not change[ele]
            total_prob = 0.0
            for state in new_histogram:
                #print("DEV", state, new_histogram[state])
                total_prob += new_histogram[state]
            #print()
            #  Normalize
            if normalize:
                for state in new_histogram:
                    if total_prob > 0:
                        new_histogram[state] /= total_prob
            #print("DEBUG", new_histogram, probabilities_mul[x])
            beliefs[obj] = Histogram(new_histogram)
    #print(beliefs, len(beliefs))
    return beliefs
