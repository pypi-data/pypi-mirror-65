$sarah_file_comment

ParticleDefinitions[GaugeES] = {
	(* new fields *)
$particles_GaugeES

	(* Standard Model *)
	{H0, {
			PDG -> {0},
			Width -> 0,
			Mass -> Automatic,
			FeynArtsNr -> 1,
			LaTeX -> "H^0",
			OutputName -> "H0"
		}
	},
	{Hp, {
			PDG -> {0},
			Width -> 0,
			Mass -> Automatic,
			FeynArtsNr -> 2,
			LaTeX -> "H^+",
			OutputName -> "Hp"
		}
	},

	{VB,  {Description -> "B-Boson"}},
	{VG,  {Description -> "Gluon"}},
	{VWB, {Description -> "W-Bosons"}},
	{gB,  {Description -> "B-Boson Ghost"}},
	{gG,  {Description -> "Gluon Ghost"}},
	{gWB, {Description -> "W-Boson Ghost"}}
};

ParticleDefinitions[EWSB] = {
	(* new fields *)
$particles_EWSB

	(* Neutrinos *)
	{Fv,   {Description -> "Neutrinos",
			Mass -> LesHouches
		}
	},

	(* Standard Model *)
	{hh,   {Description -> "Higgs",
			PDG -> {25},
			PDG.IX -> {101000001}
		}
	},
	{Ah,   {Description -> "Pseudo-Scalar Higgs",
			PDG -> {0},
			PDG.IX -> {0},
			Mass -> {0},
			Width -> {0}
		}
	},
	{Hp,   {Description -> "Charged Higgs",
			PDG -> {0},
			PDG.IX -> {0},
			Width -> {0},
			Mass -> {0},
			LaTeX -> {"H^+", "H^-"},
			OutputName -> {"Hp", "Hm"},
			ElectricCharge -> 1
		}
	},

	{VP,   {Description -> "Photon"}},
	{VZ,   {Description -> "Z-Boson",
			Goldstone -> $particles_goldstone_Z
		}
	},
	{VWp,  {Description -> "W+ - Boson",
			Goldstone -> $particles_goldstone_W
		}
	},
	{VG,   {Description -> "Gluon"}},
	{gP,   {Description -> "Photon Ghost"}},
	{gZ,   {Description -> "Z-Boson Ghost"}},
	{gWp,  {Description -> "Positive W+ - Boson Ghost"}},
	{gWpC, {Description -> "Negative W+ - Boson Ghost"}},
	{gG,   {Description -> "Gluon Ghost"}},

	{Fu,   {Description -> "Up-Quarks"}},
	{Fd,   {Description -> "Down-Quarks"}},
	{Fe,   {Description -> "Leptons"}}
};

WeylFermionAndIndermediate = {
	(* new fields *)
$particles_WeylFermionAndIndermediate

	(* Standard Model *)
	{H, {
			PDG -> {0},
			Width -> 0,
			Mass -> Automatic,
			LaTeX -> "H",
			OutputName -> ""
		}
	},

	{l,   {LaTeX -> "l"}},
	{vL,  {LaTeX -> "\\nu_L"}},
	{eL,  {LaTeX -> "e_L"}},
	{eR,  {LaTeX -> "e_R"}},
	{q,   {LaTeX -> "q"}},
	{uL,  {LaTeX -> "u_L"}},
	{dL,  {LaTeX -> "d_L"}},
	{uR,  {LaTeX -> "u_R"}},
	{dR,  {LaTeX -> "d_R"}},

	{EL,  {LaTeX -> "E_L"}},
	{ER,  {LaTeX -> "E_R"}},
	{UL,  {LaTeX -> "U_L"}},
	{DL,  {LaTeX -> "D_L"}},
	{UR,  {LaTeX -> "U_R"}},
	{DR,  {LaTeX -> "D_R"}}
};
