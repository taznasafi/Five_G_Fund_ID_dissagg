from Five_G_Fund_ID_dissagg import five_g
from Five_G_Fund_ID_dissagg import get_path
from pprint import pprint


if __name__ == '__main__':
    test = five_g.GeoTools()
    test.outputPathFolder = "54664"
    test.outputGDBName = "delete_me"
    #test.create_gdb()



    test_2 = get_path.pathFinder(env_0=r"D:\FCC_GIS_Projects\Five_G_Fund\disagg\dagg_11_f477_2018_06_voice_coverage_subsidized_item_grid_overlap_1x1.gdb")
    reference_names = test_2.make_list_from_filename(inlist=test_2.get_path_for_all_feature_from_gdb())
    #print(reference_names)
    test_3 = get_path.pathFinder(env_0=r"D:\Coverage_data\F-477\2018June\f477_2018_06_Broadband.gdb")

    match_names = test_3.make_list_from_filename(inlist=test_3.get_file_path_with_wildcard_from_gdb("*_83"),
                                                 regex=r"(?P<pname>\w.+)_(?P<tech>\d{1,2})")

    #print(match_names)


    a = test_2.check_names_return_tuple_list(reference_dict=reference_names,
                                         match_dict=match_names)

    #print(a[1])

    #print(a[2])
    for i,id,score in a[2]:
        print("{} \n{} {}\n\n\n".format(i, id, score))

    #print(a[3])
    #print(a.keys())

