


def _cal_height(x,y,z):
    h0 = 0
    i = 0
    while i<=10 and delt_h <= 0.001:
        h = search_h(x,y,z)
        
        delt_h = abs(h-h0)
        h0 = h
        i += 1
    
    
    
    
def search_h(x,y,z):
    pass


import math

def computeEllipsoidElevation(x, y, z, semiMajor, semiMinor, desired_precision, achieved_precision=None):
    # Compute elevation given xyz
    # Requires semi-major-axis and eccentricity-square
    MKTR = 10
    ecc_sqr = 1.0 - semiMinor * semiMinor / semiMajor / semiMajor
    ep2 = 1.0 - ecc_sqr
    d2 = x * x + y * y
    d = math.sqrt(d2)
    h = 0.0
    ktr = 0
    hPrev = r = 0.0

    # Suited for points near equator
    if d >= z:
        tanPhi = z / d
        while True:
            hPrev = h
            tt = tanPhi * tanPhi
            r = semiMajor / math.sqrt(1.0 + ep2 * tt)
            zz = z + r * ecc_sqr * tanPhi
            n = r * math.sqrt(1.0 + tt)
            h = math.sqrt(d2 + zz * zz) - n
            tanPhi = zz / d
            print('tanPhi:\n',tanPhi)
            ktr += 1
            print(h)
            if ktr > MKTR or abs(h - hPrev) < desired_precision:
                break
    else:
        # Suited for points near the poles
        cotPhi = d / z
        while ktr < MKTR and abs(h - hPrev) > desired_precision:
            hPrev = h
            cc = cotPhi * cotPhi
            r = semiMajor / math.sqrt(ep2 + cc)
            dd = d - r * ecc_sqr * cotPhi
            nn = r * math.sqrt(1.0 + cc) * ep2
            h = math.sqrt(dd * dd + z * z) - nn
            cotPhi = dd / z
            ktr += 1

    if achieved_precision is not None:
        achieved_precision[0] = abs(h - hPrev)

    return h


if __name__=='__main__':
    h = computeEllipsoidElevation(1121826.61526021, -4623505.4143307, -4233738.31197042,6378140,6356750,0.001)
    print(h)
    r_h = h - math.sqrt(1121826.61526021**2 + 4623505.4143307**2 + 4233738.31197042**2)
    print(r_h)