from Five_G_Fund_ID_dissagg import logger
import os
import arcpy
import pandas as pd
import paths
from Five_G_Fund_ID_dissagg import get_path
from pprint import pprint



class GeoTools:
    init_input_dic = {}
    base_input_folder = r'./data/input'
    base_output_folder = r'./data/output'

    def __int__(self, inputPath=None, inputGDB=None, inputGDB2=None, outputGDBName=None, outputPathFolder=None,
                outputGDB=None, name=None):
        self.inputPath = inputPath
        self.inputGDB = inputGDB
        self.inputGDB2 = inputGDB2
        self.outputGDBName = outputGDBName
        self.outputPathFolder = outputPathFolder
        self.outputGDB = outputGDB
        self.name = name
        self.fcList = None
        self.input_dict = None
        self.output_dict = {}

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def create_gdb(self):

        gdb_path = os.path.join(self.outputPathFolder, self.outputGDBName + ".gdb")
        if not arcpy.Exists(gdb_path):

            arcpy.CreateFileGDB_management(out_folder_path=self.outputPathFolder, out_name=self.outputGDBName)
            print(arcpy.GetMessages(0))
        else:
            print("GDB Exists")


    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def rename_f477_fc(self, in_reference_list=None):


        in_list = get_path.pathFinder(env_0=self.inputGDB).get_path_for_all_feature_from_gdb()

        for fc in in_list:

            print(os.path.basename(fc)[:-3])

            match_name_dic = get_path.pathFinder.query_pid_by_dba(in_reference_list,dba=os.path.basename(fc)[:-3])

            #print(match_name_dic['provider_id'])

            arcpy.Rename_management(in_data=fc,out_data=fc+"_{}".format(match_name_dic['provider_id']))





    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def id_the_voice_coverage(self, wildcard = None):

        print("identifying the voice coverage")

        in_fc_list = get_path.pathFinder(env_0=self.inputGDB).get_path_for_all_feature_from_gdb()

        in_fc_dic = get_path.pathFinder.make_list_from_filename(in_fc_list)

        pprint(in_fc_dic)

        for k,v in in_fc_dic.items():

            in_fc = k

            if k is None:
                print("K is a pass")
                pass
            #print(k,v)

            print(list(v))

            id_fc = get_path.pathFinder(self.inputGDB2).get_file_path_with_wildcard_from_gdb(wildcard="*_{}_{}".format(wildcard, list(v)[0][1]))

            if len(id_fc)==0:
                output = os.path.join(self.outputGDB, "{}_{}".format('NOT_identified', os.path.basename(k)))
            else:
                output = os.path.join(self.outputGDB, "{}_{}".format('identified',os.path.basename(k)))

            if not arcpy.Exists(output):

                if len(id_fc) == 0:

                    arcpy.CopyFeatures_management(in_features=in_fc, out_feature_class=output)
                else:
                    arcpy.Identity_analysis(in_features=in_fc, identity_features=id_fc[0],out_feature_class=output)
                    print(arcpy.GetMessages(0))

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def add_field(self, field_name, field_type, field_length=None, wildcard=None):

        print("\nadding field")
        master_list = get_path.pathFinder(env_0=self.inputGDB).get_path_for_all_feature_from_gdb()

        fc_list = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(master_list, wildcard)

        for fc in fc_list:
            arcpy.AddField_management(fc, field_name, field_type, field_length)
            print(arcpy.GetMessages(0))

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def pop_field(self, wildcard=None, field_name = None):
        print("\nadding field")
        master_list = get_path.pathFinder(env_0=self.inputGDB).get_path_for_all_feature_from_gdb()

        fc_list = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(master_list, wildcard)

        for fc in fc_list:



            field_exists, num_fields, field_list = self.field_exists(fc_path=fc,field_wildcard="FID_*")

            print(field_list)

            field_list.append(field_name)

            print(field_list)


            if (field_exists==True and num_fields==2):

                with arcpy.da.UpdateCursor(fc, field_list) as cursor:

                    for row in cursor:
                        if row[1] == -1:
                            row[2] = 0
                        else:
                            row[2] = 1

                        cursor.updateRow(row)
            elif (field_exists==True, num_fields < 2):

                with arcpy.da.UpdateCursor(fc, field_list) as cursor:

                    for row in cursor:
                        row[0] = 0
                        cursor.updateRow(row)


    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def field_exists(self, fc_path, field_wildcard):
        field_list = [f.name for f in arcpy.ListFields(fc_path, field_wildcard)]


        if len(field_list) >0:
            return True, len(field_list), field_list

        else:
            return False, len(field_list), field_list

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def calculate_field(self, code=None, field_name=None, wildcard=None, add_column_value = False, sum_col = None):


        print("\ncalculating field")
        master_list = get_path.pathFinder(env_0=self.inputGDB).get_path_for_all_feature_from_gdb()

        fc_list = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(master_list, wildcard)

        for fc in fc_list:

            if add_column_value:
                arcpy.CalculateField_management(in_table=fc, field=field_name,
                                                expression=self.add_column_value(fc=fc,field_list=sum_col),
                                                expression_type="PYTHON3")
                print(arcpy.GetMessages(0))
            else:

                arcpy.CalculateField_management(in_table=fc,field=field_name,expression=code,expression_type="PYTHON3")
                print(arcpy.GetMessages(0))

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def add_column_value(self, fc, field_list):

        row_sum = []
        with arcpy.da.SearchCursor(fc, field_list) as cursor:
            for row in cursor:
                row_sum.append(row[0])
        #print(row_sum)

        return sum(row_sum)

    @logger.arcpy_exception(logger.create_error_logger())
    @logger.event_logger(logger.create_logger())
    def fc_table_to_grouped_df(self, field_list, wildcard=None, table_name = None):

        master_list = get_path.pathFinder(env_0=self.inputGDB).get_path_for_all_feature_from_gdb()

        fc_list = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(master_list, wildcard)

        df_list = []
        for fc in fc_list:
            df_list.append(pd.DataFrame(arcpy.da.FeatureClassToNumPyArray(in_table = fc,
                                                                          field_names = field_list)))
        df = pd.concat(df_list)
        if table_name is not None:
            df.to_csv(os.path.join(self.outputPathFolder, table_name+'_raw.csv'))
        
        df_grouped = df.groupby(['state_fips', 'provider_id', 'provider_name','eligible_flag', 'overlap_flag', 'overlap_between_sub_voice_and_LTE', 'total_coverage_area'])['area_sq_km', 're_Adjusted_sq_km', 're_dis_fhc'].sum()

        if table_name is not None:
            df_grouped.to_csv(os.path.join(self.outputPathFolder, table_name+'_summed.csv'))

        
            
                           

