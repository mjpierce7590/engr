def NormalStress(P, A):
    """
    Average Normal Stress Distribution

	Computes the average normal stress at any point in the cross-sectional area

	Assumptions
	-----------
	* applies only to the central regions of bars loaded axially
	* does not apply to the ends of bars near localized distortions
	* P is applies along the centroidal axis of the cross section
	* material must be homogeneous and isotropic

    Parameters
    ----------
    P : flt : [lbs]
        Normal force exerted on the cross section
    A : flt : [in^2]
        Cross-sectional area

    Returns
    -------
    sigma : flt : [psi]
		The average normal stress at any point in the cross-sectional area
    """
    return P / A

def ShearStress(V, A):
    """
    Average Shear Stress Distribution

    Computes the average shear stress at any point in the cross-sectional area

    Assumptions
    -----------
    * simple or direction shear loading

    Parameters
    ----------
    V : flt : [lbs]
        Internal resultant shear force at the section determined from the equations of equilibrium
    A : flt : [in^2]
        Cross-sectional area

    Returns
    -------
    tau_avg : flt : [psi]
        Average shear stress at the cross-sectional area
    """
    return V / A

def helloworld():
    print("hello world")

if __name__ == "__main__":
    helloworld()