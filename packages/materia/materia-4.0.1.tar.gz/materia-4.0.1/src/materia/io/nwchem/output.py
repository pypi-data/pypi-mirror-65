from __future__ import annotations
import collections
import materia
from typing import Iterable, List, Tuple

__all__ = ["NWChemOutput"]


class NWChemOutput:
    def __init__(self, filename: str) -> None:
        self.filename = materia.expand(filename)
        self.output_dict = collections.OrderedDict()

        self.chunk_dict = {
            "input": "echo of input deck",
            "titlecard": "Northwest Computational Chemistry Package (NWChem)",
            "jobinfo": "Job information",
            "meminfo": "Memory information",
            "directoryinfo": "Directory information",
            "dftmodule": "NWChem DFT Module",
            "responsemodule": "*** RESPONSE ***",
            "tddftmodule": "NWChem TDDFT Module",
            "rttddftmodule": "NWChem Real-Time TDDFT Module",
            "gastats": "GA Statistics for process",
        }

        # chunk the output into major sections
        chunk_starts, chunk_types = zip(*self._chunk_file())
        chunks = self._get_chunks(chunk_starts=chunk_starts, chunk_types=chunk_types)

        def get(self, *quantity_names: str):
            method_dict = dict(inspect.getmembers(self, predicate=inspect.isroutine))

            with open(self.filepath, "r") as f:
                lines = "".join(f.readlines())

            quantities = tuple(
                method_dict[name.lower()](lines=lines) for name in quantity_names
            )

            if len(quantities) == 1:
                return quantities[0]
            return quantities

        # fragment each chunk into minor sections
        def modify_chunk_type(x, data={}):
            if x in data:
                data[x] += 1
            else:
                data[x] = 0

            return "{0}{1}".format(x, data[x])

        for chunk, chunk_type in zip(chunks, chunk_types):

            def modify_frag_type(
                x, data={}
            ):  # this is some clever trickery with the default value data={}
                if x in data:
                    data[x] += 1
                else:
                    data[x] = 0
                return "{0}{1}".format(x, data[x])

            fragment_starts, fragment_types = zip(
                *self._fragment_chunk(chunk=chunk, chunk_type=chunk_type)
            )

            unique_fragment_types = [
                modify_frag_type(x=frag_type) for frag_type in fragment_types
            ]
            fragments = self._get_fragments(
                chunk=chunk, fragment_starts=fragment_starts
            )

            self.output_dict[modify_chunk_type(x=chunk_type)] = collections.OrderedDict(
                zip(unique_fragment_types, fragments)
            )

    def _chunk_file(self: str) -> List[Tuple[str, str]]:
        return sorted(
            [
                (x, chunk_type)
                for chunk_type, chunk_keyword in self.chunk_dict.items()
                for x in self._find_chunk_keyword_in_file(chunk_keyword=chunk_keyword)
            ]
        )

    def _find_chunk_keyword_in_file(self, chunk_keyword: str) -> List[int]:
        with open(self.filename, "r") as f:
            return [linenum for linenum, line in enumerate(f) if chunk_keyword in line]

    def _get_chunks(
        self, chunk_starts: Iterable[int], chunk_types: Iterable[str]
    ) -> List[str]:
        cur_ind = 0
        chunk_start = chunk_starts[cur_ind]
        chunk_end = (
            chunk_starts[cur_ind + 1]
            if cur_ind != len(chunk_starts) - 1
            else float("inf")
        )
        cur_chunk = ""
        chunks = []
        with open(self.filename, "r") as f:
            for linenum, line in enumerate(f):
                if linenum < chunk_start:
                    pass
                elif linenum >= chunk_start and linenum < chunk_end:
                    cur_chunk += line
                else:
                    cur_ind += 1
                    chunk_start = chunk_starts[cur_ind]
                    chunk_end = (
                        chunk_starts[cur_ind + 1]
                        if cur_ind != len(chunk_starts) - 1
                        else float("inf")
                    )
                    chunks.append(cur_chunk)
                    cur_chunk = line
        chunks.append(cur_chunk)

        return chunks

    def _fragment_chunk(self, chunk, chunk_type):
        if chunk_type == "input":
            fragment_dict = {"input": "echo of input deck"}
        elif chunk_type == "titlecard":
            fragment_dict = {
                "titlecard": "Northwest Computational Chemistry Package (NWChem)"
            }
        elif chunk_type == "jobinfo":
            fragment_dict = {"jobinfo": "Job information"}
        elif chunk_type == "meminfo":
            fragment_dict = {"meminfo": "Memory information"}
        elif chunk_type == "directoryinfo":
            fragment_dict = {"directoryinfo": "Directory information"}
        elif chunk_type == "dftmodule":
            fragment_dict = {
                "basis": 'Basis "ao basis"',
                "basissummary": 'Summary of "ao basis"',
                "geninfo": "General Information",
                "xcinfo": "XC Information",
                "gridinfo": "Grid Information",
                "convergenceinfo": "Convergence Information",
                "screeninginfo": "Screening Tolerance Information",
                "guess": "Superposition of Atomic Density Guess",
                "scf": "Memory utilization after 1st SCF pass",
                "orbitals": "DFT Final Molecular Orbital Analysis",
                "alpha_orbitals": "DFT Final Alpha Molecular Orbital Analysis",
                "beta_orbitals": "DFT Final Beta Molecular Orbital Analysis",
                "com": "center of mass",
                "moments": "moments of inertia",
                "multipole": "Multipole analysis of the density",
            }
        elif chunk_type == "responsemodule":
            fragment_dict = {
                "header": "Response module for NWChem",
                "field": "Solving response equations for perturbing field",
                "cphf": "NWChem CPHF Module",
                "electricdipoleresponse": "Electric Dipole Response Matrix",
                "linearresponsepolarizability": "DFT Linear Response polarizability",
                "magneticdipoleresponse": "Magnetic Dipole Response Matrix",
            }
        elif chunk_type == "tddftmodule":
            fragment_dict = {
                "geninfo": "General Information",
                "xcinfo": "XC Information",
                "tddftinfo": "TDDFT Information",
                "meminfo": "Memory Information",
                "evaldiffs": "smallest eigenvalue differences",
            }
        elif chunk_type == "rttddftmodule":
            fragment_dict = {
                "basissummary": 'Summary of "ao basis"',
                "geninfo": "General Information",
                "xcinfo": "XC Information",
                "convergenceinfo": "Convergence Information",
                "screeninginfo": "Screening Tolerance Information",
                "propparams": "Propagation parameters",
                "dipolequadrupole": "Dipole and quadrupole matrices",
                "appliedfields": "Applied fields",
                "excitationrules": "Excitation rules",
                "propheader": "shell propagation",
                "propstart": "Propagation started",
                "checkspassed": "Checks passed",
                "savedrestart": "Saved restart file",
                "tddipole": "Dipole moment [system]",
                "istart": "istart",
                "dipcontribx": "Mu-X i-a Contrib",
                "dipcontriby": "Mu-Y i-a Contrib",
                "dipcontribz": "Mu-Z i-a Contrib",
                "propfinish": "Propagation finished",
            }
        elif chunk_type == "gastats":
            fragment_dict = {
                "summary": "Summary of allocated global arrays",
                "stats": "GA Statistics",
            }

        return sorted(
            [
                (x, frag_type)
                for frag_type, frag in fragment_dict.items()
                for x in self._find_fragment_in_chunk(
                    chunk=chunk.split("\n"), fragment=frag
                )
            ]
        )

    def _find_fragment_in_chunk(self, chunk, fragment):
        return [linenum for linenum, line in enumerate(chunk) if fragment in line]

    def _get_fragments(self, chunk, fragment_starts):
        cur_ind = 0
        fragment_start = fragment_starts[cur_ind]
        fragment_end = (
            fragment_starts[cur_ind + 1]
            if cur_ind != len(fragment_starts) - 1
            else float("inf")
        )
        cur_fragment = ""
        fragments = []
        for linenum, line in enumerate(chunk.split("\n")):
            if linenum < fragment_start:
                pass
            elif linenum >= fragment_start and linenum < fragment_end:
                cur_fragment += line + "\n"
            else:
                cur_ind += 1
                fragment_start = fragment_starts[cur_ind]
                fragment_end = (
                    fragment_starts[cur_ind + 1]
                    if cur_ind != len(fragment_starts) - 1
                    else float("inf")
                )
                fragments.append(cur_fragment)
                cur_fragment = line

        fragments.append(cur_fragment)

        return fragments

    def get_orbital_info(
        self, orbitals=None, spin=None, dftmodule_num=0, orbitals_fragment_num=0
    ):
        dft_key = "dftmodule{0}".format(dftmodule_num)

        if spin is None:
            orbital_key = "orbitals{0}".format(orbitals_fragment_num)
        elif hasattr(spin, "lower") and spin.lower() == "alpha":
            orbital_key = "alpha_orbitals{0}".format(orbitals_fragment_num)
        elif hasattr(spin, "lower") and spin.lower() == "beta":
            orbital_key = "beta_orbitals{0}".format(orbitals_fragment_num)
        else:
            raise ValueError(
                "Invalid value for argument spin, which can take values 'alpha','beta', or None."
            )

        orbital_fragment = self.output_dict[dft_key][orbital_key]

        energies = []
        vector_nums = []
        occupancies = []

        mo_centers = []
        mo_r2s = []  # shows how diffuse an orbital is

        for line in orbital_fragment.split("\n"):
            if "Vector" in line:
                partial_1, partial_2, energy = line.split("=")
                _, vector_num, _ = partial_1.split()
                occupancy, _ = partial_2.split()

                energy = float(energy.replace("D", "e"))
                energies.append(energy)

                vector_nums.append(int(vector_num))

                occupancy = float(occupancy.replace("D", "e"))
                occupancies.append(occupancy)
            elif "MO Center" in line:
                _, partial_1, r2 = line.split("=")
                x, y, z, _, = partial_1.strip().split(",")

                x = float(x.replace("D", "e"))
                y = float(y.replace("D", "e"))
                z = float(z.replace("D", "e"))
                mo_centers.append((x, y, z))

                r2 = float(r2.replace("D", "e"))
                mo_r2s.append(r2)

        orbital_dicts = (
            {
                "energy": units.Qty(value=eng, unit=units.hartree),
                "occupancy": units.Qty(value=occ, unit=units.Unit(base="unitless")),
                "center": units.Qty(value=moc, unit=units.Unit(base="bohr")),
                "R2": units.Qty(value=mor2, unit=units.Unit(base="bohr") ** 2),
            }
            for eng, occ, moc, mor2 in zip(energies, occupancies, mo_centers, mo_r2s)
        )

        if orbitals is None:
            return dict(zip(vector_nums, orbital_dicts))
        else:
            return {
                num: od
                for num, od in zip(vector_nums, orbital_dicts)
                if num in orbitals
            }

    def get_homo_lumo(self, dftmodule_num=0, orbitals_fragment_num=0):
        dft_key = "dftmodule{0}".format(dftmodule_num)

        if self.is_spin_polarized(dftmodule_num=dftmodule_num):
            alpha_info = self.get_orbital_info(
                spin="alpha",
                dftmodule_num=dftmodule_num,
                orbitals_fragment_num=orbitals_fragment_num,
            )
            alpha_homo = max(
                od["energy"] for od in alpha_info.values() if od["occupancy"] != 0
            )
            alpha_lumo = min(
                od["energy"] for od in alpha_info.values() if od["occupancy"] == 0
            )

            beta_info = self.get_orbital_info(
                spin="beta",
                dftmodule_num=dftmodule_num,
                orbitals_fragment_num=orbitals_fragment_num,
            )
            beta_homo = max(
                od["energy"] for od in beta_info.values() if od["occupancy"] != 0
            )
            beta_lumo = min(
                od["energy"] for od in beta_info.values() if od["occupancy"] == 0
            )

            homo = max(alpha_homo, beta_homo)
            lumo = min(alpha_lumo, beta_lumo)
        else:
            orbital_info = self.get_orbital_info(
                dftmodule_num=dftmodule_num, orbitals_fragment_num=orbitals_fragment_num
            )
            homo = max(
                [od["energy"] for od in orbital_info.values() if od["occupancy"] != 0]
            )
            lumo = min(
                [od["energy"] for od in orbital_info.values() if od["occupancy"] == 0]
            )

        return {"homo": homo, "lumo": lumo, "gap": lumo - homo}

    def is_spin_polarized(self, dftmodule_num=0):
        dft_key = "dftmodule{0}".format(dftmodule_num)
        return (
            sum(
                (k.startswith("alpha_orbitals") or k.startswith("beta_orbitals"))
                for k in self.output_dict[dft_key].keys()
            )
            > 0
        )

    def get_total_energies(self, dftmodule_num=0, scf_fragment_num=0):
        dft_key = "dftmodule{0}".format(dftmodule_num)
        scf_key = "dftmodule{0}".format(scf_fragment_num)

        energy_fragment = self.output_dict[dft_key][scf_key]

        energy_dict = {}
        for line in energy_fragment.split("\n"):
            if "Total DFT energy" in line:
                _, total_energy = line.split("=")
                total_energy = float(total_energy.replace("D", "e"))
                energy_dict["total_energy"] = units.Qty(
                    value=total_energy, unit=units.hartree
                )
            elif "One electron energy" in line:
                _, one_electron_energy = line.split("=")
                one_electron_energy = float(one_electron_energy.replace("D", "e"))
                energy_dict["one_electron_energy"] = units.Qty(
                    value=one_electron_energy, unit=units.hartree
                )
            elif "Coulomb energy" in line:
                _, coulomb_energy = line.split("=")
                coulomb_energy = float(coulomb_energy.replace("D", "e"))
                energy_dict["coulomb_energy"] = units.Qty(
                    value=coulomb_energy, unit=units.hartree
                )
            elif "Exchange-Corr. energy" in line:
                _, xc_energy = line.split("=")
                xc_energy = float(xc_energy.replace("D", "e"))
                energy_dict["xc_energy"] = units.Qty(
                    value=xc_energy, unit=units.hartree
                )
            elif "Nuclear repulsion energy" in line:
                _, nuclear_repulsion_energy = line.split("=")
                nuclear_repulsion_energy = float(
                    nuclear_repulsion_energy.replace("D", "e")
                )
                energy_dict["nuclear_repulsion_energy"] = units.Qty(
                    value=nuclear_repulsion_energy, unit=units.hartree
                )
            elif "COSMO energy" in line:
                _, cosmo_energy = line.split("=")
                cosmo_energy = float(cosmo_energy.replace("D", "e"))
                energy_dict["cosmo_energy"] = units.Qty(
                    value=cosmo_energy, unit=units.hartree
                )

        return energy_dict

    def get_polarizability(self, responsemodule_num=0, polarize_fragment_num=0):
        response_key = "responsemodule{0}".format(responsemodule_num)
        polarize_key = "linearresponsepolarizability{0}".format(polarize_fragment_num)

        polarizability_fragment = self.output_dict[response_key][polarize_key].split(
            "\n"
        )

        header_string = polarizability_fragment[:4]
        matrix_string = polarizability_fragment[4:7]
        eigenvalues_string = polarizability_fragment[8]
        isotropic_string = polarizability_fragment[9]
        anisotropic_string = polarizability_fragment[10]

        matrix_elements = [
            float(str)
            for m in matrix_string
            for str in m.split()
            if str not in ("X", "Y", "Z")
        ]
        polarizability_matrix = np.array(matrix_elements).reshape((3, 3))

        _, _, eig1, eig2, eig3 = eigenvalues_string.split()
        eigenvalues = (float(eig1), float(eig2), float(eig3))

        _, _, iso = isotropic_string.split()
        isotropic_polarizability = float(iso)

        _, _, aniso = anisotropic_string.split()
        anisotropy = float(aniso)

        return units.Qty(value=polarizability_matrix, unit=units.au_volume)

        # return {'polarizability_matrix': units.Qty(value=polarizability_matrix,unit=units.au_volume),
        #         'polarizability_eigenvalues': units.Qty(value=eigenvalues,unit=units.au_volume),
        #         'isotropic_polarizability': units.Qty(value=isotropic_polarizability,unit=units.au_volume),
        #         'polarizability_anisotropy': units.Qty(value=anisotropy,unit=units.au_volume),
        #        }

    def get_tddipole(self, rttddftmodule_num=None, field_tag=None, appliedfields_num=0):
        if rttddftmodule_num is None:
            rttddft_keys = (
                k for k in self.output_dict.keys() if k.startswith("rttddftmodule")
            )
        else:
            rttddft_keys = (f"rttddftmodule{rttddftmodule_num}",)

        result_dict = {}

        for rttddft_key in rttddft_keys:
            rttddft_dict = self.output_dict[rttddft_key]

            tddipole_keys = [k for k in rttddft_dict.keys() if k.startswith("tddipole")]

            if field_tag is None:
                field_tags = (
                    tag
                    for tag, _, _, _, _, _, _, _, _ in (
                        rttddft_dict[k].split() for k in tddipole_keys
                    )
                )
            else:
                field_tags = (field_tag,)

            result = {}

            for ft in field_tags:
                tddipole_keys = [
                    k for k in rttddft_dict.keys() if k.startswith("tddipole")
                ]
                time, mu_x, mu_y, mu_z = zip(
                    *(
                        (float(t), float(x), float(y), float(z))
                        for tag, t, x, y, z, _, _, _, _ in (
                            rttddft_dict[k].split() for k in tddipole_keys
                        )
                        if tag == ft
                    )
                )

                applied_field_fragment = rttddft_dict[
                    f"appliedfields{appliedfields_num}"
                ].split("\n")
                applied_field_header = applied_field_fragment[:3]
                (
                    applied_field_type_str,
                    applied_field_polarization_str,
                    applied_field_maximum_str,
                    _,
                    _,
                    _,
                ) = applied_field_fragment[3:]

                _, _, applied_field_type = applied_field_type_str.split()
                (
                    _,
                    _,
                    applied_field_polarization,
                ) = applied_field_polarization_str.split()
                (
                    _,
                    _,
                    _,
                    _,
                    _,
                    _,
                    applied_field_maximum,
                    _,
                ) = applied_field_maximum_str.split()

                time_unit = units.Unit("au_time")
                dipole_unit = units.au_dipole_moment
                applied_field_unit = units.volt / units.Unit("nanometer")

                result[ft] = {
                    "time": units.Qty(value=np.array(time), unit=time_unit),
                    "mu_x": units.Qty(value=np.array(mu_x), unit=dipole_unit),
                    "mu_y": units.Qty(value=np.array(mu_y), unit=dipole_unit),
                    "mu_z": units.Qty(value=np.array(mu_z), unit=dipole_unit),
                    "E_max": units.Qty(
                        value=applied_field_maximum, unit=applied_field_unit
                    ),
                    "E_shape": applied_field_type,
                    "E_polarization": applied_field_polarization,
                }

            result_dict[rttddft_key] = result

        return result_dict

    def plot_tddipole(self, rttddftmodule_num=None, field_tag=None):
        tddipole_dict = self.get_tddipole(
            field_tag=field_tag, rttddftmodule_num=rttddftmodule_num
        )
        for rttddftmodule_num, result_dict in tddipole_dict.items():
            for field_tag, result in result_dict.items():
                time = result["time"]
                mu_x = result["mu_x"]
                mu_y = result["mu_y"]
                mu_z = result["mu_z"]

                plt.plot(
                    time.value, mu_x.value, label=f"x_{field_tag}_{rttddftmodule_num}"
                )
                plt.plot(
                    time.value, mu_y.value, label=f"y_{field_tag}_{rttddftmodule_num}"
                )
                plt.plot(
                    time.value, mu_z.value, label=f"z_{field_tag}_{rttddftmodule_num}"
                )
                plt.title("Dynamic dipole moments")
                plt.xlabel("Time ({0})".format(time.unit))
                plt.ylabel("Dipole moment ({0})".format(mu_x.unit))

        plt.legend()
        plt.show()

    def get_dipcontribs(self, dipcontrib_dir, rttddftmodule_num=0, i=None, a=None):
        # FIXME: there is currently no way to get dipcontribs by field tag like
        # there is with get_tddipole; consider fixing by not fragmenting dipcontribs
        # and tddipoles apart but rather storing them together
        rttddft_key = "rttddftmodule{0}".format(rttddftmodule_num)
        rttddft_dict = self.output_dict[rttddft_key]

        # dipcontrib_keys = [k for k in rttddft_dict.keys() if k.startswith('dipcontrib')]
        # dipcontribx_keys = [k for k in dipcontrib_keys if k.startswith('dipcontribx')]
        # dipcontriby_keys = [k for k in dipcontrib_keys if k.startswith('dipcontriby')]
        # dipcontribz_keys = [k for k in dipcontrib_keys if k.startswith('dipcontribz')]
        #
        # for direction in ('x','y','z'):
        #     dipcontrib_dir_keys = [k for k in dipcontrib_keys if k.startswith('dipcontrib{0}'.format(direction))]
        #     from_orbitals_key,to_orbitals_key,propagation_keys = dipcontrib_dir_keys[0],dipcontrib_dir_keys[1],dipcontrib_dir_keys[2:]
        #
        #     orbital_pairs = [(int(i),int(a)) for i,a in zip(rttddft_dict[from_orbitals_key].split(),rttddft_dict[to_orbitals_key].split()) if i not in ('#Mu-X','#Mu-Y','#Mu-Z','i-a','Contrib','CLOSED') and a not in ('#Mu-X','#Mu-Y','#Mu-Z','i-a','Contrib','CLOSED')]
        #
        #     np.array([[float(p) for p in rttddft_dict[k].split()[:-4]] for k in propagation_keys]))
        #
        #
        #
        # from_orbital_nums = tuple(int(i) for i in rttddft_dict[dipcontrib_keys[0]].split()[:-4])
        # to_orbital_nums = tuple(int(a) for a in rttddft_dict[dipcontrib_keys[1]].split()[:-4])
        #
        # zip(*((float(t),float(x),float(y),float(z)) for tag,t,x,y,z,_,_,_,_ in (rttddft_dict[k].split() for k in propagation_keys) if tag == field_tag))
        #
        # print(len(rttddft_dict[dipcontrib_keys[2]].split()[:-4]))
        #
        # print(len(list(zip(from_orbital_nums,to_orbital_nums))))

        dipcontribs = [
            [float(x) for x in rttddft_dict[k].split()[:-4]]
            for k in rttddft_dict.keys()
            if "dipcontrib{0}".format(dipcontrib_dir) in k
        ]
        # need to cut out first two rows (don't currently understand these outputs from NWChem)
        # first column (first row after transpose) represents the time
        ia_pairs = np.array([(int(x), int(y)) for x, y in zip(*dipcontribs[0:2])])
        dipcontrib_array = np.array(dipcontribs[2:]).T
        time = dipcontrib_array[0]

        return {
            "time": units.Qty(value=time, unit=units.Unit(base="au_time")),
            "dipole_contributions": units.Qty(
                value=dipcontribs, unit=units.au_dipole_moment
            ),
            "orbital_pairs": units.Qty(
                value=ia_pairs, unit=units.Unit(base="unitless")
            ),
        }

        # if i is not None or a is not None:
        #     if i is not None and a is None:
        #         plot_inds = [ind+1 for ind,(j,b) in enumerate(ia_pairs) if j == i]
        #     elif i is None and a is not None:
        #         plot_inds = [ind+1 for ind,(j,b) in enumerate(ia_pairs) if b == a]
        #     elif i is not None and a is not None:
        #         plot_inds = [ind+1 for ind,(j,b) in enumerate(ia_pairs) if j == i and b == a]
        #
        #     ia_pair_inds = [ind-1 for ind in plot_inds]
        #
        #     return ia_pairs[ia_pair_inds],time,dipcontrib_array[plot_inds]
        # else:

    #     #     return ia_pairs,time,dipcontrib_array[1:]
    #
    # def plot_dipcontrib(self,rttddft_key,dipcontrib_dir,i=None,a=None):
    #     ia_pairs,time,dipcontrib_array = self.get_dipcontribs(rttddft_key=rttddft_key,dipcontrib_dir=dipcontrib_dir)
    #
    #     if i is not None and a is None:
    #         ia_pair_inds = [ind for ind,(j,b) in enumerate(ia_pairs) if j == i]
    #     elif i is None and a is not None:
    #         ia_pair_inds = [ind for ind,(j,b) in enumerate(ia_pairs) if b == a]
    #     elif i is not None and a is not None:
    #         ia_pair_inds = [ind for ind,(j,b) in enumerate(ia_pairs) if j == i and b == a]
    #     else:
    #         ia_pair_inds = [ind for ind,(j,b) in enumerate(ia_pairs)]
    #
    #     #!!! the * notation here is not correct yet - some occupied orbitals are included!!
    #     for row in dipcontrib_array[ia_pair_inds]:
    #         plt.plot(time,row)
    #     plt.legend(['{0} --> {1}*'.format(x,y) for x,y in ia_pairs[ia_pair_inds]])
    #     plt.show()
    #
    #     plt.plot(-0.5*np.sum(dipcontrib_array,0))


# def parse_dipole(filename):
#     dipole_dict = {}
#     with open(filename,'r') as f:
#         dmx_lines = [line for line in f if 'DMX' in line]
#     with open(filename,'r') as f:
#         dmy_lines = [line for line in f if 'DMY' in line]
#     with open(filename,'r') as f:
#         dmz_lines = [line for line in f if 'DMZ' in line]
#
#     dipole_dict['dmx_au'] = float(dmx_lines[0].split()[1])
#     dipole_dict['dmx_efc_au'] = float(dmx_lines[0].split()[-1])
#     dipole_dict['dmx_debye'] = float(dmx_lines[1].split()[1])
#     dipole_dict['dmx_efc_debye'] = float(dmx_lines[1].split()[-1])
#
#     dipole_dict['dmy_au'] = float(dmy_lines[0].split()[1])
#     dipole_dict['dmy_efc_au'] = float(dmy_lines[0].split()[-1])
#     dipole_dict['dmy_debye'] = float(dmy_lines[1].split()[1])
#     dipole_dict['dmy_efc_debye'] = float(dmy_lines[1].split()[-1])
#
#     dipole_dict['dmz_au'] = float(dmz_lines[0].split()[1])
#     dipole_dict['dmz_efc_au'] = float(dmz_lines[0].split()[-1])
#     dipole_dict['dmz_debye'] = float(dmz_lines[1].split()[1])
#     dipole_dict['dmz_efc_debye'] = float(dmz_lines[1].split()[-1])
#
#     dipole_dict['total_dipole_au'] = np.linalg.norm([dipole_dict['dmx_au']+dipole_dict['dmx_efc_au'],dipole_dict['dmy_au']+dipole_dict['dmy_efc_au'],dipole_dict['dmz_au']+dipole_dict['dmz_efc_au']])
#     dipole_dict['total_dipole_debye'] = np.linalg.norm([dipole_dict['dmx_debye']+dipole_dict['dmx_efc_debye'],dipole_dict['dmy_debye']+dipole_dict['dmy_efc_debye'],dipole_dict['dmz_debye']+dipole_dict['dmz_efc_debye']])
#
#     return dipole_dict
