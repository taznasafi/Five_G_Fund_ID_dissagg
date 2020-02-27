from Five_G_Fund_ID_dissagg import five_g
import paths


def rename_f477_files(run=False):

    _01_rename_f477 = five_g.GeoTools()
    _01_rename_f477.inputGDB = paths.f477_gdb
    if run:
        _01_rename_f477.rename_f477_fc(in_reference_list=paths.provider_pid_name)

