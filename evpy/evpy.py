def throttle_calc(w,kt,Vdc):
    """
    INPUTS
    -----
    w : desired speed [rad/s]
    kt : motor torque constant
    Vdc = DC voltage [V]

    OUTPUT
    -----
    d = throttle setting
    """

    d = w*kt/Vdc

    return d

def mot_eff(w,M,d,Vdc,kt,Rm,I0):
    """
    INPUTS
    -----
    w : desired speed [rad/s]
    M : desired torque [N*m]
    d : throttle setting
    Vdc : DC voltage [V]
    kt : motor torque constant
    Rm : stator winding resistance [Ω]
    I0 : no-load current [A]

    OUTPUTS
    -----
    Iac : actual current draw [A]
    Pac : power consumption by motor [W]
    n_mot : motor efficiency
    Qmot: total losses of motor [W]
    """

    #derive internal parms
    E = kt*w #[V] back-EMF
    I = M/kt+I0 #[A] nominal motor current
    Pmech = M*w #[W] applied mechanical load power

    #calculate losses
    Qcopper = Rm*I**2.0 #[W] copper losses
    Qiron = kt*I0*w #[W] iron losses
    Qmisc = 0.1*Pmech #[W] miscellaneous losses
    Qharm = (Qcopper+Qiron)/d #[W] increase in losses from harmonics
    Qmot = Qmisc + Qharm #[W] losses including harmonic distortion

    #calc efficiency, final current and power draw
    Pac = Pmech + Qmot #[W] elec power consumed by motor
    n_mot = Pmech/Pac # motor efficiency
    Iac = Pac/E #[A] actual current draw

    return Iac, Pac, n_mot, Qmot

def ctrl_eff(Iac,Pac,d,Vdc,f_pwm=12E3,Rds_on=1E-3,T_trans=1E-6,P_qui=0.25):
    """
    INPUTS
    -----
    Iac : actual current draw [A]
    Pac : power consumption by motor [W]
    d : throttle setting
    Vdc : DC voltage [V]
    f_pwm : switching frequency of ESC [Hz]
    Rds_on : ESC resistance [Ω]
    T_trans : transition period of MOSFETs
    P_qui : quiescent losses

    OUTPUTS
    -----
    Idc : actual current draw [A]
    Pdc : power consumption by ESC [W]
    n_ctrl: efficiency of ESC
    Q_ctrl: total losses of ESC [W]
    """

    #calculate losses for desired load
    Qcopper = Rds_on*(Iac**2.0) #[W] copper losses
    Qswitch = f_pwm*T_trans*Vdc*Iac #[W] switching losses
    Qharm = 2*(Qcopper+Qswitch)/d #[W] increase in losses from harmonics
    Qctrl = P_qui + Qharm #[W] losses including harmonic distortion

    #calculate efficiency, DC power, DC current draw
    Pdc = Pac + Qesc #[W] elec power consumed by ESC
    n_ctrl = Pac/Pdc # ESC efficiency
    Idc = Pdc/Vdc #[A] actual current draw

    return Idc, Pdc, n_ctrl, Qctrl
