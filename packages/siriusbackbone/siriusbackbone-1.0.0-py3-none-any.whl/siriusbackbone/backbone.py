import torch
import torch.nn as nn
import torchvision.models._utils as mutils
import torchvision.models as pretrains



class BackBone(nn.Module):
    def __init__(self, net, maps):
        super().__init__()
        self.net = getattr(pretrains, net)(pretrained=True)
        self.maps = maps
        self.backbone = mutils.IntermediateLayerGetter(self.net, self.maps)
    
    def forward(self, x):
        res = self.backbone(x)
        k = list(self.maps.values())[0]
        return res[k]


def mobilenet_v2():
    return BackBone('mobilenet_v2', {'features': 'backbone'})


def resnet18():
    return BackBone('resnet18', {'layer4': 'backbone'})



if __name__ == '__main__':
    x = torch.randn(1, 3, 300, 300)
    net = resnet18()
    with torch.no_grad():
        res = net(x)
