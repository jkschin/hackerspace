import math
import numpy as np

np.random.seed(0)

# Referenced from TensorFlow tf.nn.convolution

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

  def fprop(self, inp):
    IN, IH, IW, IC = inp.shape
    SN, SH, SW, SC = self.strides
    FH, FW, FIC, FOC = self.fil.shape
    assert IC == FIC
    if self.padding == 'SAME':
      OH = int(math.ceil(float(IH) / SH))
      OW = int(math.ceil(float(IW) / SW))
      PH = max((OH - 1) * SH + FH - IH, 0)
      PW = max((OW - 1) * SW + FW - IW, 0)
    elif self.padding == 'VALID':
      OH = int(math.ceil(float(IH - FH + 1) / SH))
      OW = int(math.ceil(float(IW - FW + 1) / SW))
      PH = 0
      PW = 0
    PT = PH / 2
    PB = PH - PT
    PL = PW / 2
    PR = PW - PL
    out = np.zeros((IN, OH, OW, FOC), dtype=np.float32)
    for n in xrange(IN):
      for h in xrange(OH):
        for w in xrange(OW):
          for c in xrange(FOC):
            for fh in xrange(FH):
              for fw in xrange(FW):
                for ic in xrange(IC):
                  i = SH * h + fh - PT
                  j = SW * w + fw - PL
                  if i < 0 or j < 0 or i >= IH or j >= IW:
                    continue
                  else:
                    val = inp[n, i, j, ic]
                  out[n, h, w, c] += \
                      self.fil[fh, fw, ic, c] * val
    self.inp = inp
    self.out = out
    return out

  def bprop(self, inp_grad):
    ON, OH, OW, OC = self.inp.shape
    IN, IH, IW, IC = inp_grad.shape
    SN, SH, SW, SC = self.strides
    FH, FW, FIC, FOC = self.fil.shape
    fil = np.flip(np.flip(self.fil, 1), 2)
    if self.padding == 'SAME':
      PH = max((OH - 1) * SH + FH - IH, 0)
      PW = max((OW - 1) * SW + FW - IW, 0)
    elif self.padding == 'VALID':
      PH = 0
      PW = 0
    PT = PH / 2
    PB = PH - PT
    PL = PW / 2
    PR = PW - PL
    out_grad = np.zeros((IN, OH, OW, OC), dtype=np.float32)
    for n in xrange(IN):
      for h in xrange(IH):
        for w in xrange(IW):
          for ic in xrange(IC):
            for fh in xrange(FH):
              for fw in xrange(FW):
                for oc in xrange(OC):
                  i = SH * h + fh - PT
                  j = SW * w + fw - PL
                  if i < 0 or j < 0 or i >= OH or j >= OW:
                    continue
                  else:
                    # NOTE
                    # the ic and oc convention here may be very confusing
                    # because it's now inverted.
                    out_grad[n, i, j, oc] += \
                    fil[fh, fw, oc, ic] * inp_grad[n, h, w, ic]
    self.inp_grad = inp_grad
    self.out_grad = out_grad
    return out_grad

a = np.ones((1, 6, 6, 3))
b = np.ones((1, 4, 4, 1))

conv1 = Conv((3, 3, 3, 1), (1, 1, 1, 1), 'VALID')
conv1.fprop(a)
# print conv1.out.shape
# print conv1.out
conv1.bprop(b)
# print conv1.out_grad.shape
print conv1.out_grad
# print conv1.out.shape
# print conv1.out_grad.shape
# print conv1.inp.shape
# print conv1.out.shape









