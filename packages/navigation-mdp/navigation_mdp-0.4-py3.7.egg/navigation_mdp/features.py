import numpy as np
from navigation_mdp.utils import one_hot_nd
"""
Why.
"""

class AbstractStateFeature:

    def __init__(self, state_space):
        self.state_space = state_space
        self.features_lst = None

    def __call__(self, loc=None, idx=None, gridded=False):
        if loc is not None:
            return self.get_features_at_loc(loc)
        elif idx is not None:
            return self.get_features_at_idx(idx)
        else:
            if gridded:
                return self.get_all_features().reshape(self.state_space.limits + self.features_lst.shape[1:])
            else:
                return self.get_all_features()

    def __getitem__(self, idx):
        return self.get_features_at_idx(idx)

    def __len__(self):
        return len(self.features_lst)

    def get_all_features(self):
        return self.features_lst

    def get_features_at_idx(self, idx):
        return self.features_lst[idx]

    def get_features_at_loc(self, loc):
        return self.features_lst[self.state_space.loc_to_idx_dict[loc]]


class FeatureStateIndicator(AbstractStateFeature):

    def __init__(self, state_space):
        super().__init__(state_space)
        self.features_lst = self.state_space.idxs.flatten()


class FeatureStateIndicatorOneHot(AbstractStateFeature):

    def __init__(self, state_space):
        super().__init__(state_space)
        self.features_lst = one_hot_nd(self.state_space.idxs.flatten(), N=self.state_space.n_states)


class FeatureClassIndicator(AbstractStateFeature):

    def __init__(self, state_space):
        super().__init__(state_space)
        self.features_lst = self.state_space.class_ids


class FeatureClassIndicatorOneHot(AbstractStateFeature):

    def __init__(self, state_space, K=None):
        super().__init__(state_space)
        max_class_id = max(self.state_space.class_ids) if K is None else K
        self.features_lst = one_hot_nd(self.state_space.class_ids, N=max_class_id + 1)


class FeatureClassImage(AbstractStateFeature):

    def __init__(self, state_space, feature_map):
        super().__init__(state_space)
        self.features_lst = np.asarray([feature_map[clsid] for clsid in self.state_space.class_ids.flatten()])


class FeatureClassImageSampler(AbstractStateFeature):

    def __init__(self, state_space, feature_sampler):
        super().__init__(state_space)
        self.features_lst = np.asarray([feature_sampler(clsid) for clsid in self.state_space.class_ids.flatten()])


class ImageDiscretizer:
    def __init__(self, img, h_cells, w_cells, aug_cells=(0,0)):
        assert len(img.shape) == 3
        self.h_cells = h_cells
        self.w_cells = w_cells
        self.aug_cell_cnt_h, self.aug_cell_cnt_w = aug_cells
        self.cell_height = int(img.shape[0] // self.h_cells)
        self.cell_width = int(img.shape[1] // self.w_cells)
        self.img_clipped = img[:self.cell_height * self.h_cells, :self.cell_width * self.w_cells]
        self.img_clipped = np.pad(self.img_clipped,
                                  ((self.aug_cell_cnt_h*self.cell_height, self.aug_cell_cnt_h*self.cell_height),
                                   (self.aug_cell_cnt_w*self.cell_width, self.aug_cell_cnt_w*self.cell_width), (0,0)),
                                  mode="constant", constant_values=0)
        print("Note: image clipped to: {}".format(self.img_clipped.shape))
        self.img_lst = self._create_img_grid()
        self.idxs = np.arange(h_cells * w_cells).tolist()

    def _create_img_grid(self):
        img_lst = []
        for i in range(self.h_cells):
            img_lst.append([])
            for j in range(self.w_cells):
                img_lst[-1].append(self.img_clipped[ (i) * self.cell_height: (i +  2*self.aug_cell_cnt_h + 1) * self.cell_height,
                                   (j) * self.cell_width: (j + 2*self.aug_cell_cnt_w + 1) * self.cell_width])
        return np.asarray(img_lst)

    def get_raw_image(self):
        return self.img_clipped

    def get_image_grid(self):
        return self.img_lst

    def get_image_cell(self, row, col):
        return self.img_lst[row][col]

    def __call__(self):
        return self.get_image_grid()


class FeatureStateIdxImage(AbstractStateFeature):

    def __init__(self, state_space, state_idx_to_image_fn):
        super().__init__(state_space)
        self.features_lst = np.asarray([
            state_idx_to_image_fn(state_idx) for state_idx in self.state_space.idxs.flatten()])

class FeatureStateLocImage(AbstractStateFeature):

    def __init__(self, state_space, state_loc_to_image_fn):
        super().__init__(state_space)
        self.features_lst = np.asarray(
            [state_loc_to_image_fn(*state.location) for state in self.state_space])
