import itertools
import numpy as np
"""
What, Where.
"""

class DiscreteStateSpace:
    ''' Discrete State Space specification class '''

    def __init__(self, *args):
        self.n_dims = len(args)
        self.limits = args
        self.n_states = np.product(self.limits)
        self.idxs = self._get_idxs()
        self.space = self._get_space()
        self.state_lst, self.loc_to_state_dict, self.state_to_loc_dict, self.loc_to_idx_dict = self._get_states()
        self.T = None

    def _get_idxs(self):
        return np.arange(self.n_states).reshape(self.limits)

    def _get_space(self):
        return np.array(list(itertools.product(*[np.arange(lim) for lim in self.limits]))).reshape(
            self.limits + (self.n_dims,))

    def _get_states(self):

        state_list = []
        loc_to_state_dict = {}
        state_to_loc_dict = {}
        loc_to_idx_dict = {}
        idx = 0
        for loc in list(itertools.product(*[np.arange(lim) for lim in self.limits])):
            state = State(location=loc, idx=idx)
            state_list.append(state)
            loc_to_state_dict[loc] = state
            state_to_loc_dict[state] = loc
            loc_to_idx_dict[loc] = idx
            idx += 1
        return state_list, loc_to_state_dict, state_to_loc_dict, loc_to_idx_dict

    def __str__(self):
        #return "".join(str(s) if ((idx+1) % self.limits[-1] != 0) else str(s) + "\n" for idx, s in enumerate(self.states_lst))
        return str(self.space)

    def print_states_meta(self):
        for s in self.state_lst:
            print(s._meta())

    def at_loc(self, loc):
        return self.loc_to_state_dict[loc]

    def __call__(self, idx=None):
        if idx is None:
            return self.state_lst
        else:
            return self.__getitem__(idx)

    def __getitem__(self, idx):
        if type(idx) == tuple:
            return self.at_loc(loc=idx)
        else:
            return self.state_lst[idx]

    def __len__(self):
        return self.n_states

    def all(self):
        return self.state_lst

    def attach_classes(self, class_ids=[]):
        if len(class_ids) != self.n_states:
            raise Exception("Require class id for each state!")
        self.n_classes = len(np.unique(class_ids))
        for idx, class_id in enumerate(class_ids):
            self.state_lst[idx].attach_class(class_id)

    def sample_and_attach_classes(self, class_ids=[], p_dist=None):
        S = class_ids
        if p_dist is None:
            p_dist = np.ones(len(S)) / len(S)
        if len(p_dist) != len(class_ids):
            raise Exception("class_ids and p_dist must have same length!")
        self.uniq_classes = class_ids
        class_ids = np.random.choice(S, self.n_states, p=p_dist) #.reshape(self.limits)
        for idx, class_id in enumerate(class_ids):
            self.state_lst[idx].attach_class(class_id)

    def override_classes_by_loc(self, loc_lst, class_id_lst):
        for i, loc in enumerate(loc_lst):
            self.loc_to_state_dict[loc].attach_class(class_id_lst[i])
        self.uniq_classes = np.unique(self.class_ids)

    @property
    def class_ids(self):
        return np.asarray([self.state_lst[idx].get_class() for idx in range(self.n_states)])

    @property
    def num_classes(self):
        return len(self.uniq_classes)

    def attach_features(self, PHI_spec):
        self.PHI_spec = PHI_spec
        for idx, features in enumerate(self.PHI_spec.get_all_features()):
            self.state_lst[idx].attach_features(features)

    def features(self, loc=None, idx=None, gridded=False):
        if loc is not None:
            return np.asarray(self.loc_to_state_dict[loc].get_features())
        elif idx is not None:
            return np.asarray(self.state_lst[idx].get_features())
        else:
            features_lst = np.asarray([self.state_lst[idx].get_features() for idx in range(self.n_states)])
            if gridded:
                return features_lst.reshape(self.limits + self.feature_dim)
            else:
                return features_lst

    @property
    def feature_dim(self):
        return self.features(idx=0).shape

    def attach_rewards(self, R_spec):
        self.R_spec = R_spec
        for idx, reward in enumerate(self.R_spec.get_reward_lst()):
            self.state_lst[idx].attach_reward(reward)

    def rewards(self, gridded=False):
        rewards = np.asarray([self.state_lst[idx].get_reward() for idx in range(self.n_states)], dtype=np.float32)
        if gridded:
            return rewards.reshape(*self.limits, 1)
        else:
            return rewards

    def set_terminal_status_by_loc(self, loc_lst, b_terminal_status=True):
        for loc in loc_lst:
            self.loc_to_state_dict[loc].set_terminal_status(b_terminal_status)

    def set_terminal_status_by_idx(self, idx_lst, b_terminal_status=True):
        for idx in idx_lst:
            self.state_lst[idx].set_terminal_status(b_terminal_status)

    def get_terminal_states(self):
        return [s for s in self.state_lst if s.terminal_status is True]

    def reset_terminal_status(self):
        for s in self.state_lst:
            s.set_terminal_status(False)

    def _organize_to_grid(self, values):
        return np.asarray(values).reshape(self.limits + values[0].shape)


class State(object):
    ''' State specification class
    Adapted from https://github.com/david-abel/simple_rl/simple_rl/mdp/StateClass.py
    '''

    def __init__(self, location, idx=None,
                 class_id=None, features=None,
                 reward=None, terminal_status=False):
        self.location = location
        self.idx = idx
        self.class_id = class_id
        self.features = features
        self.reward = reward
        self.terminal_status = terminal_status

    def get_idx(self):
        return self.idx

    def get_id(self):
        return self.location

    def get_location(self):
        return self.location

    def get_class(self):
        return self.class_id

    def get_features(self):
        return self.features

    def get_reward(self):
        return self.reward

    def is_terminal(self):
        return self.terminal_status

    def attach_class(self, class_id):
        self.class_id = class_id

    def attach_features(self, features):
        self.features = features

    def attach_reward(self, reward):
        self.reward = reward

    def set_terminal_status(self, b_terminal_status):
        self.terminal_status = b_terminal_status

    def __hash__(self):
        if type(self.location).__module__ == np.__name__:
            # Numpy arrays
            return hash(str(self.location))
        elif self.location.__hash__ is None:
            return hash(tuple(self.location))
        else:
            return hash(self.location)

    def __str__(self):
        return "State: " + str(self.location)

    def _meta(self):
        return "State: " + str(self.location) + " [ "+ \
               ("C {} ".format(self.get_class()) if self.get_class() is not None else "") + \
               ("R {:.2f} ".format(self.get_reward()) if self.get_reward() is not None else "") + \
               ("phi {} ".format(self.get_features().shape) if self.get_features() is not None else "") + \
               ("Terminal " if self.is_terminal() else "") + \
                "]"

    def __repr__(self):
        return str(self.__module__) + "." + self.__class__.__name__ + str(self.location) + " at " + hex(id(self))

    def __eq__(self, other):
        if isinstance(other, State):
            return self.location == other.location
        return False

    def __getitem__(self, index):
        return self.location[index]

    def __len__(self):
        return len(self.location)