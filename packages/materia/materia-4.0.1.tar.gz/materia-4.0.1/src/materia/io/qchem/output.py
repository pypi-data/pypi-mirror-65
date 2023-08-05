from __future__ import annotations
import inspect
import numpy as np
import materia
import re
from typing import Dict, Tuple, TypeVar, Union

__all__ = ["QChemOutput"]

# class QChemOutput: #FIXME: inherit Output
#     def parse(self):
#         flag = ''
#         with open(self.filepath,'r') as f:
#             for line in f:
#                 flag = _set_flag(line=line,current_flag=flag)
#                 _parse_with_flag(flag=flag)(line=line,output=self.output)
#
# def _set_flag(line, current_flag):
#     if 'Archival summary' in line:
#         return 'footer'
#     elif 'Ground-State Mulliken Net Atomic Charges' in line:
#         return 'net_atomic_charges'
#     elif 'Orbital Energies' in line:
#         return 'orbital_energies'
#     else:
#         return current_flag
#
# def _parse_with_flag(flag):
#     if flag == 'footer':
#         return _parse_footer
#     elif flag == 'net_atomic_charges':
#         return _parse_net_atomic_charges
#     elif flag == 'orbital_energies':
#         return _parse_orbital_energies
#
# def _parse_footer(line, output):
#     if 'Total job time' in line:
#         wall_time,cpu_time = re.search(r'.*?(\d*\.\d*)s.*?(\d*\.\d*)s.*$',line).groups()
#         output['footer','wall_time'] = materia.Qty(value=float(wall_time),unit=materia.second)
#         output['footer','cpu_time'] = materia.Qty(value=float(cpu_time),unit=materia.second)
#
# def _parse_net_atomic_charges(line, output):
#     if 'Atom ' in line:
#         (charge_unit_string,) = re.search(r'.*\((.*)\).*$',line).groups()
#         if charge_unit_string.lower() == 'ev':
#             output['net_atomic_charges','unit'] = materia.eV
#         elif charge_unit_string.lower() == 'a.u.':
#             output['net_atomic_charges','unit'] = materia.au_charge
#     elif 'Sum of atomic charges' in line:
#         *_,sum_of_atomic_charges_str = line.split()
#         output['net_atomic_charges','sum_of_atomic_charges'] = materia.Qty(value=float(sum_of_atomic_charges_str),unit=output['net_atomic_charges','unit'])
#     elif len(line.split()) > 0 and line.split()[0].isdigit():
#         atom_number,atomic_species,charge = line.split()
#         output['net_atomic_charges',atom_number,'species'] = atomic_species
#         output['net_atomic_charges',atom_number,'charge'] = materia.Qty(value=float(charge),unit=output['net_atomic_charges','unit'])
#
# def _parse_orbital_energies(line, output):
#     if 'Orbital Energies' in line:
#         (unit_str,) = re.search(r'.*\((.*)\).*$',line).groups()
#         if unit_str == 'a.u.':
#             output['orbital_energies','unit'] = materia.hartree
#     elif 'Alpha' in line:
#         parse_alpha_orbitals = True
#     elif 'Beta' in line:
#         parse_alpha_orbitals = False
#     elif 'Occupied' in line:
#         parse_occupied_orbitals = True
#     elif 'Virtual' in line:
#         parse_occupied_orbitals = False
#     else:
#         output['orbital_energies','alpha' if parse_alpha_orbitals else 'beta','occupied' if parse_occupied_orbitals else 'unoccupied'].extend(materia.Qty(value=float(eng),unit=output['orbital_energies','unit']) for eng in line.strip().split())

T = TypeVar("T")


class QChemOutput:
    def __init__(self, filepath: str) -> None:
        self.filepath = materia.expand(filepath)

    def get(self, *quantity_names: str) -> Union[T, Tuple[T]]:
        method_dict = dict(inspect.getmembers(self, predicate=inspect.isroutine))

        with open(self.filepath, "r") as f:
            lines = "".join(f.readlines())

        quantities = tuple(
            method_dict[name.lower()](lines=lines) for name in quantity_names
        )

        if len(quantities) == 1:
            return quantities[0]
        return quantities

    def footer(
        self, lines: str
    ):  # FIXME: not sure how to annotate type hint: is it -> Dict[materia.Qty,materia.Qty,Tuple[int,str,int,int,int,int,str]] ?
        s = r"\s*Total\s*job\s*time\s*:\s*(\d*\.\d*)\s*s\s*\(\s*wall\s*\)\s*,\s*(\d*\.\d*)\s*s\s*\(\s*cpu\s*\)\s*(\w*)\s*(\w*)\s*(\d*)\s*(\d*)\s*:\s*(\d*)\s*:\s*(\d*)\s*(\d*)\s*"
        pattern = re.compile(s)
        (
            walltime,
            cputime,
            day,
            month,
            date,
            hour,
            minutes,
            seconds,
            year,
        ) = pattern.search(lines).groups()

        walltime = float(walltime) * materia.second
        cputime = float(cputime) * materia.second
        date = tuple(
            int(year), month, int(date), int(hour), int(minutes), int(seconds), day
        )

        return {"walltime": walltime, "cputime": cputime, "date": date}

    def kohn_sham_gap(self, lines: str):  # FIXME: not sure how to annotate type hint
        s = (
            r"\s*---\s*Generalized\s*Kohn-Sham\s*gap\s*\((\S*)\)\s*---"
            r"\s*HOMO\s*Eigenvalue\s*=\s*(-?\d*\.*\d*)\s*LUMO\s*Eigenvalue\s*"
            r"=\s*(-?\d*\.*\d*)\s*KS\s*gap\s*=\s*(-?\d*\.*\d*)\s*"
        )

        energy_unit_str, homo, lumo, gap = re.search(s, lines).groups()

        if energy_unit_str.lower() == "ev":
            unit = materia.eV
        else:
            raise ValueError("Cannot parse energy unit.")

        homo = float(homo) * unit
        lumo = float(lumo) * unit
        gap = float(gap) * unit

        return {"homo": homo, "lumo": lumo, "gap": gap}

    def polarizability(self, lines: str) -> materia.Qty:
        s = (
            r"\s*Polarizability tensor\s*\[(.*)\]\s*(-?\d*\.\d*)\s*"
            r"(-?\d*\.\d*)\s*(-?\d*\.\d*)\s*(-?\d*\.\d*)\s*(-?\d*\.\d*)\s*"
            r"(-?\d*\.\d*)\s*(-?\d*\.\d*)\s*(-?\d*\.\d*)\s*(-?\d*\.\d*)\s*"
        )
        pattern = re.compile(s)
        # FIXME: more robust (or any) error checking/edge-case handling needed here
        unit_str, *tensor_components = pattern.search(lines).groups()

        if unit_str.lower() == "a.u.":
            unit = materia.au_volume

        polarizability_tensor = (
            np.array(tuple(float(tc) for tc in tensor_components)).reshape(3, 3) * unit
        )

        return materia.Polarizability(polarizability_tensor=polarizability_tensor)

    def rttddft(self, lines: str):  # FIXME: not sure how to annotate type hint
        s = r"ITER:\s*(\d*)\s*T:\s*(\d*\.\d*)\(fs\)\s*dt\s*(\d*\.\d*)\(fs\)\s*Hr/Ps:\s*(\d*\.\d*)\s*-\s*Lpsd/Rem\.:\s*(\d*\.\d*),\s*([^\s]*)\s*\(min\)\s*Tr\.Dev:\s*(\d*\.\d*)\s*Hrm:\s*(\d*\.\d*)\s*Enrgy:\s*(-?\d*\.\d*)\s*Entr:\s*(-?\d*.\d*)\s*Fld\s*(\d*)\s*NFk:\s*(\d*)\s*Mu\s*(-?\d*\.\d*e?-?\d*)\s*(-?\d*\.\d*e?-?\d*)\s*(-?\d*\.\d*e?-?\d*)"
        pattern = re.compile(s)

        iterations = []
        Ts = []
        dts = []
        hours_per_ps = []
        lapsed = []  # FIXME: what is this?
        remaining = []  # FIXME: what is this?
        trace_deviations = []  # FIXME: what is this?
        hrms = []  # FIXME: what is this?
        energies = []
        entrs = []  # FIXME: what is this?
        field = []  # FIXME: what is this? field on or off, always a boolean?
        number_fock = []
        mu_xs = []
        mu_ys = []
        mu_zs = []

        for (
            iter,
            T,
            dt,
            hps,
            lpsd,
            rem,
            tr_dev,
            hrm,
            energy,
            entr,
            fld,
            nfk,
            mu_x,
            mu_y,
            mu_z,
        ) in pattern.findall(lines):
            iterations.append(int(iter))
            Ts.append(float(T))
            dts.append(float(dt))
            hours_per_ps.append(float(hps))
            lapsed.append(float(lpsd))
            remaining.append(float(rem))
            trace_deviations.append(float(tr_dev))
            hrms.append(float(hrm))
            energies.append(float(energy))
            entrs.append(float(entr))
            field.append(int(fld))
            number_fock.append(int(nfk))
            mu_xs.append(float(mu_x))
            mu_ys.append(float(mu_y))
            mu_zs.append(float(mu_z))

        return {
            "iterations": iterations,
            "T": np.array(Ts) * materia.fs,
            "dt": np.array(dts) * materia.fs,
            "hours_per_picosecond": np.array(hours_per_ps) * materia.hr / materia.ps,
            "lapsed": np.array(lapsed) * materia.minute,
            "remaining": np.array(remaining) * materia.minute,
            "trace_deviations": trace_deviations,
            "hrm": hrms,
            "energies": np.array(energies) * materia.hartree,
            "entr": entrs,
            "field": field,
            "number_fock": number_fock,
            "mu_x": np.array(mu_xs) * materia.au_dipole_moment,
            "mu_y": np.array(mu_ys) * materia.au_dipole_moment,
            "mu_z": np.array(mu_zs) * materia.au_dipole_moment,
        }

    def electronic_excitations(
        self, lines: str
    ):  # FIXME: not sure how to annotate type hint
        s = (
            r"\s*excitation\s*energy\s*"
            r"\((.*)\)\s*=\s*(-?\d*.\d*)\s*Total\s*energy\s*for\s*state\s*"
            r"\d*:\s*(-?\d*.\d*)\s*([^\s]*)\s*Multiplicity\s*:\s*([^\s]*)\s*"
            r"Trans.\s*Mom.\s*:\s*(-?\d*.\d*)\s*X\s*(-?\d*.\d*)\s*Y"
            r"\s*(-?\d*.\d*)\s*Z\s*Strength\s*:\s*(-?\d*.\d*)\s*"
            r"(([DSV]\(\s*\d*\s*\)\s*-*>\s*[DSV]\(\s*\d*\s*\)\s*"
            r"amplitude\s*=\s*-?\d*.\d*\s*)*)"
        )
        pattern_1 = re.compile(s)

        s = (
            r"([DSV])\(\s*(\d*)\s*\)\s*-*>\s*([DSV])\(\s*(\d*)\s*\)\s*"
            r"amplitude\s*=\s*(-?\d*.\d*)\s*"
        )
        pattern_2 = re.compile(s)

        return tuple(
            self._process_ee_block(
                block=block, pattern_1=pattern_1, pattern_2=pattern_2
            )
            for block in re.split(r"\s*Excited\s*state\s*\d*\s*:", lines)[1:]
        )

    def _process_ee_block(
        self, block, pattern_1, pattern_2
    ):  # FIXME: not sure how to annotate type hint
        (
            excitation_energy_unit_str,
            excitation_energy,
            total_energy,
            total_energy_unit_str,
            multiplicity,
            moment_x,
            moment_y,
            moment_z,
            strength_str,
            *excitation_strs,
        ) = pattern_1.search(block).groups()

        if excitation_energy_unit_str.lower() == "ev":
            excitation_energy_unit = materia.eV
        excitation_energy = float(excitation_energy) * excitation_energy_unit

        if total_energy_unit_str.lower() == "au":
            total_energy_unit = materia.au_energy
        total_energy = float(total_energy) * total_energy_unit

        if multiplicity.lower() == "singlet":
            mult = 1
        elif multiplicity.lower() == "triplet":
            mult = 3

        moment = np.array((float(moment_x), float(moment_y), float(moment_z)))
        strength = float(strength_str)

        contributions = []
        for s in excitation_strs:
            from_occ, from_num, to_occ, to_num, amplitude = pattern_2.search(s).groups()
            contributions.append(
                (from_occ, int(from_num), to_occ, int(to_num), float(amplitude))
            )

        return materia.ElectronicExcitation(
            excitation_energy=excitation_energy,
            total_energy=total_energy,
            multiplicity=mult,
            transition_moment=moment,
            oscillator_strength=strength,
            contributions=contributions,
        )

    def orbital_energies(self, lines: str) -> Tuple[Tuple[materia.Qty]]:
        energy_symmetry_pattern = re.compile(
            r"((?:-?\d*\.\d*\s*)*(?:\d*\s*[a-zA-Z]*\d*\s*)*)"
        )
        energy_pattern = re.compile(r"(-?\d*\.\d*)")
        symmetry_pattern = re.compile(r"(\d*\s*[a-zA-Z]+\d*)")

        s = r"\s*Orbital\s*Energies\s*\((a\.u\.)\)\s*and\s*Symmetries"
        pattern = re.compile(s)
        (energy_unit_str,) = pattern.search(lines).groups()
        if energy_unit_str == "a.u.":
            energy_unit = materia.hartree
        else:
            raise ValueError("Cannot parse energy unit in Orbital Energies section.")

        s = (
            r"\s*Alpha\s*MOs.*?"
            r"\s*--\s*Occupied\s*--\s*((?:(?:-?\d*\.\d*\s*)*(?:\d*\s*[a-zA-Z]*\d*\s*)*)*)"
            r"\s*--\s*Virtual\s*--\s*((?:(?:-?\d*\.\d*)*\s*(?:\d*\s*[a-zA-Z]*\d*)*\s*)*)"
        )
        pattern_alpha = re.compile(s)
        alpha_orbitals_occupied, alpha_orbitals_virtual = pattern_alpha.search(
            lines
        ).groups()

        alpha_orbital_occupied_energies = tuple(
            float(x) * energy_unit
            for split in energy_symmetry_pattern.findall(alpha_orbitals_occupied)
            for x in energy_pattern.findall(split)
            if split != ""
        )
        alpha_orbital_virtual_energies = tuple(
            float(x) * energy_unit
            for split in energy_symmetry_pattern.findall(alpha_orbitals_virtual)
            for x in energy_pattern.findall(split)
            if split != ""
        )
        # alpha_orbital_occupied_symmetries = tuple(x for split in energy_symmetry_pattern.findall(alpha_orbitals_occupied) for x in symmetry_pattern.findall(split) if split != '')

        s = (
            r"\s*Beta\s*MOs.*?"
            r"\s*--\s*Occupied\s*--\s*((?:(?:-?\d*\.\d*\s*)*(?:\d*\s*[a-zA-Z]*\d*\s*)*)*)"
            r"\s*--\s*Virtual\s*--\s*((?:(?:-?\d*\.\d*)*\s*(?:\d*\s*[a-zA-Z]*\d*)*\s*)*)"
        )
        pattern_beta = re.compile(s)
        beta_orbitals_occupied, beta_orbitals_virtual = pattern_beta.search(
            lines
        ).groups()

        beta_orbital_occupied_energies = tuple(
            float(x) * energy_unit
            for split in energy_symmetry_pattern.findall(beta_orbitals_occupied)
            for x in energy_pattern.findall(split)
            if split != ""
        )
        beta_orbital_virtual_energies = tuple(
            float(x) * energy_unit
            for split in energy_symmetry_pattern.findall(beta_orbitals_virtual)
            for x in energy_pattern.findall(split)
            if split != ""
        )
        # beta_orbital_occupied_symmetries = tuple(x for split in energy_symmetry_pattern.findall(beta_orbitals_occupied) for x in symmetry_pattern.findall(split) if split != '')

        return (
            alpha_orbital_occupied_energies,
            beta_orbital_occupied_energies,
            alpha_orbital_virtual_energies,
            beta_orbital_virtual_energies,
        )

    def scf_energy(self, lines: str) -> materia.Qty:
        s = r"\s*SCF\s*energy\s*in\s*the\s*final\s*basis\s*set\s*=\s*(-?\d*\.\d*)\s*"
        # FIXME: this doesn't seem like a great way to handle multiple groups... better fix?
        *_, energy_str = re.search(s, lines).groups()

        return float(energy_str) * materia.hartree

    def total_energy(self, lines: str) -> materia.Qty:
        s = r"\s*Total\s*energy\s*in\s*the\s*final\s*basis\s*set\s*=\s*(-?\d*\.\d*)\s*"
        # FIXME: this doesn't seem like a great way to handle multiple groups... better fix?
        *_, energy_str = re.search(s, lines).groups()

        return float(energy_str) * materia.hartree


# class Section:
#     def __init__(self, name):
#         self.name = name
#
#     def parse(self, line):
#         pass
#
#     @property
#     def sections(self):
#         section_list = []
#         lines = []
#         section_class = None
#
#         for line in self.lines:
#             new_section_class = next((sc for skw,sc in self.section_keywords.items() if skw in line), None)
#             if new_section_class is None:
#                 lines.append(line)
#             else:
#                 if section_class is not None:
#                     section_list.append(section_class(lines=lines))
#                 section_class = new_section_class
#                 lines = [line]
#
#         section_list.append(section_class(lines=lines))
#
#         return tuple(section_list)
#
#     # def __str__(self):
#     #     return ''.join(self.lines)
#
# class QChemOutput(Section):
#     def __init__(self, filename):
#         self.filename = filename
#         #self.output_dict = collections.OrderedDict()
#         self.job_list = []
#
#     @property
#     def jobs(self):
#         with open(self.filename,'r') as f:
#             for line in f:
#                 self.parse(line)
#
#         return tuple(self.job_list)
#
#     def parse(self, line):
#         if 'Running Job' in line:
#             self.job_list.append(Job())
#         if len(self.job_list) > 0:
#             self.job_list[-1].parse(line=line)
#
# class Job:
#     def __init__(self):
#         self.sections = collections.OrderedDict()
#         self.names = collections.defaultdict(int)
#
#     def parse(self, line):
#         if 'Archival summary:' in line:
#             self.sections[self.append_counts('Footer')] = Footer()
#         elif 'Welcome to Q-Chem' in line:#elif 'Thank you very much for using Q-Chem.  Have a nice day.' in line:
#             self.sections[self.append_counts('Header')] = Header()
#         elif 'Checking the input file for inconsistencies...' in line:
#             self.sections[self.append_counts('InputEcho')] = InputEcho()
#         elif 'TDDFT/TDA calculation will be performed' in line:
#             self.sections[self.append_counts('TDDFTTDARoots')] = TDDFTTDARoots()
#         elif 'Excited state' in line:
#             self.sections[self.append_counts('TDDFTExcitation')] = TDDFTExcitation()
#         # elif 'TDDFT/TDA Excitation Energies' in line:
#         #     self.section_list.append(TDDFTExcitationEnergies())
#         elif 'Orbital Energies' in line:
#             self.sections[self.append_counts('OrbitalEnergies')] = OrbitalEnergies()
#         elif 'Generalized Kohn-Sham gap' in line:
#             self.sections[self.append_counts('KohnShamGap')] = KohnShamGap()
#         elif 'Ground-State Mulliken Net Atomic Charges' in line:
#             self.sections[self.append_counts('NetAtomicCharges')] = NetAtomicCharges()
#         elif 'Cartesian Multipole Moments' in line:
#             self.sections[self.append_counts('CartesianMultipoleMoments')] = CartesianMultipoleMoments()
#         elif 'SETman timing' in line:
#             self.sections[self.append_counts('SETManTiming')] = SETManTiming()
#         elif 'General SCF calculation program' in line:
#             self.sections[self.append_counts('SCF')] = SCF()
#         elif 'Gradient of SCF Energy' in line:
#             self.sections[self.append_counts('SCFGradient')] = SCFGradient()
#         elif 'Standard Nuclear Orientation' in line:
#             self.sections[self.append_counts('StandardNuclearOrientation')] = StandardNuclearOrientation()
#         elif 'Calculating the polarizability using responseman/libresponse' in line:
#             self.sections[self.append_counts('Polarizability')] = Polarizability()
#
#         if len(self.sections) > 0:
#             next(reversed(self.sections.values())).parse(line=line)
#
#     def append_counts(self, name):
#         self.names[name] += 1
#         return f'{name}_{self.names[name]}'
#         #data[x] += 1
#         #
#         #return f'{x}_{data[x]}'
#
# class CartesianMultipoleMoments(Section):
#     def __init__(self):
#         super().__init__(name='CartesianMultipoleMoments')
#         self.charge_next = False
#
#         self.charge_unit = None
#         self.charge_multiplier = None
#         self.charge = None
#         self.dipole_unit = None
#         self.total_dipole = None
#         self.quadrupole_unit = None
#         self.quadrupole = None
#
#     def todict(self):
#         dipole_value = np.array([self.x,self.y,self.z])
#         dipole = materia.Qty(value=dipole_value,unit=self.dipole_unit)
#
#         quad_value = np.array([self.xx,self.xy,self.xz,self.yx,self.yy,self.yz,self.zx,self.zy,self.zz]).reshape(3,3)
#         quadrupole = materia.Qty(value=quad_value,unit=self.quadrupole_unit)
#
#         oct_value = np.array([self.xxx,self.xxy,self.xxz,self.xyx,self.xyy,self.xyz,
#                               self.xzx,self.xzy,self.xzz,self.yxx,self.yxy,self.yxz,
#                               self.yyx,self.yyy,self.yyz,self.yzx,self.yzy,self.yzz,
#                               self.zxx,self.zxy,self.zxz,self.zyx,self.zyy,self.zyz,
#                               self.zzx,self.zzy,self.zzz]).reshape(3,3,3)
#         octopole = materia.Qty(value=oct_value,unit=self.octopole_unit)
#
#         hex_value = np.array([self.xxxx,self.xxxy,self.xxxz,self.xxyx,self.xxyy,
#                               self.xxyz,self.xxzx,self.xxzy,self.xxzz,self.xyxx,
#                               self.xyxy,self.xyxz,self.xyyx,self.xyyy,self.xyyz,
#                               self.xyzx,self.xyzy,self.xyzz,self.xzxx,self.xzxy,
#                               self.xzxz,self.xzyx,self.xzyy,self.xzyz,self.xzzx,
#                               self.xzzy,self.xzzz,self.yxxx,self.yxxy,self.yxxz,
#                               self.yxyx,self.yxyy,self.yxyz,self.yxzx,self.yxzy,
#                               self.yxzz,self.yyxx,self.yyxy,self.yyxz,self.yyyx,
#                               self.yyyy,self.yyyz,self.yyzx,self.yyzy,self.yyzz,
#                               self.yzxx,self.yzxy,self.yzxz,self.yzyx,self.yzyy,
#                               self.yzyz,self.yzzx,self.yzzy,self.yzzz,self.zxxx,
#                               self.zxxy,self.zxxz,self.zxyx,self.zxyy,self.zxyz,
#                               self.zxzx,self.zxzy,self.zxzz,self.zyxx,self.zyxy,
#                               self.zyxz,self.zyyx,self.zyyy,self.zyyz,self.zyzx,
#                               self.zyzy,self.zyzz,self.zzxx,self.zzxy,self.zzxz,
#                               self.zzyx,self.zzyy,self.zzyz,self.zzzx,self.zzzy,
#                               self.zzzz]).reshape(3,3,3,3)
#         hexadecapole = materia.Qty(value=hex_value,unit=self.hexadecapole_unit)
#
#         return {'charge': self.charge,'dipole': dipole,'total_dipole': self.total_dipole,
#                 'quadrupole': quadrupole,'octopole': octopole,'hexadecapole': hexadecapole}
#
#     def parse(self, line):
#         if 'Charge' in line:
#             self._parse_charge_unit_and_multiplier(line=line)
#             self.charge_next = True
#         elif self.charge_next:
#             self._parse_charge(line=line)
#             self.charge_next = False
#         elif 'Tot ' in line:
#             self._parse_total_dipole(line=line)
#         elif 'Quadrupole Moments' in line:
#             self._parse_quadrupole_unit(line=line)
#         elif 'Octopole Moments' in line:
#             self._parse_octopole_unit(line=line)
#         elif 'Hexadecapole Moments' in line:
#             self._parse_hexadecapole_unit(line=line)
#         elif 'Dipole Moment' in line:
#             self._parse_dipole_unit(line=line)
#         elif 'X' in line or 'Y' in line or 'Z' in line:
#             self._parse_multipole_elements(line=line)
#         else:
#             pass
#
#     def _parse_charge(self, line):
#         charge_value = float(line.strip())*self.charge_multiplier
#         self.charge = materia.Qty(value=charge_value,unit=self.charge_unit)
#
#     def _parse_charge_unit_and_multiplier(self, line):
#         charge_unit_str,charge_prefactor_base,charge_prefactor_exp = re.search(r'.*\((.*)\s*x\s*(\d*)\^(\d*).*\).*',line).groups()
#
#         charge_unit_str = charge_unit_str.strip().lower()
#         if charge_unit_str == 'esu':
#             self.charge_unit = materia.esu
#         else:
#             raise ValueError('Cannot parse charge unit in Cartesian Multipole Moments section.')
#
#         self.charge_multiplier = float(charge_prefactor_base)**float(charge_prefactor_exp)
#
#     def _parse_dipole_unit(self, line):
#         (dipole_unit_str,) = re.search(r'.*\((.*).*\).*',line).groups()
#         dipole_unit_str = dipole_unit_str.strip().lower()
#         if dipole_unit_str == 'debye':
#             self.dipole_unit = materia.debye
#         else:
#             raise ValueError('Cannot parse dipole unit in Cartesian Multipole Moments section.')
#
#     def _parse_quadrupole_unit(self, line):
#         (quad_unit_str,) = re.search(r'.*\((.*).*\).*',line).groups()
#         quad_unit_str = quad_unit_str.strip().lower()
#         if quad_unit_str == 'debye-ang':
#             self.quadrupole_unit = materia.debye*materia.angstrom
#         else:
#             raise ValueError('Cannot parse quadrupole unit in Cartesian Multipole Moments section.')
#
#     def _parse_octopole_unit(self, line):
#         (oct_unit_str,) = re.search(r'.*\((.*).*\).*',line).groups()
#         oct_unit_str = oct_unit_str.strip().lower()
#         if oct_unit_str == 'debye-ang^2':
#             self.octopole_unit = materia.debye*materia.angstrom**2
#         else:
#             raise ValueError('Cannot parse octopole unit in Cartesian Multipole Moments section.')
#
#     def _parse_hexadecapole_unit(self, line):
#         (hex_unit_str,) = re.search(r'.*\((.*).*\).*',line).groups()
#         hex_unit_str = hex_unit_str.strip().lower()
#         if hex_unit_str == 'debye-ang^3':
#             self.hexadecapole_unit = materia.debye*materia.angstrom**3
#         else:
#             raise ValueError('Cannot parse hexadecapole unit in Cartesian Multipole Moments section.')
#
#     def _parse_total_dipole(self, line):
#         _,dipole_total_value = line.split()
#         self.total_dipole = materia.Qty(value=float(dipole_total_value),unit=self.dipole_unit)
#
#     def _parse_multipole_elements(self, line):
#         for multipole_element_symbol,multipole_element_value in self._pairwise(iterable=line.split()):
#             self._store_multipole_element(element_symbol=multipole_element_symbol.lower(),value=float(multipole_element_value))
#
#     def _pairwise(self, iterable):
#         args = [iter(iterable)] * 2
#         return itertools.zip_longest(*args)
#
#     def _store_multipole_element(self, element_symbol, value):
#         for p in itertools.permutations(element_symbol):
#             setattr(self,''.join(p),value)
#
# class Footer(Section):
#     def __init__(self):
#         super().__init__(name='Footer')
#         self.wall_time = None
#         self.cpu_time = None
#
#     def todict(self):
#         return {'wall_time': self.wall_time, 'cpu_time': self.cpu_time}
#
#     def parse(self, line):
#         if 'Total job time' in line:
#             self._parse_job_time(line=line)
#
#     def _parse_job_time(self, line):
#         wall_time,cpu_time = re.search(r'.*?(\d*\.\d*)s.*?(\d*\.\d*)s.*$',line).groups()
#         self.wall_time = materia.Qty(value=float(wall_time),unit=materia.second)
#         self.cpu_time = materia.Qty(value=float(cpu_time),unit=materia.second)
#
# class Header(Section):
#     def __init__(self):
#         super().__init__(name='Header')
#
# class InputEcho(Section):
#     def __init__(self):
#         super().__init__(name='InputEcho')
#
# class KohnShamGap(Section):
#     def __init__(self):
#         super().__init__(name='KohnShamGap')
#         self.parse_lookup = {1: self._parse_unit, 2: self._parse_homo, 3: self._parse_lumo, 4: self._parse_gap}
#         self.num_lines = 0
#
#     def parse(self, line):
#         self.num_lines += 1
#         try:
#             self.parse_lookup[self.num_lines](line=line)
#             return True
#         except KeyError:
#             return False
#
#     def _parse_unit(self, line):
#         (unit_string,) = re.search(r'.*\((.*)\).*$',line).groups()
#         if unit_string == 'eV':
#             self.unit = materia.eV
#         else:
#             raise ValueError('Cannot parse energy unit in Kohn-Sham Gap section.')
#
#     def _parse_homo(self, line):
#         *_,homo_value = line.split()
#         self.homo = materia.Qty(value=float(homo_value),unit=self.unit)
#
#     def _parse_lumo(self, line):
#         *_,lumo_value = line.split()
#         self.lumo = materia.Qty(value=float(lumo_value),unit=self.unit)
#
#     def _parse_gap(self, line):
#         *_,gap_value = line.split()
#         self.gap = materia.Qty(value=float(gap_value),unit=self.unit)
#
# class NetAtomicCharges(Section):
#     def __init__(self):
#         super().__init__(name='NetAtomicCharges')
#         self.unit = None
#         self.charge_dictionary = {}
#
#     def todict(self):
#         return {'charge_dictionary': self.charge_dictionary}
#
#     def parse(self, line):
#         if 'Atom ' in line:
#             self._parse_unit(line=line)
#         elif 'Sum of atomic charges' in line:
#             self._parse_sum_of_atomic_charges(line=line)
#         elif len(line.split()) > 0 and line.split()[0].isdigit():
#             self._parse_atomic_charge(line=line)
#         else:
#             pass
#
#     def _parse_unit(self, line):
#         (charge_unit_string,) = re.search(r'.*\((.*)\).*$',line).groups()
#         if charge_unit_string == 'eV':
#             self.unit = materia.eV
#         elif charge_unit_string == 'a.u.':
#             self.unit = materia.au_charge
#         else:
#             raise ValueError('Cannot parse charge unit in Net Atomic Charges section.')
#
#     def _parse_atomic_charge(self, line):
#         atom_number,atomic_species,charge = line.split()
#         self.charge_dictionary[int(atom_number)] = (atomic_species,materia.Qty(value=float(charge),unit=self.unit))
#
#     def _parse_sum_of_atomic_charges(self, line):
#         *_,sum_of_atomic_charges_str = line.split()
#         self.sum_of_atomic_charges = materia.Qty(value=float(sum_of_atomic_charges_str),unit=self.unit)
#
# class OrbitalEnergies(Section):
#     def __init__(self):
#         super().__init__(name='OrbitalEnergies')
#         self.alpha = False
#         self.occupied = False
#         self.unit = None
#
#         self.energy_dict = {'alpha': {'occupied': [], 'unoccupied': []},'beta': {'occupied': [], 'unoccupied': []}}
#
#     def todict(self):
#         homo = max(self.energy_dict['alpha']['occupied'],self.energy_dict['beta']['occupied'])
#         lumo = min(self.energy_dict['alpha']['unoccupied'],self.energy_dict['beta']['unoccupied'])
#
#         return {'homo': homo, 'lumo': lumo, **self.energy_dict}
#
#     def parse(self, line):
#         if 'Orbital Energies' in line:
#             self._parse_energy_unit(line=line)
#         elif 'Alpha' in line:
#             self.alpha = True
#         elif 'Beta' in line:
#             self.alpha = False
#         elif 'Occupied' in line:
#             self.occupied = True
#         elif 'Virtual' in line:
#             self.occupied = False
#         else:
#             self._parse_orbital_energies(line=line)
#
#     def _parse_energy_unit(self, line):
#         (unit_str,) = re.search(r'.*\((.*)\).*$',line).groups()
#         if unit_str == 'a.u.':
#             self.unit = materia.hartree
#         else:
#             raise ValueError('Cannot parse energy unit in Orbital Energies section.')
#
#     def _parse_orbital_energies(self, line):
#         try:
#             energies = [materia.Qty(value=float(eng),unit=self.unit) for eng in line.strip().split()]
#             self.energy_dict['alpha' if self.alpha else 'beta']['occupied' if self.occupied else 'unoccupied'].extend(energies)
#         except:
#             pass
# #
# # class Polarizability(Section):
# #     def __init__(self):
# #         super().__init__(name='Polarizability')
# #         self.alpha = False
# #         self.occupied = False
# #         self.unit = None
# #
# #         self.energy_dict = {'alpha': {'occupied': [], 'unoccupied': []},'beta': {'occupied': [], 'unoccupied': []}}
# #
# #     def todict(self):
# #         homo = max(self.energy_dict['alpha']['occupied'],self.energy_dict['beta']['occupied'])
# #         lumo = min(self.energy_dict['alpha']['unoccupied'],self.energy_dict['beta']['unoccupied'])
# #
# #         return {'homo': homo, 'lumo': lumo, **self.energy_dict}
# #
# #     def parse(self, line):
# #         if 'Polarizability tensor' in line:
# #             self._parse_polarizability(line=line)
# #         elif 'Alpha' in line:
# #             self.alpha = True
# #         elif 'Beta' in line:
# #             self.alpha = False
# #         elif 'Occupied' in line:
# #             self.occupied = True
# #         elif 'Virtual' in line:
# #             self.occupied = False
# #         else:
# #             self._parse_orbital_energies(line=line)
# #
# #     def _parse_energy_unit(self, line):
# #         (unit_str,) = re.search(r'.*\((.*)\).*$',line).groups()
# #         if unit_str == 'a.u.':
# #             self.unit = materia.hartree
# #         else:
# #             raise ValueError('Cannot parse energy unit in Orbital Energies section.')
# #
# #     def _parse_orbital_energies(self, line):
# #         try:
# #             energies = [materia.Qty(value=float(eng),unit=self.unit) for eng in line.strip().split()]
# #             self.energy_dict['alpha' if self.alpha else 'beta']['occupied' if self.occupied else 'unoccupied'].extend(energies)
# #         except:
# #             pass
#
# class SETManTiming(Section):
#     def __init__(self):
#         super().__init__(name='SETManTiming')
#
# # class TDDFTExcitationEnergies(Section):
# #     def __init__(self):
# #         self.section_keywords = {'Excited state': TDDFTExcitation}
#
#     # def _parse(self):
#     #     gen = (l for l in self.lines)
#     #     next(self._yield_excitation_blocks(gen=gen)) # first block is just junk, discard it
#     #
#     #     print(list(self._yield_excitation_blocks(gen=gen)))
#     #     for energy_str,tot_energy_str,mult_str,mom_str,strength_str,*contributions_str in self._yield_excitation_blocks(gen=gen):
#     #          print(energy_str)
#     #          print(energy_str)
#     #
#     # def _yield_excitation_blocks(self, gen):
#     #     #gen = (l for l in self.lines)
#     #     while True:
#     #         t = tuple(itertools.takewhile(lambda l: l.strip() != '',gen))
#     #         if t == ():
#     #             break
#     #         yield t
#
# class SCF(Section):
#     def __init__(self):
#         super().__init__(name='SCF')
#         self.scf_steps = {}
#
#     def todict(self):
#         return {'quadrature_grid': self.quadrature_grid, 'number_threads': self.num_threads,
#                 'cpu_time': self.cpu_time, 'wall_time': self.wall_time, 'scf_energy': self.scf_energy,
#                 'total_energy': self.total_energy, **self.scf_steps}
#
#     def parse(self, line):
#         if 'standard quadrature grid' in line:
#             self._parse_quadrature_grid(line=line)
#         elif 'threads for integral computing' in line:
#             self._parse_num_threads(line=line)
#         elif 'SCF time' in line:
#             self._parse_scf_time(line=line)
#         elif len(line.split()) > 0 and line.split()[0].isdigit():
#             self._parse_scf_step(line=line)
#         elif 'energy in the final basis set' in line:
#             self._parse_energy(line=line)
#         else:
#             pass
#
#     def _parse_energy(self, line):
#         energy_type,energy = re.search(r'\s*(.*?)\s*energy in the final basis set.*?(-?\d*\.\d*)\.*$',line).groups()
#         if energy_type == 'SCF':
#             self.scf_energy = materia.Qty(value=float(energy),unit=materia.hartree)
#         elif energy_type == 'Total':
#             self.total_energy = materia.Qty(value=float(energy),unit=materia.hartree)
#         else:
#             pass
#
#     def _parse_quadrature_grid(self, line):
#         self.quadrature_grid,*_ = re.search(r'Using (.*) standard quadrature grid.*$',line).groups()
#
#     def _parse_num_threads(self, line):
#         num_threads,*_ = re.search(r'using (\d*) threads for integral computing.*$',line).groups()
#         self.num_threads = int(num_threads)
#
#     def _parse_scf_step(self, line):
#         scf_step_num,energy,error = re.search(r'\s*(\d*)\s*(-?\d*\.\d*)\s*(\d*\.\d*e-?\d*).*$',line).groups()
#         self.scf_steps[int(scf_step_num)] = (materia.Qty(value=float(energy),unit=materia.hartree),float(error))
#
#     def _parse_scf_time(self, line):
#         cpu_time,cpu_time_unit,wall_time,wall_time_unit = re.search(r'SCF time:\s*CPU (\d*\.\d*)(.*?)\s*wall (\d*\.\d*)(.*?)\s*$',line).groups()
#         self.cpu_time = materia.Qty(value=float(cpu_time),unit=getattr(materia,cpu_time_unit))
#         self.wall_time = materia.Qty(value=float(wall_time),unit=getattr(materia,wall_time_unit))
#
# class SCFGradient(Section):
#     def __init__(self):
#         #FIXME: implement parse(self, line), todict(self)
#         super().__init__(name='SCFGradient')
#
# class StandardNuclearOrientation(Section):
#     def __init__(self):
#         super().__init__(name='StandardNuclearOrientation')
#         self.position_unit = None
#         self.atom_dictionary = {}
#
#     def todict(self):
#         return self.atom_dictionary
#
#     def parse(self, line):
#         if 'Standard Nuclear Orientation' in line:
#             self._parse_atomic_position_unit(line=line)
#         elif len(line.split()) > 0 and line.split()[0].isdigit():
#             self._parse_atomic_position(line=line)
#         else:
#             pass
#
#     def _parse_atomic_position_unit(self, line):
#         (unit_str,) = re.search(r'.*\((.*)\).*$',line).groups()
#         if unit_str == 'Angstroms':
#             self.position_unit = materia.angstrom
#         else:
#             raise ValueError('Cannot parse atomic position unit in Standard Nuclear Orientation section.')
#
#     def _parse_atomic_position(self, line):
#         try:
#             atom_number,atomic_symbol,x,y,z = line.strip().split()
#             atomic_position_value = np.array([float(x),float(y),float(z)]).reshape(3,1)
#             self.atom_dictionary[int(atom_number)] = (atomic_symbol,materia.Qty(value=atomic_position_value,unit=self.position_unit))
#         except ValueError: # wrong line got passed into this function, so just pass without processing
#             pass
#
# class TDDFTExcitation(Section):
#     def __init__(self):
#         super().__init__(name='TDDFTExcitation')
#
#     def parse(self, line):
#         if 'Excited state' in line:
#             self._parse_excited_state(line=line)
#         elif 'Total energy for state' in line:
#             self._parse_excited_total_energy(line=line)
#         elif 'Multiplicity:' in line:
#             self._parse_multiplicity(line=line)
#         elif 'Trans. Mom.' in line:
#             self._parse_transition_dipole(line=line)
#         elif 'Strength' in line:
#             self._parse_oscillator_strength(line=line)
#
#     def todict(self):
#         return {'excitation_energy': self.excitation_energy, 'total_energy': self.total_energy,
#                 'multiplicity': self.multiplicity, 'transition_dipole': self.transition_dipole,
#                 'oscillator_strength': self.oscillator_strength}
#
#     def _parse_excited_state(self, line):
#         (energy_unit_str,energy_value_str) = re.search(r'.*\((.*)\).*=\s*(\d*).*$',line).groups()
#         if energy_unit_str == 'eV':
#             excitation_energy_unit = materia.eV
#         else:
#             raise ValueError('Cannot parse excitation energy unit in TDDFT Excitation section.')
#         energy_value = float(energy_value_str)#float(line.strip().split()[-1])
#         self.excitation_energy = materia.Qty(value=energy_value,unit=excitation_energy_unit)
#
#     def _parse_excited_total_energy(self, line):
#         *_,tot_energy_val_str,tot_energy_unit_str = line.strip().split()
#         if tot_energy_unit_str == 'au':
#             tot_energy_unit = materia.hartree
#         else:
#             raise ValueError('Cannot parse total energy unit in TDDFT Excitation section.')
#         self.total_energy = materia.Qty(value=float(tot_energy_val_str),unit=tot_energy_unit)
#
#     def _parse_multiplicity(self, line):
#         *_,self.multiplicity = line.lower().strip().split()
#
#     def _parse_transition_dipole(self, line):
#         *_,x,_,y,_,z,_ = line.strip().split()
#         self.transition_dipole = materia.Qty(value=np.array([float(x),float(y),float(z)]),unit=materia.debye) # Unit is debye as stated here: http://iopenshell.usc.edu/forum/topic.php?id=3696
#
#     def _parse_oscillator_strength(self, line):
#         *_,strength_val_str = line.strip().split()
#         self.oscillator_strength = float(strength_val_str)
#
#     def _parse(self):
#         #FIXME: fix all this
#         energy_str,tot_energy_str,mult_str,mom_str,strength_str,*contributions_str = self.lines
#
#         # EXCITATION ENERGY
#
#
#
#         # EXCITED TOTAL ENERGY
#
#
#
#         # MULTIPLICITY
#
#
#
#         # TRANSITION DIPOLE
#
#
#
#         # OSCILLATOR STRENGTH
#
#
#         # OCCUPIED-UNOCCUPIED ORBITAL PAIR CONTRIBUTIONS
#
#         contributions_dict = {}
#         for l in contributions_str:
#             stripped = l.strip()
#             if stripped != '':
#                 try:
#                     f,t = re.search(r'.*\((.*)\).*\((.*)\).*$',l).groups()
#                     *_,amplitude_str = stripped.split()
#                     contributions_dict[int(f),int(t)] = float(amplitude_str)
#                 except AttributeError:
#                     break
#
#         return excitation_energy,total_energy,multiplicity,transition_moment,strength,contributions_dict
#
# class TDDFTTDARoots(Section):
#     def __init__(self):
#         super().__init__(name='TDDFTTDARoots')
#
#     def parse(self, line):
#         pass
