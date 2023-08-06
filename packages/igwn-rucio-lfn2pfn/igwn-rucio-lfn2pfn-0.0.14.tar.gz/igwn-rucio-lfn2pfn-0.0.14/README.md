# igwn-rucio-lfn2pfn

Algorithm for LFN to PFN conversion for rucio in the international gravitational wave network

## Plugging into rucio as an external module
As currently configured, this module should be made available to rucio by setting the following in the `rucio.cfg`:
```
[policy]
lfn2pfn_module=igwn_lfn2pfn.frames_lfn2pfn
lfn2pfn_algorithm=ligo_legacy
```
And installing via e.g.,:
```
pip install git+https://git.ligo.org/rucio/igwn-rucio-lfn2pfn.git
```

