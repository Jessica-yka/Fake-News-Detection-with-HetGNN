import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from args import read_args
import numpy as np
import string
import re
import math
args = read_args()


def cross_entropy_loss(c_embed_batch, pos_embed_batch, neg_embed_batch, embed_d):

	batch_size = c_embed_batch.shape[0] * c_embed_batch.shape[1]
    # make c_embed 3D tensor. Batch_size * 1 * embed_d
    # c_embed[0] = 1 * embed_d
	c_embed = c_embed_batch.view(batch_size, 1, embed_d)
	pos_embed = pos_embed_batch.view(batch_size, embed_d, 1)
	neg_embed = neg_embed_batch.view(batch_size, embed_d, 1)
    
    # c_embed, pos_embed, and neg_embed are all finalized output embedding vectors.
    # torch.bmm is a matrix product computation
    # If input is a (b×n×m) tensor, mat2 is a (b×m×p) tensor, output will be a (b×n×p) tensor.
	out_p = torch.bmm(c_embed, pos_embed) # positive neighbors
	out_n = - torch.bmm(c_embed, neg_embed) # negative neighbors

	sum_p = F.logsigmoid(out_p) #log(1/(1+exp(-x)))    sigmoid = 1/(1+exp(-x))
	sum_n = F.logsigmoid(out_n)
	loss_sum = - (sum_p + sum_n)

	#loss_sum = loss_sum.sum() / batch_size

	return loss_sum.mean()
