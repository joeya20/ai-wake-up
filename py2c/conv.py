import numpy as np

def conv_layer(x, W, b, stride=1, pad=0):
    # Apply padding to the input to maintain spatial dimensions
    x_padded = np.pad(x, ((0, 0), (0, 0), (pad, pad), (pad, pad)), mode='constant', constant_values=0)
    filter_height, filter_width,_,num_filters = W.shape
    batch_size, num_channels, height, width = x.shape

    # Output dimensions
    out_height = (height + 2*pad - filter_height) // stride + 1
    out_width = (width + 2*pad - filter_width) // stride + 1
    out = np.zeros((batch_size, num_filters, out_height, out_width))

    for n in range(batch_size):
        for f in range(num_filters):
            for i in range(out_height):
                for j in range(out_width):
                    vert_start = i * stride
                    vert_end = vert_start + filter_height
                    horiz_start = j * stride
                    horiz_end = horiz_start + filter_width

                    # Extract the slice for the current convolution operation
                    x_slice = x_padded[n, :, vert_start:vert_end, horiz_start:horiz_end]

                    # Compute the convolution output (element-wise multiplication and sum)
                    #print(x_slice.shape)
                    #print(W[:,:,:,f].shape)
                    #print(b[f].shape)
                    out[n, f, i, j] = np.sum(x_slice * W[:, :, :, f].transpose(2,0,1)) + b[f]
    return out

