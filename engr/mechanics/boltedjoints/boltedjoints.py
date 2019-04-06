import numpy as np


def F_preload(S_ty, A_t, reuse=True):
    if reuse:
        F_preload = 0.64 * S_ty * A_t
    else:
        F_preload = 0.77 * S_ty * A_t
    return F_preload


def Torque(K_factor, d_nominal, F_preload):
    return K_factor * d_nominal * F_preload


def PreloadStress(F_preload, A_t):
    return F_preload / A_t


def MemberStiffness(E, d, l):
    return 0.5574 * np.pi * E * d / (2 * np.log(5 * (0.5774 * l + 0.5 * d) / (0.5774 * l + 2.5 * d)))


def BoltStiffness(E, A_t, l):
    return E * A_t / l


def StiffnessConstant(k_b, k_m):
    return k_b / (k_b + k_m)


def FailureForce(S_ty, A_t):
    return 0.85 * S_ty * A_t


def ServiceLoad(failforce, preloadforce, C, FS):
    return (failforce - preloadforce) / (C * FS)


class Bolt(object):
    def __init__(self, d_nominal, tensilestrength, tensilestressarea, reuse=True, K=.2):
        self.d_nominal = d_nominal
        self.tensilestrength = tensilestrength
        self.tensilestressarea = tensilestressarea
        self.reuse = reuse
        self.K = K

        # compute recommended preload
        self.F_preload = F_preload(self.tensilestrength, self.tensilestressarea, reuse=reuse)

        # assumes K factor of .2
        self.Torque = Torque(self.K, self.d_nominal, self.F_preload)

        # preload stress
        self.Stress_preload = PreloadStress(self.F_preload, self.tensilestressarea)

        # failure force
        self.failureforce = FailureForce(self.tensilestrength, self.tensilestressarea)

    def SetGrip(self, l):
        self.grip = l

    def SetModulus(self, E):
        self.modulus = E

    def CalcStiffness(self):
        self.stiffness = BoltStiffness(self.modulus, self.tensilestressarea, self.grip)


class Member(object):
    def __init__(self, thickness, ID, modulus):
        self.thickness = thickness
        self.ID = ID
        self.modulus = modulus

        # compute stiffness
        self.stiffness = MemberStiffness(self.modulus, self.ID, self.thickness)


class BoltedJoint(object):
    def __init__(self, bolt, member):
        self.bolt = bolt
        self.member = member

        # compute stiffness
        self.stiffnessconstant = StiffnessConstant(self.bolt.stiffness, self.member.stiffness)

        # service load
        # assume FS of 4
        self.serviceload = ServiceLoad(self.bolt.failureforce, self.bolt.F_preload, self.stiffnessconstant, 1)


def OldRoutine():
    print("BOLT")
    print("Thread Size: 1/2-13")
    print("Tensile Strength: 150,000 psi")
    print("Tensile Yield: 130, 000 psi")
    print("Thread Fit: Class 2A")
    print("Tensile Stress Area: 0.1419 in^2")
    print("Service Load: 1000 lbs")

    mybolt = Bolt(.5, 130000, 0.1419)
    print("\nRESULTS")
    print("Preload Force: {} lbs".format(mybolt.F_preload))
    print("Preload Torque: {} in-lbs".format(mybolt.Torque))
    print("Preload Stress: {} psi".format(mybolt.Stress_preload))

    print("\nMEMBER")
    print("Thickness: 1 in")
    print("Hole ID: 0.5156 in")
    print("Modulus of Elasticity: 29000000 psi")

    mymember = Member(1, 0.5156, 29e6)
    print("\nRESULTS")
    print("Member Stiffness: {} lbs/in".format(mymember.stiffness))

    print("\nSTACK UP")
    print("Assume no washer, grip is exactly 1 in")
    mybolt.SetGrip(1)
    mybolt.SetModulus(29e6)
    mybolt.CalcStiffness()
    print("\nRESULTS")
    print("Bolt Stiffness: {} lbs/in".format(mybolt.stiffness))
    myjoint = BoltedJoint(mybolt, mymember)
    print("Joint Stiffness Constant: {}".format(myjoint.stiffnessconstant))

    print("\nFAILURE")
    print("Failure Force of Bolt: {}".format(mybolt.failureforce))
    print("Service Load of Joint: {}".format(myjoint.serviceload))


if __name__ == "__main__":
    OldRoutine()
