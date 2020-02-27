from Five_G_Fund_ID_dissagg import five_g
import paths, os


def id_disag_voice_with_lte(run=False, wildcard= None):
    _02_id = five_g.GeoTools()
    _02_id.inputGDB = paths.disag_voice
    _02_id.inputGDB2 = paths.f477_gdb
    _02_id.outputPathFolder = _02_id.base_input_folder
    _02_id.outputGDBName = "_01_id_diss"
    _02_id.create_gdb()
    five_g.GeoTools.init_input_dic[_02_id.outputGDBName] = os.path.join(_02_id.outputPathFolder,
                                                                        _02_id.outputGDBName+".gdb")
    _02_id.outputGDB = five_g.GeoTools.init_input_dic[_02_id.outputGDBName]
    if run:
        _02_id.id_the_voice_coverage(wildcard=wildcard)

def id_disag_service_with_lte(run = False, wildcard = None):
    _02_id = five_g.GeoTools()
    _02_id.inputGDB = paths.disag_service
    _02_id.inputGDB2 = paths.f477_gdb
    _02_id.outputPathFolder = _02_id.base_input_folder
    _02_id.outputGDBName = "_01_id_diss"
    _02_id.create_gdb()
    five_g.GeoTools.init_input_dic[_02_id.outputGDBName] = os.path.join(_02_id.outputPathFolder,
                                                                        _02_id.outputGDBName + ".gdb")
    _02_id.outputGDB = five_g.GeoTools.init_input_dic[_02_id.outputGDBName]
    if run:
        _02_id.id_the_voice_coverage(wildcard=wildcard)


def add_field(run=False, wildcard = None, field_name="overlap_between_sub_voice_and_LTE", field_length = None, field_type = "SHORT"):
    _02_id = five_g.GeoTools()
    _02_id.inputGDB = five_g.GeoTools.init_input_dic["_01_id_diss"]
    if run:
        _02_id.add_field(field_name=field_name, field_type=field_type, field_length=field_length, wildcard=wildcard)


def pop_overlap_field(run = False, field_name = "overlap_between_sub_voice_and_LTE"):
    _02_id = five_g.GeoTools()
    _02_id.inputGDB = five_g.GeoTools.init_input_dic["_01_id_diss"]
    if run:
        _02_id.pop_field(wildcard="*", field_name=field_name)


def calculate_field(run=False, wildcard = None, field_name="overlap_between_sub_voice_and_LTE", code=None):
    _02_id = five_g.GeoTools()
    _02_id.inputGDB = five_g.GeoTools.init_input_dic["_01_id_diss"]
    if run:
        _02_id.calculate_field(field_name=field_name, wildcard=wildcard,code=code)

def calculate_total_area(run = False, wildcard = None, field_name = None, column_to_be_summed = None):
    _02_id = five_g.GeoTools()
    _02_id.inputGDB = five_g.GeoTools.init_input_dic["_01_id_diss"]

    if run:
        _02_id.calculate_field(field_name=field_name, wildcard=wildcard,
                               add_column_value=True, sum_col=column_to_be_summed)


def grouped_df(run = False, field_list = None, wildcard = None, table_name = None):
    _02_id = five_g.GeoTools()
    _02_id.inputGDB = five_g.GeoTools.init_input_dic["_01_id_diss"]
    _02_id.outputPathFolder = five_g.GeoTools.base_output_folder
    if run:
        _02_id.fc_table_to_grouped_df(field_list = field_list,
                                      wildcard=wildcard,table_name=table_name)
