import numpy as np
import torch
import torch.utils.data


def paired_collate_fn(insts):
    """ This function creates mini-batches (4-tuples) of src_seq/pos,
        trg_seq/pos Tensors. insts is a list of tuples, each containing one src
        and one target seq.
        """
    src_insts, tgt_insts = list(zip(*insts))
    src_insts = collate_fn(src_insts)
    tgt_insts = collate_fn(tgt_insts, is_tgt=True)
    return (*src_insts, *tgt_insts)

def collate_fn(insts, is_tgt=False):
    ''' Pad the instance to the max seq length in batch '''

    max_len = max(len(inst) for inst in insts)

    if is_tgt:
        pad_dim = 22
    else:
        pad_dim = 20
    batch_seq = np.array([
        np.concatenate((inst, np.zeros((max_len - len(inst), pad_dim))), axis=0)
        for inst in insts])

    batch_pos = np.array([
        [pos_i+1 if w_i.any() else 0
         for pos_i, w_i in enumerate(inst)] for inst in batch_seq]) # position arr

    if is_tgt:
        batch_seq = torch.FloatTensor(batch_seq)
    else:
        batch_seq = torch.FloatTensor(batch_seq)
    batch_pos = torch.LongTensor(batch_pos)


    return batch_seq, batch_pos

class ProteinDataset(torch.utils.data.Dataset):
    def __init__(
        self, seqs=None, angs=None):

        assert seqs is not None
        assert (angs is None) or (len(seqs) == len(angs))

        self._seqs = seqs
        self._angs = angs

    @property
    def n_insts(self):
        ''' Property for dataset size '''
        return len(self._seqs)

    def __len__(self):
        return self.n_insts

    def __getitem__(self, idx):
        if self._angs is not None:
            return self._seqs[idx], self._angs[idx]
        return self._seqs[idx]
