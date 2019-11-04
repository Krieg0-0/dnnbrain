import os
import h5py
import unittest
import numpy as np

from os.path import join as pjoin
from dnnbrain.io.fileio import StimulusFile, ActivationFile

DNNBRAIN_TEST = pjoin(os.environ['DNNBRAIN_DATA'], 'test')
TMP_DIR = pjoin(os.path.expanduser('~'), '.dnnbrain_tmp')
if not os.path.isdir(TMP_DIR):
    os.makedirs(TMP_DIR)


class TestStimulusFile(unittest.TestCase):

    def test_read(self):

        # ground truth
        stim_type = 'image'
        stim_title = 'ImageNet images in all 5000scenes runs of sub-CSI1_ses-01'
        stim_id = ['n01930112_19568.JPEG', 'n03733281_29214.JPEG']
        stim_rt = [3.6309, 4.2031]

        # load by StimulusFile.read()
        stim_file = pjoin(DNNBRAIN_TEST, 'image', 'sub-CSI1_ses-01_imagenet.stim.csv')
        stim = StimulusFile(stim_file).read()

        # compare
        self.assertEqual(stim['type'], stim_type)
        self.assertEqual(stim['title'], stim_title)
        self.assertEqual(stim['data']['stimID'][:2].tolist(), stim_id)
        self.assertEqual(stim['data']['RT'][:2].tolist(), stim_rt)

    def test_write(self):

        # ground truth
        type = 'video'
        path = 'video_file'
        title = 'video stimuli'
        data = {'stimID': [1, 3, 5]}

        # save by StimulusFile.write()
        fname = pjoin(TMP_DIR, 'test.stim.csv')
        StimulusFile(fname).write(type, path, data, title=title)

        # compare
        stim_dict = StimulusFile(fname).read()
        self.assertEqual(stim_dict['type'], type)
        self.assertEqual(stim_dict['path'], path)
        self.assertEqual(stim_dict['title'], title)
        self.assertEqual(stim_dict['data']['stimID'].tolist(), data['stimID'])


class TestActivationFile(unittest.TestCase):

    def test_read(self):

        # read file
        fpath = pjoin(DNNBRAIN_TEST, "image", "sub-CSI1_ses-01_imagenet.act.h5")
        test_read = ActivationFile(fpath).read()
        rf = h5py.File(fpath, 'r')

        # assert
        self.assertTrue(np.all(test_read['conv5']['raw_shape'] ==
                               rf['conv5'].attrs['raw_shape']))
        self.assertTrue(np.all(test_read['conv5']['data'] ==
                               np.array(rf['conv5'])))
        self.assertTrue(np.all(test_read['fc3']['raw_shape'] ==
                               rf['fc3'].attrs['raw_shape']))
        self.assertTrue(np.all(test_read['fc3']['data'] ==
                               np.array(rf['fc3'])))
        rf.close()

    def test_write(self):

        # prepare dictionary
        fpath = pjoin(TMP_DIR, 'test.act.h5')
        act = np.random.randn(2, 3)
        raw_shape = act.shape
        layers = ['conv4', 'fc2']
        act_dict = {layers[0]: {'data': act, 'raw_shape': raw_shape},
                    layers[1]: {'data': act, 'raw_shape': raw_shape}}

        # write
        ActivationFile(fpath).write(act_dict)

        # compare
        rf = ActivationFile(fpath).read()
        self.assertTrue(np.all(rf[layers[0]]['data'] ==
                               np.array(act)))
        self.assertTrue(np.all(rf[layers[0]]['raw_shape'] ==
                               np.array(raw_shape)))


class TestMaskFile(unittest.TestCase):

    def test_read(self):
        pass

    def test_write(self):
        pass


if __name__ == '__main__':
    unittest.main()
