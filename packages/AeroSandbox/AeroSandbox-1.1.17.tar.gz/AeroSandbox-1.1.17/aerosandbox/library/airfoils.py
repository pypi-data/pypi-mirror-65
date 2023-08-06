### This file contains an assortment of random airfoils to use
from ..geometry import *
from .aerodynamics import *

generic_cambered_airfoil = Airfoil(
    CL_function=lambda alpha, Re, mach, deflection,: (  # Lift coefficient function
            (alpha * np.pi / 180) * (2 * np.pi) + 0.4550
    ),
    CDp_function=lambda alpha, Re, mach, deflection: (  # Profile drag coefficient function
            (1 + (alpha / 5) ** 2) * 2 * Cf_flat_plate(Re_L=Re)
    ),
    Cm_function=lambda alpha, Re, mach, deflection: (  # Moment coefficient function about quarter-chord
        -0.1
    )
)
generic_airfoil = Airfoil(
    CL_function=lambda alpha, Re, mach, deflection,: (  # Lift coefficient function
            (alpha * np.pi / 180) * (2 * np.pi)
    ),
    CDp_function=lambda alpha, Re, mach, deflection: (  # Profile drag coefficient function
            (1 + (alpha / 5) ** 2) * 2 * Cf_flat_plate(Re_L=Re)
    ),
    Cm_function=lambda alpha, Re, mach, deflection: (  # Moment coefficient function about quarter-chord
        0
    )  # TODO make this an actual curve!
)

# Make the airfoils
e216 = Airfoil("e216")
e216.CL_function = lambda alpha, Re, mach, deflection: (  # Lift coefficient function
    Cl_e216(alpha=alpha, Re_c=Re)
)
e216.CDp_function = lambda alpha, Re, mach, deflection: (  # Profile drag coefficient function
        Cd_profile_e216(alpha=alpha, Re_c=Re) +
        Cd_wave_e216(Cl=Cl_e216(alpha=alpha, Re_c=Re), mach=mach)
)
e216.Cm_function = lambda alpha, Re, mach, deflection: (  # Moment coefficient function about quarter-chord
    -0.15  # TODO
)  # TODO make this an actual curve!

rae2822 = Airfoil("rae2822")
rae2822.CL_function = lambda alpha, Re, mach, deflection: (  # Lift coefficient function
    Cl_rae2822(alpha=alpha, Re_c=Re)
)
rae2822.CDp_function = lambda alpha, Re, mach, deflection: (  # Profile drag coefficient function
        Cd_profile_rae2822(alpha=alpha, Re_c=Re) +
        Cd_wave_rae2822(Cl=Cl_rae2822(alpha=alpha, Re_c=Re), mach=mach)
)
rae2822.Cm_function = lambda alpha, Re, mach, deflection: (  # Moment coefficient function about quarter-chord
    -0.05
)  # TODO make this an actual curve!

naca0008 = Airfoil("naca0008")
naca0008.CL_function = lambda alpha, Re, mach, deflection: (  # Lift coefficient function
    Cl_flat_plate(alpha=alpha, Re_c=Re) # TODO fit this to actual data
)
naca0008.CDp_function = lambda alpha, Re, mach, deflection: (  # Profile drag coefficient function
        (1 + (alpha / 5) ** 2) * 2 * Cf_flat_plate(Re_L=Re) # TODO fit this to actual data
)
naca0008.Cm_function = lambda alpha, Re, mach, deflection: (  # Moment coefficient function about quarter-chord
    0
)  # TODO make this an actual curve!

flat_plate = Airfoil(
    CL_function=lambda alpha, Re, mach, deflection,: (  # Lift coefficient function
        Cl_flat_plate(alpha=alpha, Re_c=Re)
    ),
    CDp_function=lambda alpha, Re, mach, deflection,: (  # Profile drag coefficient function
            Cf_flat_plate(Re_L=Re) * 2
    ),
    Cm_function=lambda alpha, Re, mach, deflection: (  # Moment coefficient function
        0
    )  # TODO make this an actual curve!
)
