from fastmrt.modules.data_module import FastmrtDataModule
from fastmrt.data.transforms import FastmrtDataTransform2D
from fastmrt.data.mask import RandomMaskFunc
from fastmrt.data.prf import PrfFunc, PrfHeader
from fastmrt.data.augs import IdentityAugs

root = "/data/fastmri/knee/multicoil_train"

mask_func = RandomMaskFunc(center_fraction=0.08, acceleration=4)
prf_func = PrfFunc(prf_header=PrfHeader(B0=3.0, gamma=42.58, alpha=0.01, TE=0.03))
augs_func = IdentityAugs()

transform = FastmrtDataTransform2D(
    mask_func=mask_func, prf_func=prf_func, aug_func=augs_func, data_format='complex'
)

dm = FastmrtDataModule(
    root=root,
    only_source=True,
    train_transform=transform,
    val_transform=transform,
    test_transform=transform,
    batch_size=2,
    workers=2
)

dm.setup()

loader = dm.train_dataloader()
for batch in loader:
    print(batch.keys())
    break
