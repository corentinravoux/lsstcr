import matplotlib.pyplot as plt
import numpy as np
from lsst.afw.cameraGeom import FIELD_ANGLE, FOCAL_PLANE, DetectorType
from lsst.obs.lsst import LsstCam, LsstComCam
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon


def getCamera(name):
    """
    Get the camera object for a given camera name.
    Supported cameras: 'LSSTCam', 'LSSTComCam'.
    """
    if name == "LSSTCam":
        return LsstCam()
    elif name == "LSSTComCam":
        return LsstComCam()
    else:
        raise ValueError(
            f"Unsupported camera name: {name}. Use 'LSSTCam' or 'LSSTComCam'."
        )


def plotFocalPlane(
    camera, sky_units=True, ax=None, ra_field=0.0, dec_field=0.0, show_name=True
):

    colorMap = {
        DetectorType.SCIENCE: "b",
        DetectorType.FOCUS: "y",
        DetectorType.GUIDER: "g",
        DetectorType.WAVEFRONT: "r",
    }

    patches = []
    colors = []
    if ax is None:
        plt.figure(figsize=(15, 15))
        ax = plt.gca()
    xvals = []
    yvals = []
    for det in camera:
        if sky_units:
            corners_radec = camera.transform(
                det.getCorners(FOCAL_PLANE), FOCAL_PLANE, FIELD_ANGLE
            )
            corners = [
                (ra_field + c.getX() * 180 / np.pi, dec_field + c.getY() * 180 / np.pi)
                for c in corners_radec
            ]
        else:
            corners = [(c.getX(), c.getY()) for c in det.getCorners(FOCAL_PLANE)]
        for corner in corners:
            xvals.append(corner[0])
            yvals.append(corner[1])
        colors.append(colorMap[det.getType()])
        patches.append(Polygon(corners, closed=True))
        if show_name:
            center = det.getOrientation().getFpPosition()
            if sky_units:
                center_radec = camera.transform(center, FOCAL_PLANE, FIELD_ANGLE)
                center_x = ra_field + center_radec.getX() * 180 / np.pi
                center_y = dec_field + center_radec.getY() * 180 / np.pi
            else:
                center_x, center_y = center.getX(), center.getY()
            if det.getName() in ["R04_SW0", "R04_SW1", "R40_SW0", "R40_SW1"]:
                text_rotation = "vertical"
            else:
                text_rotation = "horizontal"
            ax.text(
                center_x,
                center_y,
                det.getName(),
                horizontalalignment="center",
                rotation=text_rotation,
                rotation_mode="anchor",
                size=6,
            )
    patchCollection = PatchCollection(
        patches, alpha=0.4, edgecolor=colors, facecolor="None"
    )
    ax.add_collection(patchCollection)
    ax.set_xlim(min(xvals) - 0.5, max(xvals) + 0.5)
    ax.set_ylim(min(yvals) - 0.5, max(yvals) + 0.5)
