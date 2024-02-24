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
        if pos == analyze_pos: #(analyze_pos[1], analyze_pos[0]):
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
    r"""
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
        probabilities_mul.append((observation_prob, next_state.objid, next_state.pose))
    
    for mul in probabilities_mul:
        if mul[0] != 1.0:
            for dispid in range(len(maps.dispositions)):
                pos = maps.dispositions[dispid][mul[1]]
                if (pos[1], pos[0]) == mul[2]:
                    for id, element in enumerate(maps.dispositions[dispid]):
                        if count_times(element, id) == 1 or (element[1], element[0]) == mul[2] or mul[0] == 1e100:
                            state = ObjectState(id, "target", (element[1], element[0]))
                            beliefs[id][state] = beliefs[id][state] * mul[0]

    #  Normalize
    if normalize:
        for obj in beliefs:
            total_prob = 0
            for state in beliefs[obj]:
                total_prob += beliefs[obj][state]
            for state in beliefs[obj]:
                if total_prob > 0:
                    beliefs[obj][state] /= total_prob
    return beliefs
