# Optical Flow Visualization

Python port of the optical flow visualization: [people.csail.mit.edu/celiu/OpticalFlow/](https://people.csail.mit.edu/celiu/OpticalFlow/).
This implementation is based on the color wheel presented in:

```
S. Baker, D. Scharstein, J. Lewis, S. Roth, M. J. Black, and R. Szeliski.
A database and evaluation methodology for optical flow.
In Proc. IEEE International Conference on Computer Vision (ICCV), 2007.
```

## Installation

    pip install flow_vis

## Usage

    import flow_vis
    flow_color = flow_vis.flow_to_color(flow_uv, convert_to_bgr=False)

## Examples visualizations

Example visualization from the MPI Sintel Dataset:

![MPI Sintel 01](./example/data/mpi-sintel-01.png)

![MPI Sintel 02](./example/data/mpi-sintel-03.png)

![MPI Sintel 03](./example/data/mpi-sintel-02.png)


## Acknowledgements

I would like to thank [Susana Bouchardet](https://github.com/sbouchardet) for preparing the repository for PyPi.
