
from .modelBase import ModelBase
import   monai.networks.nets.dynunet as dynunet 

class dynunet_wrapper(ModelBase):
    """
    More info: https://docs.monai.io/en/stable/_modules/monai/networks/nets/dynunet.html#DynUNet

    Args:
        spatial_dims: number of spatial dimensions.
        in_channels: number of input channels.
        out_channels: number of output channels.
        kernel_size: convolution kernel size.
        strides: convolution strides for each blocks.
        upsample_kernel_size: convolution kernel size for transposed convolution layers. The values should
            equal to strides[1:].
        filters: number of output channels for each blocks. Different from nnU-Net, in this implementation we add
            this argument to make the network more flexible. As shown in the third reference, one way to determine
            this argument is like:
            ``[64, 96, 128, 192, 256, 384, 512, 768, 1024][: len(strides)]``.
            The above way is used in the network that wins task 1 in the BraTS21 Challenge.
            If not specified, the way which nnUNet used will be employed. Defaults to ``None``.
        dropout: dropout ratio. Defaults to no dropout.
        norm_name: feature normalization type and arguments. Defaults to ``INSTANCE``.
            `INSTANCE_NVFUSER` is a faster version of the instance norm layer, it can be used when:
            1) `spatial_dims=3`, 2) CUDA device is available, 3) `apex` is installed and 4) non-Windows OS is used.
        act_name: activation layer type and arguments. Defaults to ``leakyrelu``.
        deep_supervision: whether to add deep supervision head before output. Defaults to ``False``.
            If ``True``, in training mode, the forward function will output not only the final feature map
            (from `output_block`), but also the feature maps that come from the intermediate up sample layers.
            In order to unify the return type (the restriction of TorchScript), all intermediate
            feature maps are interpolated into the same size as the final feature map and stacked together
            (with a new dimension in the first axis)into one single tensor.
            For instance, if there are two intermediate feature maps with shapes: (1, 2, 16, 12) and
            (1, 2, 8, 6), and the final feature map has the shape (1, 2, 32, 24), then all intermediate feature maps
            will be interpolated into (1, 2, 32, 24), and the stacked tensor will has the shape (1, 3, 2, 32, 24).
            When calculating the loss, you can use torch.unbind to get all feature maps can compute the loss
            one by one with the ground truth, then do a weighted average for all losses to achieve the final loss.
        deep_supr_num: number of feature maps that will output during deep supervision head. The
            value should be larger than 0 and less than the number of up sample layers.
            Defaults to 1.
        res_block: whether to use residual connection based convolution blocks during the network.
            Defaults to ``False``.
        trans_bias: whether to set the bias parameter in transposed convolution layers. Defaults to ``False``.
    """
    
    def __init__(self,parameters:dict ):
        super(dynunet_wrapper, self).__init__(parameters)
        strides = (1, 1, 1, 1)
        self.model = dynunet.DynUNet(spatial_dims= 3,
                                    in_channels=2,
                                    out_channels=2,
                                    kernel_size= (3, 3, 3, 1),
                                    strides=strides,
                                    upsample_kernel_size=strides[1:],
                                    # filters=,
                                    dropout=None,
                                    norm_name="batch",
                                    act_name=("leakyrelu", {"inplace": True, "negative_slope": 0.2}),
                                    deep_supervision=False,
                                    # deep_supr_num=,
                                    # res_block=True,
                                    # trans_bias=)
        )
        
    def forward(self, x):
        return self.model.forward()