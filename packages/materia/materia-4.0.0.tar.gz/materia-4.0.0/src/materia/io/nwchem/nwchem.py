# from __future__ import annotations
# import os
# import subprocess

# from ...workflow.tasks.task import Task

# __all__ = ["ExecuteNWChem"]


# class ExecuteNWChem(Task):
#     def __init__(
#         self,
#         input_name,
#         output_name,
#         executable="nwchem",
#         work_directory=".",
#         num_cores=1,
#         parallel=False,
#         handlers=None,
#         name=None,
#     ):
#         super().__init__(handlers=handlers)
#         self.settings["input_path"] = materia.expand(
#             os.path.join(work_directory, input_name)
#         )
#         self.settings["output_path"] = materia.expand(
#             os.path.join(work_directory, output_name)
#         )
#         self.settings["scratch_directory"] = materia.expand(scratch_directory)

#         self.settings["executable"] = executable
#         self.settings["work_directory"] = materia.expand(work_directory)

#         self.settings["num_cores"] = num_cores
#         self.settings["parallel"] = parallel

#         try:
#             os.makedirs(self.settings["work_directory"])
#         except FileExistsError:
#             pass

#     def run(self):
#         with open(self.settings["output_path"], "w") as f:
#             if self.settings["parallel"]:
#                 subprocess.call(
#                     [
#                         "mpirun",
#                         "-np",
#                         str(self.settings["num_cores"]),
#                         self.settings["executable"],
#                         self.settnigs["input_path"],
#                     ],
#                     stdout=f,
#                 )
#             else:
#                 subprocess.call(
#                     [self.settings["executable"], self.settings["input_path"]], stdout=f
#                 )


# # from ..calculation import Calculation
# #
# # class NWChemPolarizability(Calculation):
# #     def __init__(self):
# #         raise NotImplementedError
# #
# # class NWChemRTTDDFT(Calculation):
# #     def __init__(self):
# #         raise NotImplementedError
# #
# # def compute_polarizability(self, molecule, num_cores, parallel, header_params={},\
# #                            geometry_params={}, set_geometry_params={}, basis_params={},\
# #                            dft_params={}, property_params={}, task_params={}):
# #
# #     input_path = os.path.join(self.scratch_directory,'polarizability.in')
# #     output_path = os.path.join(self.scratch_directory,'polarizability.out')
# #
# #     default_header_params = {'title':'molecule','echo':True,'scratch_dir':'./scratch','permanent_dir':'./permanent','start': True}
# #     merged_header_params = self._merge_new_params(old_params=default_header_params,new_params=header_params)
# #
# #     default_geometry_params = {'title': 'system', 'xyz_filepath': molecule.xyz.filepath}
# #     merged_geometry_params = self._merge_new_params(old_params=default_geometry_params,new_params=geometry_params)
# #
# #     default_set_geometry_params = {'set_params': {'variable_name': 'geometry', 'variable_value': '\"system\"'}}
# #     merged_set_geometry_params = self._merge_new_params(old_params=default_set_geometry_params,new_params=set_geometry_params)
# #
# #     default_basis_params = {'atom_strings': ('*',), 'library_strings': ('6-311G**',)}
# #     merged_basis_params = self._merge_new_params(old_params=default_basis_params,new_params=basis_params)
# #
# #     default_dft_params = {'direct': True, 'xc_params': {'xc_functional_strings': ('b3lyp',)}}
# #     merged_dft_params = self._merge_new_params(old_params=default_dft_params,new_params=dft_params)
# #
# #     default_property_params = {'response_order': 1, 'response_frequency': 0}
# #     merged_property_params = self._merge_new_params(old_params=default_property_params,new_params=property_params)
# #
# #     default_task_params = {'task_params': {'theory_level': 'dft', 'operation': 'property'}}
# #     merged_task_params = self._merge_new_params(old_params=default_task_params,new_params=task_params)
# #
# #     input = NWChemInput()
# #     input.add_block(top=merged_header_params)
# #     input.add_block(geometry=merged_geometry_params)
# #     input.add_block(top=merged_set_geometry_params)
# #     input.add_block(basis=merged_basis_params)
# #     input.add_block(dft=merged_dft_params)
# #     input.add_block(property=merged_property_params)
# #     input.add_block(top=merged_task_params)
# #     input.write_input(filename=input_path)
# #
# #     self.execute(input_path=input_path,output_path=output_path,num_cores=num_cores,parallel=parallel)
# #
# #     output = NWChemOutput(filename=output_path)
# #
# #     molecule.polarizability = output.get_polarizability()
# #
# # def compute_dynamic_dipole_moment(self, molecule, num_cores, parallel,
# #                                   x=True, y=True, z=True, header_params={},
# #                                   geometry_params={}, set_geometry_params={},
# #                                   basis_params={}, dft_params={}, dft_task_params={},
# #                                   rttddft_x_params={}, rttddft_x_task_params={},
# #                                   rttddft_y_params={}, rttddft_y_task_params={},
# #                                   rttddft_z_params={}, rttddft_z_task_params={}):
# #
# #     input_path = os.path.join(self.scratch_directory,'dynamic_dipole_moment.in')
# #     output_path = os.path.join(self.scratch_directory,'dynamic_dipole_moment.out')
# #
# #     input = NWChemInput()
# #
# #     default_header_params = {'title':'molecule','echo':True,'scratch_dir':'./scratch','permanent_dir':'./permanent','start': True}
# #     merged_header_params = self._merge_new_params(old_params=default_header_params,new_params=header_params)
# #     input.add_block(top=merged_header_params)
# #
# #     default_geometry_params = {'title': 'system', 'xyz_filepath': molecule.xyz.filepath}
# #     merged_geometry_params = self._merge_new_params(old_params=default_geometry_params,new_params=geometry_params)
# #     input.add_block(geometry=merged_geometry_params)
# #
# #     default_set_geometry_params = {'set_params': {'variable_name': 'geometry', 'variable_value': '\"system\"'}}
# #     merged_set_geometry_params = self._merge_new_params(old_params=default_set_geometry_params,new_params=set_geometry_params)
# #     input.add_block(top=merged_set_geometry_params)
# #
# #     default_basis_params = {'atom_strings': ('*',), 'library_strings': ('6-311G**',)}
# #     merged_basis_params = self._merge_new_params(old_params=default_basis_params,new_params=basis_params)
# #     input.add_block(basis=merged_basis_params)
# #
# #     default_dft_params = {'direct': True, 'xc_params': {'xc_functional_strings': ('b3lyp',)}}
# #     merged_dft_params = self._merge_new_params(old_params=default_dft_params,new_params=dft_params)
# #     input.add_block(dft=merged_dft_params)
# #
# #     default_dft_task_params = {'task_params': {'theory_level': 'dft', 'operation': 'energy'}}
# #     merged_dft_task_params = self._merge_new_params(old_params=default_dft_task_params,new_params=dft_task_params)
# #     input.add_block(top=merged_dft_task_params)
# #
# #     if x:
# #         default_rttddft_x_params = {'tmax':500.0,'dt':0.1,'tag':'kickx','print_dipole':True,
# #                                     'load_type': 'vectors', 'load_from': os.path.join(self.scratch_directory,'permanent','molecule.movecs'),
# #                                     'field_params':{'field_name':'kick','shape':'delta','polarization':'x','max': 1e-4},
# #                                     'excite_params':{'geometry_name':'system','field_name':'kick'}}
# #         merged_rttddft_x_params = self._merge_new_params(old_params=default_rttddft_x_params,new_params=rttddft_x_params)
# #         input.add_block(rttddft=merged_rttddft_x_params)
# #
# #         default_rttddft_x_task_params = {'task_params': {'theory_level': 'dft', 'operation': 'rt_tddft'}}
# #         merged_rttddft_x_task_params = self._merge_new_params(old_params=default_rttddft_x_task_params,new_params=rttddft_x_task_params)
# #         input.add_block(top=merged_rttddft_x_task_params)
# #
# #     if y:
# #         default_rttddft_y_params = {'tmax':500.0,'dt':0.1,'tag':'kicky','print_dipole':True,
# #                                     'load_type': 'vectors', 'load_from': os.path.join(self.scratch_directory,'permanent','molecule.movecs'),
# #                                     'field_params':{'field_name':'kick','shape':'delta','polarization':'y','max': 1e-4},
# #                                     'excite_params':{'geometry_name':'system','field_name':'kick'}}
# #         merged_rttddft_y_params = self._merge_new_params(old_params=default_rttddft_y_params,new_params=rttddft_y_params)
# #         input.add_block(rttddft=merged_rttddft_y_params)
# #
# #         default_rttddft_y_task_params = {'task_params': {'theory_level': 'dft', 'operation': 'rt_tddft'}}
# #         merged_rttddft_y_task_params = self._merge_new_params(old_params=default_rttddft_y_task_params,new_params=rttddft_y_task_params)
# #         input.add_block(top=merged_rttddft_y_task_params)
# #
# #     if z:
# #         default_rttddft_z_params = {'tmax':500.0,'dt':0.1,'tag':'kickz','print_dipole':True,
# #                                     'load_type': 'vectors', 'load_from': os.path.join(self.scratch_directory,'permanent','molecule.movecs'),
# #                                     'field_params':{'field_name':'kick','shape':'delta','polarization':'z','max': 1e-4},
# #                                     'excite_params':{'geometry_name':'system','field_name':'kick'}}
# #         merged_rttddft_z_params = self._merge_new_params(old_params=default_rttddft_z_params,new_params=rttddft_z_params)
# #         input.add_block(rttddft=merged_rttddft_z_params)
# #
# #         default_rttddft_z_task_params = {'task_params': {'theory_level': 'dft', 'operation': 'rt_tddft'}}
# #         merged_rttddft_z_task_params = self._merge_new_params(old_params=default_rttddft_z_task_params,new_params=rttddft_z_task_params)
# #         input.add_block(top=merged_rttddft_z_task_params)
# #
# #     input.write_input(input_path)
# #
# #     self.execute(input_path=input_path,output_path=output_path,num_cores=num_cores,parallel=parallel)
# #
# #     output = NWChemOutput(filename=output_path)
# #
# #     tddipole_dict = output.get_tddipole()
# #
# #     molecule.tddipole_x = (tddipole_dict['time'],tddipole_dict['mu_x'])
# #     molecule.tddipole_y = (tddipole_dict['time'],tddipole_dict['mu_y'])
# #     molecule.tddipole_z = (tddipole_dict['time'],tddipole_dict['mu_z'])
