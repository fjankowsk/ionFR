
import numpy as np


def interpolate_to_hour_resolution(a, NumberOfMaps, pointsLat, pointsLon, totalmaps, timeInt):
    """
    Interpolate the IONEX files to 1 hour resolution (25 maps per day).

    Returns
    -------
    newa: ~np.array of float
        The TEC data interpolated to 25 maps, i.e. 1 hour resolution.

    Raises
    ------
    RuntimeError
        On incorrect input.
    """

    # sanity check input
    if NumberOfMaps != 13:
        raise RuntimeError('Wrong number of TEC maps: {0}'.format(NumberOfMaps))

    # producing interpolated TEC maps, and consequently a new array that will
    # contain 25 TEC maps in total. The interpolation method used is the second
    # one indicated in the IONEX manual

    # creating a new array that will contain 25 maps in total
    newa = np.zeros((totalmaps, int(pointsLat), int(pointsLon)))
    inc = 0

    for item in range(int(NumberOfMaps)):
        newa[inc,:,:] = a[item,:,:]
        inc = inc + 2

    # performing the interpolation to create 12 addional maps
    # from the 13 TEC maps available
    while int(timeInt) <= (totalmaps - 2):
        for lat in range(int(pointsLat)):
            for lon in range(int(pointsLon)):
                # interpolation type 2:
                # newa[int(timeInt),lat,lon] = 0.5*newa[int(timeInt)-1,lat,lon] + 0.5*newa[int(timeInt)+1,lat,lon]
                # interpolation type 3 ( 3 or 4 columns to the right and left of the odd maps have values of zero
                # correct for this
                if (lon >= 4) and (lon <= (pointsLon - 4)):
                        newa[int(timeInt),lat,lon] = 0.5 * newa[int(timeInt)-1,lat,lon+3] + 0.5 * newa[int(timeInt)+1,lat,lon-3]

        timeInt = timeInt + 2.0
    
    return newa
