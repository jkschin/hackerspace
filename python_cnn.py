import numpy as np

np.random.seed(0)

class Layer(object):
  def _setup(self):
    pass

  def fprop(self, inp):
    raise NotImplementedError()

  def bprop(self, inp_grad):
    raise NotImplementedError()

class Conv(Layer):
  def __init__(self, fil, strides, padding):
    self.fil = np.random.rand(*fil)
    self.strides = np.array(strides)
    self.padding = padding

  def _fprop_preprocess(self, inp):
    N, H, W, C = inp.shape
    FH, FW, IC, OC = self.fil.shape
    SN, SH, SW, SC = self.strides
    if self.padding == 'VALID':
      PH = 0
      PW = 0
    else:
      PH = (H * SH) - 1 - H + FH
      PW = (W * SW) - 1 - W + FW
    ON = N
    OH = (H - FH + PH) / SH + 1
    OW = (W - FW + PW) / SW + 1
    PT = PH / 2
    PB = PH - (PH / 2)
    PL = PW / 2
    PR = PW - (PW / 2)
    padded_inp = np.pad(inp, ((0 , 0), (PT, PB), (PL, PR), (0, 0)), 'constant')
    out = np.zeros((ON, OH, OW, OC), dtype=np.float32)
    return padded_inp, out

  def fprop(self, inp):
    padded_inp, out = self._fprop_preprocess(inp)
    N, H, W, C = padded_inp.shape
    FH, FW, IC, OC = self.fil.shape
    SN, SH, SW, SC = self.strides
    FH_L = -(FH / 2)
    FH_U = FH / 2 + FH % 2
    FW_L = -(FW / 2)
    FW_U = FW / 2 + FW % 2
    for n in xrange(N):
      for h in xrange(FH/2, H - FH/2, SH):
        for w in xrange(FW/2, W - FW/2, SW):
          for c in xrange(OC):
            for fh in xrange(FH_L, FH_U):
              for fw in xrange(FW_L, FW_U):
                for ic in xrange(IC):
                  out[n, h - FH/2 - h / SH, w - FW/2 - w / SW, c] += \
                    self.fil[fh, fw, ic, c] * \
                    padded_inp[n, h - fh, w - fw, ic]
    self.inp = inp
    self.out = out
    return out

  def _bprop_preprocess(self, inp_grad):
    N, H, W, C = inp_grad.shape


  def bprop(self, inp_grad):
    inv_fil = np.flip(np.flip(self.fil, 1), 2)
    SN, SH, SW, SC = self.strides


  # def bprop(self, inp_grad):
  #   inv_fil = np.flip(np.flip(self.fil, 1), 2)
  #   out_grad = self.convolution(inp_grad, inv_fil)
  #   self.inp_grad = inp_grad
  #   self.out_grad = out_grad

  # def update(self):
  #   gradients = np.zeros((self.fil.shape), dtype=np.float32)
  #   N, H, W, C = self.inp_grad.shape
  #   FH, FW, IC, OC = self.fil.shape
  #   for oc in xrange(OC):
  #     inp_grad_per_channel = self.inp_grad[:, :, :, oc]
  #     broadcasted = np.broadcast_to(inp_grad_per_channel, (N, H, W, IC))
  #     gradients_per_channel = self.convolution(self.inp, self.inp_grad)
  #     gradients[:, :, :, oc] = gradients_per_channel

# a = np.ones((10, 6, 6, 3))

# conv1 = Conv((2, 2, 3, 32), (1, 2, 2, 1), 'VALID')
# conv1.fprop(a)
# print conv1.out.shape
# conv1.bprop(a)
# print conv1.out.shape
# print conv1.out_grad.shape
# print conv1.inp.shape
# print conv1.out.shape








