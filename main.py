from bin import _01_rename_f477, _02_id_voice_with_f477

print("rename files")
_01_rename_f477.rename_f477_files(run=False)
print("identifying voice coverages")
#_02_id_voice_with_f477.id_disag_voice_with_lte(run=False,wildcard="*83")

print("identifying service areas")
_02_id_voice_with_f477.id_disag_service_with_lte(run = True, wildcard="*83")

print("add fields")
_02_id_voice_with_f477.add_field(run = True, wildcard="*")
print("Populating overlap field")
_02_id_voice_with_f477.pop_overlap_field(run = True)

print("adding and calculating area field fields")
_02_id_voice_with_f477.add_field(run = True, wildcard="*",field_name="area_sq_km",field_type="DOUBLE")
_02_id_voice_with_f477.calculate_field(run=True, wildcard="*", field_name="area_sq_km", code="!SHAPE.geodesicAREA@SQUAREKILOMETERS!")

print("calculating total area of fields")
_02_id_voice_with_f477.add_field(run = True, wildcard="*",field_name="total_coverage_area",field_type="DOUBLE")
_02_id_voice_with_f477.calculate_total_area(run=True, wildcard="*",field_name="total_coverage_area",
                                            column_to_be_summed='area_sq_km')

print("calculating adjust square mile of fields")
_02_id_voice_with_f477.add_field(run = True, wildcard="*",field_name="re_Adjusted_sq_km",field_type="DOUBLE")
_02_id_voice_with_f477.calculate_field(run=True, wildcard="*", field_name="re_Adjusted_sq_km", code="!terrain_factor!*!area_sq_km!")


print("calculating dissagg high cost support mile of fields")
_02_id_voice_with_f477.add_field(run = True, wildcard="*",field_name="re_dis_fhc",field_type="DOUBLE")
_02_id_voice_with_f477.calculate_field(run=True, wildcard="*", field_name="re_dis_fhc", code="!cetc_sac_fhcs_rate!*!re_Adjusted_sq_km!")

print("grouping dissagg high cost support ")
_02_id_voice_with_f477.grouped_df(run=True,wildcard="*",
                                  field_list=['state_fips', 'provider_id', 'provider_name','eligible_flag','overlap_flag', 'overlap_between_sub_voice_and_LTE','total_coverage_area','area_sq_km',
                                              're_Adjusted_sq_km', 're_dis_fhc'],
                                  table_name="ALL_disagg_id_by_LTE")



