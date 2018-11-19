'''
Illustration

channels = 3
height = 5
width = 5
ksize = 3
stride = 2
pad = 1

Run code below to print im2col in col order.

Image Channel 1:
  X   X   X   X   X   X   X
  X   0   1   2   3   4   X
  X   5   6   7   8   9   X
  X   10  11  12  13  14  X
  X   15  16  17  18  19  X
  X   20  21  22  23  24  X
  X   X   X   X   X   X   X

Image Channel 2:
  X   X   X   X   X   X   X
  X   25  26  27  28  29  X
  X   30  31  32  33  34  X
  X   35  36  37  38  39  X
  X   40  41  42  43  44  X
  X   45  46  47  48  49  X
  X   X   X   X   X   X   X

Image Channel 3:
  X   X   X   X   X   X   X
  X   50  51  52  53  54  X
  X   55  56  57  58  58  X
  X   60  61  62  63  64  X
  X   65  66  67  68  69  X
  X   70  71  72  73  74  X
  X   X   X   X   X   X   X

im2col converts the image into a col, which can then be reshaped to a matrix.
The weights are already stored in a col, which are reshaped to a matrix.

Let the Weight Matrix be A, corresponding with forward_convolutional_layer in
darknet/src/convolutional_layer.c Line 449.

Let the Input Image be B, corresponding with Line 450.

The parameters M K N are from Lines 444 to 446. The same parameters M K N are
used in cuBLAS API, reproduced below:
http://docs.nvidia.com/cuda/cublas/index.html#cublas-lt-t-gt-gemm

cublasStatus_t cublasSgemm(cublasHandle_t handle,
                           cublasOperation_t transa, cublasOperation_t transb,
                           int m, int n, int k,
                           const float           *alpha,
                           const float           *A, int lda,
                           const float           *B, int ldb,
                           const float           *beta,
                           float           *C, int ldc)

Note that this format is exactly the same as the gemm operations in
darknet/src/gemm.c

A has shape M x K, where M is the number of convolutional filters, K is S*S*C,
where S is the kernel size and C is the number of channels in the input.

B has shape K x N, where K is the same value as the K above, and N is
output_height * output_width

With that, the columns are reshaped into a matrix multiply and the resulting
matrix multiply looks like this:

Matrix A
F1_W1 F1_W2 F1_W3 ... F1_W26 F1_W27
F2_W1 F2_W2 F2_W3 ... F2_W26 F2_W27

Matrix B
X   X   X   X   6   8   X   16  18
X   X   X   5   7   9   15  17  19
X   X   X   6   8   X   16  18  X
X   1   3   X   11  13  X   21  23
...
X   56  58  X   66  68  X   X   X
55  57  59  65  67  69  X   X   X
56  58  X   66  68  X   X   X   X

As you can see, reading down Matrix B column wise is taking a patch from all
channels.

When these 2 matrices are multiplied, a H*W*N matrix is obtained.
'''

def im2col_get_pixel(height, width, channels, row, col, channel, pad):
  row -= pad
  col -= pad
  if (row < 0 or col < 0 or row >= height or col >= width):
    return 'INVALID'
  else:
    # print col, width, row, height, channel
    return col + width*(row + height*channel)

def im2col_cpu(channels, height, width, ksize, stride, pad):
  height_col = (height + 2*pad - ksize) / stride + 1
  width_col = (width + 2*pad - ksize) / stride + 1
  channels_col = channels * ksize * ksize
  for c in xrange(channels_col):
    w_offset = c % ksize
    h_offset = (c / ksize) % ksize
    c_im = c / ksize / ksize
    for h in xrange(height_col):
      for w in xrange(width_col):
        im_row = h_offset + h * stride
        im_col = w_offset + w * stride
        col_index = (c * height_col + h) * width_col + w
        im_index = im2col_get_pixel(height, width, channels, im_row, im_col,
            c_im, pad)
        print col_index, im_index

channels = 3
height = 5
width = 5
ksize = 3
stride = 2
pad = 1
im2col_cpu(channels, height, width, ksize, stride, pad)

